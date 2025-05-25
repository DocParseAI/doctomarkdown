from doctomarkdown.base import BaseConverter, PageResult, ConversionResult
from typing import Optional
import fitz #PyMuPDF
from doctomarkdown.utils.markdown_helpers import image_bytes_to_base64
from doctomarkdown.utils.prompts import pdf_to_markdown_system_prompt,pdf_to_markdown_user_role_prompt
from doctomarkdown.llmwrappers import GeminiWrapper
import logging

logger = logging.getLogger(__name__)

class PdfToMarkdown(BaseConverter):
    def extract_content(self):
        doc = fitz.open(self.filepath)
        pages = []
        markdown_lines = []
        use_llm = hasattr(self, 'llm_client') and self.llm_client is not None and hasattr(self, 'llm_model') and self.llm_model is not None
        user_prompt = hasattr(self, 'llm_prompt') and self.llm_prompt
        llm_client = getattr(self, 'llm_client', None)
        llm_model = getattr(self, 'llm_model', None)

        for page_number, page in enumerate(doc, 1):
            text = page.get_text("text")
            page_content = text.strip()
            # If LLM client and model are provided, send page image to LLM for markdown extraction
            if use_llm:
                try:
                    pix = page.get_pixmap()
                    base64_image = image_bytes_to_base64(pix.tobytes())
                    page_content = self.generate_markdown_from_image(base64_image)
                except Exception as e:
                    logger.warning(f"LLM extraction failed for page {page_number}: {e}")
            pages.append(PageResult(page_number, page_content))
            markdown_lines.append(f"## Page {page_number}\n\n{page_content}\n")

            if self.extract_images:
                images = page.get_images(full=True)
                for img_index, img in enumerate(images):
                    xref = img[0]
                    pix = fitz.Pixmap(doc, xref)
                    if pix.n < 5:
                        img_path = f"{self.output_path}/page{page_number}_img{img_index}.png"
                        pix.save(img_path)
                        markdown_lines.append(f"![Image]({img_path})")
                    pix = None

        self._markdown = "\n".join(markdown_lines)
        return pages
    
    def generate_markdown_from_image(self, base64_image: str) -> str:
        # a function to determine to call LLM based on user preference
        if "gemini" in self.llm_model:
            from PIL import Image
            import io
            import base64
            # create a wrapper around gemini vision model to work as same way as groq style
            gemini_client = GeminiWrapper(self.llm_client)
            image_data = base64.b64decode(base64_image)
            image = Image.open(io.BytesIO(image_data))

            response = gemini_client.generate_content([
                {"text": pdf_to_markdown_system_prompt()},
                {"text": pdf_to_markdown_user_role_prompt()},
                image
            ])
            return response.text

        elif hasattr(self.llm_client, "chat"):
            # OpenAI/Groq style
            response = self.llm_client.chat.completions.create(
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
            )
            return response.choices[0].message.content

        else:
            raise ValueError("Unsupported LLM client type.")
