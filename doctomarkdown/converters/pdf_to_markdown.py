from doctomarkdown.base import BaseConverter, PageResult, ConversionResult
import fitz #PyMuPDF
from doctomarkdown.utils.markdown_helpers import image_bytes_to_base64
from doctomarkdown.llmwrappers.ExceptionWrapper import handleException
from doctomarkdown.utils.content_to_markdown import image_to_markdown_llm, image_to_markdown_ocr
import logging

logger = logging.getLogger(__name__)

class PdfToMarkdown(BaseConverter):
    """Converter for PDF files to Markdown format using LLMs for image content extraction or OCR fallback."""
    def extract_content(self):
        try:
            doc = fitz.open(self.filepath)
            if not doc.is_pdf:
                raise Exception("Use convert_pdf_to_markdown to convert pdf files only")
        except Exception as e:
            logger.error(f"Unable to process the pdf file {e}")      # will log error if filepath is wrong or corrupt file  
        
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
                    llm_result = handleException(
                        max_retry=2,
                        fun=image_to_markdown_llm,
                        fallback_fun=image_to_markdown_ocr,
                        llm_client=self.llm_client,
                        llm_model=self.llm_model,
                        base64_image=base64_image,
                        pix=pix,
                        context="pdf"
                    )
                    page_content = (
                        f"\n{llm_result}"
                    )
                else:
                    # Only use OCR if no text was found
                    if not text:
                        page_content = image_to_markdown_ocr(pix)
            except Exception as e:
                logger.warning(f"Extraction failed for page {page_number} : {e}")
            pages.append(PageResult(page_number, page_content))
            markdown_lines.append(f"## Page {page_number}\n\n{page_content}\n")

        self._markdown = "\n".join(markdown_lines)
        return pages
