from doctomarkdown.base import BaseConverter, PageResult, ConversionResult
from doctomarkdown.utils.markdown_helpers import generate_markdown_from_text
from typing import Optional
from docx import Document
import logging

logger = logging.getLogger(__name__)

class DocxToMarkdown(BaseConverter):
    """Converter for DOCX files to Markdown format."""

    def extract_content(self):
        doc = Document(self.filepath)
        use_llm = hasattr(self, 'llm_client') and self.llm_client is not None

        pages = []          
        markdown_lines = []

        text = []
        for para in doc.paragraphs:
            text.append(para.text)
       
        page_content = "\n\n".join(text)
        try:
            if use_llm:
                llm_result = generate_markdown_from_text(
                    self.llm_client,
                    self.llm_model,
                    page_content,
                    "You are an expert at converting DOCX content to Markdown."
                )
                page_content = f"\n{llm_result}"
        except Exception as e:
            logger.warning(f"LLM extraction failed for DOCX: {e}")

       
        pages.append(PageResult(1, page_content))
        markdown_lines.append(f"## Page 1\n\n{page_content}\n")

        self._markdown = "\n".join(markdown_lines)
        return pages