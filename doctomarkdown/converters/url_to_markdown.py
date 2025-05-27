from doctomarkdown.base import BaseConverter, PageResult, ConversionResult
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
        markdown_content = self.html_to_markdown(main_html)

        # Optionally, use LLM for enhanced Markdown conversion
        use_llm = hasattr(self, 'llm_client') and self.llm_client is not None
        try:
            if use_llm and hasattr(self, "generate_markdown_from_text"):
                llm_result = self.generate_markdown_from_text(markdown_content)
                markdown_content = f"\n{llm_result}"
        except Exception as e:
            logger.warning(f"LLM extraction failed for URL: {e}")

        # Use the page title as the Markdown header if available
        title = soup.title.string.strip() if soup.title and soup.title.string else url
        markdown_full = f"# {title}\n\n{markdown_content}\n"

        page_result = PageResult(page_number=1, page_content=markdown_full)
        self._markdown = markdown_full
        return [page_result]

    def html_to_markdown(self, html: str) -> str:
        try:
            import html2text
        except ImportError:
            raise ImportError("Please install 'html2text' to preserve formatting: pip install html2text")
        h = html2text.HTML2Text()
        h.ignore_links = False
        h.ignore_images = False
        h.body_width = 0
        h.protect_links = True
        return h.handle(html)

    def generate_markdown_from_text(self, text: str) -> str:
        """
        Use the LLM client to convert extracted text to enhanced Markdown.
        """
        if hasattr(self.llm_client, "chat"):
            def call_llm():
                return self.llm_client.chat.completions.create(
                    model=self.llm_model,
                    messages=[
                        {"role": "system", "content": "You are an expert at converting web articles to Markdown, preserving all source formatting (headings, lists, code, tables, etc)."},
                        {"role": "user", "content": text}
                    ],
                    temperature=0,
                ).choices[0].message.content
            return call_llm()
        else:
            raise ValueError("Unsupported LLM client type.")