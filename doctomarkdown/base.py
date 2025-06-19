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
        system_prompt: Optional[str] = None,
        user_prompt_template: Optional[str] = None,
        output_type: str = 'markdown',
        **kwargs: Any
    ):
        self.filepath = filepath
        self.extract_images = extract_images
        self.extract_tables = extract_tables
        self.output_path = output_path
        self.llm_client = llm_client
        self.llm_model = llm_model
        self.llm_prompt = llm_prompt
        self.system_prompt = system_prompt or "You are a helpful assistant that summarizes content into markdown."
        self.user_prompt_template = user_prompt_template or "Summarize the following content:\n\n{content}"
        self.output_type = output_type
        self.kwargs = kwargs #for future extension
    
    @abstractmethod
    def extract_content(self) -> str:
        """Extract Contents and return it in markdown format"""
        pass

    def save_markdown(self, content: str) -> str:
        """Save the markdown/text content to a file and return the output path"""
        ext = '.md' if getattr(self, 'output_type', 'markdown') == 'markdown' else '.txt'
        filename = os.path.splitext(os.path.basename(self.filepath))[0] + ext
        output_dir = self.output_path or os.getcwd()
        os.makedirs(output_dir, exist_ok=True)

        output_file = os.path.join(output_dir, filename)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)
        return output_file
    def call_llm(self, content: str) -> Optional[str]:
        if not self.llm_client or not self.llm_model:
            return None
        try:
            prompt = self.user_prompt_template.format(content=content)
            response = self.llm_client.chat.completions.create(
                model=self.llm_model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"[LLM ERROR] Failed to get response: {e}")
            return None
        
    def convert(self) -> ConversionResult:
        pages = self.extract_content()
        full_content = "\n\n".join([p.page_content for p in pages])
        self._markdown = full_content  # Save raw extracted text/markdown

        llm_summary = self.call_llm(full_content)
        if self.output_path:
            self.save_markdown(full_content)

        return ConversionResult(pages=pages, llm_summary=llm_summary)
