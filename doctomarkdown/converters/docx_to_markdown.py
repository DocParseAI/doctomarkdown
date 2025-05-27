from doctomarkdown.base import BaseConverter, PageResult, ConversionResult
from docx import Document
from docx2python import docx2python

class DocxToMarkdown(BaseConverter):
    """Converter for DOCX files to Markdown format."""
    
    def extract_content(self):
        
        
        doc = docx2python(self.filepath)
        pages = []
        markdown_lines = []

        for page_number, page in enumerate(doc.body, 1):
            page_content = "\n".join(page)
            pages.append(PageResult(page_number, page_content))
            markdown_lines.append(f"## Page {page_number}\n\n{page_content}\n")

        self._markdown = "\n".join(markdown_lines)
        return pages