from doctomarkdown.base import BaseConverter, PageResult, ConversionResult
import fitz #PyMuPDF
from doctomarkdown.utils.markdown_helpers import image_bytes_to_base64
from doctomarkdown.llmwrappers.ExceptionWrapper import handleException
from doctomarkdown.utils.content_to_markdown import image_to_markdown_llm, image_to_markdown_ocr
import logging

logger = logging.getLogger(__name__)

class PdfToMarkdown(BaseConverter):
    """Converter for PDF files to Markdown format using LLMs for image content extraction or OCR fallback."""
    def __init__(self, filepath, extract_images=False, extract_tables=False, output_path=None, llm_client=None, llm_model=None, output_type='markdown', **kwargs):
        super().__init__(filepath=filepath, extract_images=extract_images, extract_tables=extract_tables, output_path=output_path, llm_client=llm_client, llm_model=llm_model, output_type=output_type, **kwargs)

    def extract_content(self):
        try:
            logger.info(f"[INFO] Starting PDF extraction for: {self.filepath}")
            doc = fitz.open(self.filepath)
            if not doc.is_pdf:
                raise Exception("Use convert_pdf_to_markdown to convert pdf files only")
        except Exception as e:
            logger.error(f"[FAILURE] Unable to process the pdf file {self.filepath}: {e}")
            raise
        
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
                    logger.info(f"[INFO] Using LLM extraction for page {page_number} of {self.filepath}")
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
                    logger.info(f"[SUCCESS] LLM extraction successful for page {page_number} of {self.filepath}")
                else:
                    # Only use OCR if no text was found
                    if not text:
                        logger.info(f"[INFO] No text found, using OCR for page {page_number} of {self.filepath}")
                        page_content = image_to_markdown_ocr(pix)
                        logger.info(f"[SUCCESS] OCR extraction successful for page {page_number} of {self.filepath}")
            except Exception as e:
                logger.warning(f"[FAILURE] Extraction failed for page {page_number} of {self.filepath}: {e}")
            pages.append(PageResult(page_number, page_content))
            page_content = f"Page Number: {page_number}\nPage Content:\n{page_content}\n"
            markdown_lines.append(page_content)

        self._markdown = "\n".join(markdown_lines)
        logger.info(f"[SUCCESS] PDF extraction completed for: {self.filepath}")
        return pages
