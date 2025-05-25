from doctomarkdown.converters.pdf_to_markdown import PdfToMarkdown
from typing import Optional

class DocToMarkdown:
    def __init__(self, llm_client: Optional[object] = None, llm_model: Optional[str] = None):
        self.llm_client = llm_client
        self.llm_model = llm_model

    def convert_pdf_to_markdown(self, filepath: str, extract_images: bool = False, extract_tables: bool = False, output_path: Optional[str] = None, **kwargs):
        pdf_converter = PdfToMarkdown(
            filepath=filepath,
            llm_client=self.llm_client,
            llm_model=self.llm_model,
            extract_images=extract_images,
            extract_tables=extract_tables,
            output_path=output_path,
            **kwargs
        )
        return pdf_converter.convert()