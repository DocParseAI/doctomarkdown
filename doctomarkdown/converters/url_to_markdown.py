from doctomarkdown.base import BaseConverter, PageResult, ConversionResult
from doctomarkdown.utils.markdown_helpers import html_to_markdown
from doctomarkdown.utils.markdown_helpers import generate_markdown_from_text
from bs4 import BeautifulSoup
import requests
import logging

logger = logging.getLogger(__name__)

class UrlToMarkdown(BaseConverter):
    """
    Converter for web URLs (e.g., Wikipedia, Medium) to Markdown format.
    Extracts main article content and converts it to Markdown, preserving source formatting.
    """

    def extract_content(self):
        url = self.filepath
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
        except Exception as e:
            logger.error(f"Failed to fetch URL: {url} | Error: {e}")
            raise

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract the main content block
        main_block = None
        if "wikipedia.org" in url:
            main_block = soup.find("div", id="bodyContent")
        elif "medium.com" in url:
            main_block = soup.find("article")
        else:
            main_block = soup.find("article") or soup.find("main")
            if not main_block:
                # Fallback: wrap all <p> tags in a div
                paragraphs = soup.find_all("p")
                wrapper = soup.new_tag("div")
                for p in paragraphs:
                    wrapper.append(p)
                main_block = wrapper

        # Convert HTML to Markdown, preserving formatting
        main_html = str(main_block) if main_block else ""
        markdown_content = html_to_markdown(main_html)

        # Optionally, use LLM for enhanced Markdown conversion
        use_llm = hasattr(self, 'llm_client') and self.llm_client is not None
        try:
            if use_llm:
                llm_result = generate_markdown_from_text(
                    self.llm_client,
                    self.llm_model,
                    markdown_content,
                    "You are an expert at converting web articles to Markdown, preserving all source formatting (headings, lists, code, tables, etc)."
                )
                markdown_content = f"\n{llm_result}"
        except Exception as e:
            logger.warning(f"LLM extraction failed for URL: {e}")

        # Use the page title as the Markdown header if available
        title = soup.title.string.strip() if soup.title and soup.title.string else url
        markdown_full = f"# {title}\n\n{markdown_content}\n"

        page_result = PageResult(page_number=1, page_content=markdown_full)
        self._markdown = markdown_full
        return [page_result]