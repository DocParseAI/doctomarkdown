from doctomarkdown.base import BaseConverter, PageResult, ConversionResult
import pandas as pd

class CsvToMarkdown(BaseConverter):
    """Converter for CSV files to Markdown format."""
    
    def extract_content(self):
        
        # Read the CSV file into a DataFrame
        df = pd.read_csv(self.filepath)
        
        # Convert the DataFrame to Markdown format
        markdown_content = df.to_markdown(index=False)
        
        # Create a single PageResult for the entire CSV content
        page_result = PageResult(page_number=1, page_content=markdown_content)
        
        self._markdown = markdown_content
        return [page_result]