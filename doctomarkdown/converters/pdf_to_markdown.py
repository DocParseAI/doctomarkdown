from doctomarkdown.base import BaseConverter, PageResult, ConversionResult
from typing import Optional
import fitz #PyMuPDF
from doctomarkdown.utils.markdown_helpers import image_bytes_to_base64
from doctomarkdown.utils.prompts import pdf_to_markdown_system_prompt,pdf_to_markdown_user_role_prompt
from doctomarkdown.llmwrappers.GeminiWrapper import GeminiVisionWrapper
import logging

logger = logging.getLogger(__name__)

class PdfToMarkdown(BaseConverter):
    """Converter for PDF files to Markdown format using LLMs for image content extraction."""
    def extract_content(self):
        doc = fitz.open(self.filepath)
        use_llm = hasattr(self, 'llm_client') and self.llm_client is not None

        pages = []
        markdown_lines = []

        for page_number, page in enumerate(doc, 1):
            text = page.get_text("text").strip()
            pix = page.get_pixmap()
            base64_image = image_bytes_to_base64(pix.tobytes())

            page_content = text
            try:
                if use_llm:
                    llm_result = self.generate_markdown_from_image(base64_image)
                    page_content = (
                        f"\n{llm_result}"
                    )
            except Exception as e:
                logger.warning(f"LLM extraction failed for page {page_number}: {e}")
            pages.append(PageResult(page_number, page_content))
            markdown_lines.append(f"## Page {page_number}\n\n{page_content}\n")

        self._markdown = "\n".join(markdown_lines)
        return pages
    
    def generate_markdown_from_image(self, base64_image: str) -> str:
        if not self.llm_model and hasattr(self.llm_client, 'model_name') and "gemini" in self.llm_client.model_name:
            from PIL import Image
            import io
            import base64
            gemini_client = GeminiVisionWrapper(self.llm_client)
            image_data = base64.b64decode(base64_image)
            image = Image.open(io.BytesIO(image_data))
            response = gemini_client.generate_content([
                {"text": pdf_to_markdown_system_prompt()},
                {"text": pdf_to_markdown_user_role_prompt()},
                image
            ])
            return response.text
        elif hasattr(self.llm_client, "chat"):
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
            return call_groqai()
        else:
            raise ValueError("Unsupported LLM client type.")
