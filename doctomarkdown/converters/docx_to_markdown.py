from doctomarkdown.base import BaseConverter, PageResult
from docx import Document
from doctomarkdown.llmwrappers.ExceptionWrapper import handleException
from doctomarkdown.utils.content_to_markdown import text_to_markdown_llm, text_to_markdown_fallback
from docx2pdf import convert as docx2pdf_convert
from doctomarkdown.converters.pdf_to_markdown import PdfToMarkdown
import logging
import tempfile
import os
import shutil

logger = logging.getLogger(__name__)

class DocxToMarkdown(BaseConverter):
    """Converter for DOCX files to Markdown format using LLM or fallback."""

    def __init__(self, filepath, extract_images=False, extract_tables=False, output_path=None, llm_client=None, llm_model=None, output_type='markdown', **kwargs):
        super().__init__(filepath=filepath, extract_images=extract_images, extract_tables=extract_tables, output_path=output_path, llm_client=llm_client, llm_model=llm_model, output_type=output_type, **kwargs)

    def extract_content(self):
        temp_dir = None
        try:
            
            temp_dir = tempfile.mkdtemp()
            input_docx = self.filepath
            pdf_basename = os.path.splitext(os.path.basename(input_docx))[0] + '.pdf'
            output_pdf = os.path.join(temp_dir, pdf_basename)
            # Convert DOCX to PDF
            docx2pdf_convert(input_docx, output_pdf)
            if os.path.exists(output_pdf):
                pdf_converter = PdfToMarkdown(
                    filepath=output_pdf,
                    llm_client=getattr(self, 'llm_client', None),
                    llm_model=getattr(self, 'llm_model', None),
                    extract_images=self.extract_images,
                    extract_tables=self.extract_tables,
                    output_path=None,  # Don't save PDF output, just get content
                    output_type=self.output_type
                )
                pages = pdf_converter.extract_content()
                self._markdown = getattr(pdf_converter, '_markdown', None)
                logger.info(f"[SUCCESS] Extraction is successful via PDF for file: {self.filepath}")
                return pages
            else:
                logger.error(f"[ERROR] PDF file not found after DOCX to PDF conversion: {output_pdf}")
                raise Exception(f"PDF file not found after DOCX to PDF conversion: {output_pdf}")
        except Exception as e:
            logger.error(f"[FAILURE] Error during DOCX to PDF conversion for {self.filepath}: {e}")
            raise
        finally:
            if temp_dir and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
