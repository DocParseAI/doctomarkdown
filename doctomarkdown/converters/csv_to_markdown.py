from doctomarkdown.base import BaseConverter, PageResult, ConversionResult
import pandas as pd

class CsvToMarkdown(BaseConverter):
    """Converter for CSV files to Markdown format."""
    
    def __init__(self, filepath, extract_images=False, extract_tables=False, output_path=None, output_type='markdown', **kwargs):
        super().__init__(filepath=filepath, extract_images=extract_images, extract_tables=extract_tables, output_path=output_path, output_type=output_type, **kwargs)

    def extract_content(self):
        
        df = pd.read_csv(self.filepath)
        markdown_content = df.to_markdown(index=False)
        page_result = PageResult(page_number=1, page_content=markdown_content)
        self._markdown = markdown_content
        return [page_result]