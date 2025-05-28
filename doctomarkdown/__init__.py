from doctomarkdown.converters.pdf_to_markdown import PdfToMarkdown
from doctomarkdown.converters.docx_to_markdown import DocxToMarkdown
from doctomarkdown.converters.pptx_to_markdown import PptxToMarkdown
from doctomarkdown.converters.csv_to_markdown import CsvToMarkdown
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
        if not filepath.lower().endswith('.pdf'):
            raise ValueError("Unsupported file type for PDF conversion. Please provide a .pdf file.")
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
        if not filepath.lower().endswith('.docx'):
            raise ValueError("Unsupported file type for DOCX conversion. Please provide a .docx file.")
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
        if not filepath.lower().endswith('.pptx'):
            raise ValueError("Unsupported file type for PPTX conversion. Please provide a .pptx file.")
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
    
    def convert_csv_to_markdown(self, filepath: str, extract_images: bool = False, extract_tables: bool = False, output_path: Optional[str] = None, **kwargs):
        """
        Convert a CSV file to Markdown.
        
        Args:
            filepath (str): Path to the CSV file to convert.
            extract_images (bool, optional): If True, extract images from the CSV file. Defaults to False.
            extract_tables (bool, optional): If True, extract tables from the CSV file. Defaults to False.
            output_path (str, optional): If provided, save the Markdown output to this path.
            **kwargs: Additional keyword arguments passed to the converter.
        
        Returns:
            ConversionResult:
            page_number (int): The number of pages in the CSV file.
            page_content (str): The content of the CSV file in Markdown format.
        """
        if not filepath.lower().endswith('.csv'):
            raise ValueError("Unsupported file type for CSV conversion. Please provide a .csv file.")
        csv_converter = CsvToMarkdown(
            filepath=filepath,
            extract_images=extract_images,
            extract_tables=extract_tables,
            output_path=output_path,
            **kwargs
        )
        return csv_converter.convert()