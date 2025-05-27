from doctomarkdown.converters.pdf_to_markdown import PdfToMarkdown
from doctomarkdown.converters.docx_to_markdown import DocxToMarkdown
from doctomarkdown.converters.pptx_to_markdown import PptxToMarkdown
from typing import Optional

class DocToMarkdown:
    def __init__(self, llm_client: Optional[object] = None, llm_model: Optional[str] = None):
        self.llm_client = llm_client
        self.llm_model = llm_model

    def convert_pdf_to_markdown(self, filepath: str, extract_images: bool = False, extract_tables: bool = False, output_path: Optional[str] = None, **kwargs):
        """
        Convert a PDF file to Markdown.
        Args:
            filepath (str): Path to the PDF file to convert.
            extract_images (bool, optional): If True, extract images from the PDF file. Defaults to False.
            extract_tables (bool, optional): If True, extract tables from the PDF file. Defaults to False.
            output_path (str, optional): If provided, save the Markdown output to this path.
            **kwargs: Additional keyword arguments passed to the converter.
        
        Returns:
            ConversionResult:
            page_number (int): The number of pages in the pdf file.
            page_content (str): The content of the pdf file in Markdown format.
        """
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
            ConversionResult:
            page_number (int): The number of pages in the docx file.
            page_content (str): The content of the docx file in Markdown format.
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
    
    def convert_pptx_to_markdown(self, filepath: str, extract_images: bool = False, extract_tables: bool = False, output_path: Optional[str] = None, **kwargs):
        """
        Convert a PPTX file to Markdown.
        
        Args:
            filepath (str): Path to the PPTX file to convert.
            extract_images (bool, optional): If True, extract images from the PPTX file. Defaults to False.
            extract_tables (bool, optional): If True, extract tables from the PPTX file. Defaults to False.
            output_path (str, optional): If provided, save the Markdown output to this path.
            **kwargs: Additional keyword arguments passed to the converter.
        
        Returns:
            ConversionResult:
            page_number (int): The number of pages in the PPTX file.
            page_content (str): The content of the PPTX file in Markdown format.
        """
        pptx_converter = PptxToMarkdown(
            filepath=filepath,
            llm_client=self.llm_client,
            llm_model=self.llm_model,
            extract_images=extract_images,
            extract_tables=extract_tables,
            output_path=output_path,
            **kwargs
        )
        return pptx_converter.convert()