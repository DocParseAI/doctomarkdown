from doctomarkdown.converters.pdf_to_markdown import PdfToMarkdown
from typing import Optional

class DocToMarkdown:
    def __init__(self, use_llm: bool = False, llm: Optional[object] = None):
        self.use_llm = use_llm
        self.llm = llm
        # You can store other global settings here if needed

    def convert_pdf_to_markdown(self, filepath: str, extract_images: bool = False, extract_tables: bool = False, output_path: Optional[str] = None, **kwargs):
        pdf_converter = PdfToMarkdown(
            filepath=filepath,
            use_llm=self.use_llm,
            extract_images=extract_images,
            extract_tables=extract_tables,
            output_path=output_path,
            llm=self.llm,
            **kwargs
        )
        return pdf_converter.convert()