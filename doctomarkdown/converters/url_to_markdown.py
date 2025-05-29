from doctomarkdown.base import BaseConverter, PageResult
from doctomarkdown.utils.markdown_helpers import html_to_markdown
from doctomarkdown.utils.content_to_markdown import text_to_markdown_llm, text_to_markdown_fallback
from doctomarkdown.llmwrappers.ExceptionWrapper import handleException
from bs4 import BeautifulSoup
from textwrap import wrap
import requests
import logging

logger = logging.getLogger(__name__)

class UrlToMarkdown(BaseConverter):
    """Converter for web URLs (e.g., Wikipedia, Medium) to Markdown format using LLM or fallback."""

    def extract_content(self):
        url = self.filepath
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
        except Exception as e:
            logger.error(f"Failed to fetch URL: {url} | Error: {e}")
            raise

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract the main content block based on domain-specific structure
        main_block = None
        if "wikipedia.org" in url:
            main_block = soup.find("div", id="bodyContent")
        elif "medium.com" in url:
            main_block = soup.find("article")
        else:
            main_block = soup.find("article") or soup.find("main")
            if not main_block:
                paragraphs = soup.find_all("p")
                wrapper = soup.new_tag("div")
                for p in paragraphs:
                    wrapper.append(p)
                main_block = wrapper

        main_html = str(main_block) if main_block else ""
        markdown_content = html_to_markdown(main_html)
        chunks = self.split_text(markdown_content, max_tokens=6000)
        llm_outputs = []
        use_llm = hasattr(self, 'llm_client') and self.llm_client is not None

        for chunk in chunks:
            try:
                if use_llm:
                    result = handleException(
                        max_retry=2,
                        fun=text_to_markdown_llm,
                        fallback_fun=text_to_markdown_fallback,
                        llm_client=self.llm_client,
                        llm_model=self.llm_model,
                        content=chunk,
                        context="url"
                    )
                    llm_outputs.append(result)
                    
            except Exception as e:
                logger.warning(f"LLM extraction failed for URL: {e}")
        markdown_content = f"{"\n\n".join(llm_outputs)}"
        title = soup.title.string.strip() if soup.title and soup.title.string else url
        markdown_full = f"# {title}\n\n{markdown_content}\n"

        page_result = PageResult(page_number=1, page_content=markdown_full)
        self._markdown = markdown_full
        return [page_result]
    
    def split_text(self,text, max_tokens=8000):
        """
        Roughly split text into chunks under max_tokens.
        This assumes ~4 characters per token as a heuristic.
        """
        chunk_size = max_tokens * 4  # crude estimate
        return wrap(text, width=chunk_size)
