from doctomarkdown.base import BaseConverter, PageResult, ConversionResult
from typing import Optional
import fitz #PyMuPDF
from doctomarkdown.utils.markdown_helpers import image_bytes_to_base64
from doctomarkdown.utils.prompts import pdf_to_markdown_system_prompt,pdf_to_markdown_user_role_prompt
from doctomarkdown.llmwrappers.GeminiWrapper import GeminiVisionWrapper
from doctomarkdown.utils.image_to_markdown import image_to_markdown
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
                    llm_result = image_to_markdown(self.llm_client, self.llm_model, base64_image)
                    page_content = (
                        f"\n{llm_result}"
                    )
            except Exception as e:
                logger.warning(f"LLM extraction failed for page {page_number}: {e}")
            pages.append(PageResult(page_number, page_content))
            markdown_lines.append(f"## Page {page_number}\n\n{page_content}\n")

        self._markdown = "\n".join(markdown_lines)
        return pages
