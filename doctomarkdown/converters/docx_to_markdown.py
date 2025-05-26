from doctomarkdown.base import BaseConverter, PageResult, ConversionResult
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

        # For simplicity, treat the whole document as one "page"
        text = []
        for para in doc.paragraphs:
            text.append(para.text)
        page_content = "\n\n".join(text)

        # If LLM is available, you could process the text or images here
        try:
            if use_llm and hasattr(self, "generate_markdown_from_text"):
                llm_result = self.generate_markdown_from_text(page_content)
                page_content = f"\n{llm_result}"
        except Exception as e:
            logger.warning(f"LLM extraction failed for DOCX: {e}")

        pages.append(PageResult(1, page_content))
        markdown_lines.append(f"## Page 1\n\n{page_content}\n")

        self._markdown = "\n".join(markdown_lines)
        return pages

    # Optional: Implement LLM-based text enhancement if needed
    def generate_markdown_from_text(self, text: str) -> str:
        if hasattr(self.llm_client, "chat"):
            def call_llm():
                return self.llm_client.chat.completions.create(
                    model=self.llm_model,
                    messages=[
                        {"role": "system", "content": "You are an expert at converting DOCX content to Markdown."},
                        {"role": "user", "content": text}
                    ],
                    temperature=0,
                ).choices[0].message.content
            return call_llm()
        else:
            raise ValueError("Unsupported LLM client type.")