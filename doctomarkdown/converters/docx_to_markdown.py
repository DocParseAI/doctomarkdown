from doctomarkdown.base import BaseConverter, PageResult
from docx import Document
from doctomarkdown.llmwrappers.ExceptionWrapper import handleException
from doctomarkdown.utils.content_to_markdown import text_to_markdown_llm, text_to_markdown_fallback
import logging

logger = logging.getLogger(__name__)

class DocxToMarkdown(BaseConverter):
    """Converter for DOCX files to Markdown format using LLM or fallback."""

    def extract_content(self):
        try:
            doc = Document(self.filepath)
        except Exception as e:
            logger.error(f"Unable to process the DOCX file: {e}")
            raise Exception("Invalid DOCX file provided.")

        use_llm = hasattr(self, 'llm_client') and self.llm_client is not None

        pages = []
        markdown_lines = []

        text = []
        for para in doc.paragraphs:
            text.append(para.text.strip())
        
        page_content = "\n\n".join(text)
        try:
            if use_llm:
                llm_result = handleException(
                    max_retry=2,
                    fun=text_to_markdown_llm,
                    fallback_fun=text_to_markdown_fallback,
                    llm_client=self.llm_client,
                    llm_model=self.llm_model,
                    raw_text=page_content,
                    context="docx"
                )
                page_content = f"\n{llm_result}"
        except Exception as e:
            logger.warning(f"LLM extraction failed for DOCX: {e}")

        pages.append(PageResult(1, page_content))
        markdown_lines.append(f"## Page 1\n\n{page_content}\n")

        self._markdown = "\n".join(markdown_lines)
        return pages
