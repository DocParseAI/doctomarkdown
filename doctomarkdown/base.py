from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, Union, List
import os

class PageResult:
    def __init__(self, page_number: int, page_content: str):
        self.page_number = page_number
        self.page_content = page_content

class ConversionResult:
    def __init__(self, pages: List[PageResult]):
        self.pages = pages

class BaseConverter(ABC):
    def __init__(
        self,
        filepath: str,
        extract_images: bool = False,
        extract_tables: bool = False,
        output_path: Optional[str] = None,
        llm_client: Optional[object] = None,
        llm_model: Optional[str] = None,
        llm_prompt: Optional[str] = None,
        **kwargs: Any
    ):
        self.filepath = filepath
        self.extract_images = extract_images
        self.extract_tables = extract_tables
        self.output_path = output_path
        self.llm_client = llm_client
        self.llm_model = llm_model
        self.llm_prompt = llm_prompt
        self.kwargs = kwargs #for future extension
    
    @abstractmethod
    def extract_content(self) -> str:
        """Extract Contents and return it in markdown format"""
        pass

    def save_markdown(self, content: str) -> str:
        """Save the markdown content to a file and return the output path"""
        filename = os.path.splitext(os.path.basename(self.filepath))[0] + ".md"
        output_dir = self.output_path or os.getcwd()
        os.makedirs(output_dir, exist_ok=True)

        output_file = os.path.join(output_dir, filename)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)
        return output_file
    
    def convert(self):
        pages = self.extract_content()  # List[PageResult]
        # Save markdown only if output_path is provided
        if self.output_path:
            self.save_markdown(self._markdown)
        return ConversionResult(pages)

