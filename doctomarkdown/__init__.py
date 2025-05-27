from doctomarkdown.converters.pdf_to_markdown import PdfToMarkdown
from doctomarkdown.converters.docx_to_markdown import DocxToMarkdown
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

    def convert_docx_to_markdown(self, filepath: str, extract_images: bool = False, extract_tables: bool = False, output_path: Optional[str] = None, **kwargs):
        """
        Convert a DOCX file to Markdown.

        Args:
            filepath (str): Path to the DOCX file to convert.
            extract_images (bool, optional): If True, extract images from the DOCX file. Defaults to False.
            extract_tables (bool, optional): If True, extract tables from the DOCX file. Defaults to False.
            output_path (str, optional): If provided, save the Markdown output to this path.
            **kwargs: Additional keyword arguments passed to the converter.

        Returns:
            ConversionResult: The result of the conversion, including Markdown content and any extracted assets.
        """
        docx_converter = DocxToMarkdown(
            filepath=filepath,
            llm_client=self.llm_client,
            llm_model=self.llm_model,
            extract_images=extract_images,
            extract_tables=extract_tables,
            output_path=output_path,
            **kwargs
        )
        return docx_converter.convert()