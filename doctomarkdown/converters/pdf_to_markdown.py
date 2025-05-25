from doctomarkdown.base import BaseConverter, PageResult, ConversionResult
from typing import Optional
import fitz #PyMuPDF
from doctomarkdown.utils.markdown_helpers import image_bytes_to_base64
from doctomarkdown.utils.prompts import pdf_to_markdown_system_prompt,pdf_to_markdown_user_role_prompt
from doctomarkdown.llmwrappers.GeminiWrapper import GeminiVisionWrapper
import logging
import asyncio

logger = logging.getLogger(__name__)

class PdfToMarkdown(BaseConverter):
    async def extract_content(self):
        doc = fitz.open(self.filepath)
        use_llm = hasattr(self, 'llm_client') and self.llm_client is not None

        tasks = []
        pages = []
        markdown_lines = []

        for page_number, page in enumerate(doc, 1):
            text = page.get_text("text").strip()
            pix = page.get_pixmap()
            base64_image = image_bytes_to_base64(pix.tobytes())

            async def process_page(pn=page_number, raw_text=text, base64=base64_image):
                page_content = raw_text
                try:
                    if use_llm:
                        llm_result = await self.generate_markdown_from_image(base64)
                        page_content = (
                            f"### Raw Text:\n{raw_text}\n\n"
                            "---\n\n"
                            f"### LLM Markdown:\n{llm_result}"
                        )
                except Exception as e:
                    logger.warning(f"LLM extraction failed for page {pn}: {e}")
                return PageResult(pn, page_content)

            tasks.append(process_page())

        # Await all LLM processing
        results = await asyncio.gather(*tasks)

        for result in results:
            pages.append(result)
            markdown_lines.append(f"## Page {result.page_number}\n\n{result.page_content}\n")

        self._markdown = "\n".join(markdown_lines)
        return pages
    
    async def generate_markdown_from_image(self, base64_image: str) -> str:
        # a function to determine to call LLM based on user preference
        if not self.llm_model and "gemini" in self.llm_client.model_name:
            from PIL import Image
            import io
            import base64
            # create a wrapper around gemini vision model to work as same way as groq style
            gemini_client = GeminiVisionWrapper(self.llm_client)
            image_data = base64.b64decode(base64_image)
            image = Image.open(io.BytesIO(image_data))
            response = await gemini_client.generate_content_async([
                {"text": pdf_to_markdown_system_prompt()},
                {"text": pdf_to_markdown_user_role_prompt()},
                image
            ])
            return response.text

        elif hasattr(self.llm_client, "chat"):
            # Use a thread executor to wrap sync call
            loop = asyncio.get_event_loop()

            def call_groqai():
                return self.llm_client.chat.completions.create(
                    model=self.llm_model,
                    messages=[
                        {"role": "system", "content": pdf_to_markdown_system_prompt()},
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": pdf_to_markdown_user_role_prompt()},
                                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
                            ]
                        }
                    ],
                    temperature=0,
                ).choices[0].message.content

            return await loop.run_in_executor(None, call_groqai)
        else:
            raise ValueError("Unsupported LLM client type.")
