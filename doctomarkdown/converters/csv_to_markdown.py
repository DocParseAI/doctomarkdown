from doctomarkdown.base import BaseConverter, PageResult, ConversionResult
import pandas as pd

class CsvToMarkdown(BaseConverter):
    """Converter for CSV files to Markdown format."""
    
    def extract_content(self):
        
        df = pd.read_csv(self.filepath)
        markdown_content = df.to_markdown(index=False)
        page_result = PageResult(page_number=1, page_content=markdown_content)
        self._markdown = markdown_content
        return [page_result]