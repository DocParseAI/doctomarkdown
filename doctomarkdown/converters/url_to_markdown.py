from doctomarkdown.base import BaseConverter, PageResult
from doctomarkdown.utils.markdown_helpers import html_to_markdown
from doctomarkdown.utils.content_to_markdown import text_to_markdown_llm, text_to_markdown_fallback
from doctomarkdown.llmwrappers.ExceptionWrapper import handleException
from doctomarkdown.utils.prompts import html_to_markdown_system_role_prompt
from doctomarkdown.utils.site_extractor import extract_medium_article, extract_generic_content, extract_wikipedia_article
from bs4 import BeautifulSoup, Comment
import re
from textwrap import wrap
import requests
import logging

logger = logging.getLogger(__name__)

class UrlToMarkdown(BaseConverter):
    """Converter for web URLs (e.g., Wikipedia, Medium) to Markdown format using LLM or fallback."""

    def extract_content(self):
        url = self.filepath
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
        except Exception as e:
            logger.error(f"Failed to fetch URL: {url} | Error: {e}")
            raise

        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract title
        title_tag = soup.find("title")
        title = ""  # Initialize title
        if title_tag:
            if title_tag.string:  # Check if .string itself is not None
                title = title_tag.string.strip()
            else:
                # If .string is None (e.g., <title><p>text</p></title>), try get_text()
                title = title_tag.get_text(strip=True)
        
        if not title:  # If title is still empty (no title_tag, or empty/None string content)
            # Fallback title logic from URL
            name_parts = [part for part in url.split("/") if part] # Get non-empty parts of the URL path
            if name_parts:
                last_part = name_parts[-1]
                # Remove common extensions if any for a cleaner title
                common_extensions = ['.html', '.htm', '.php', '.aspx', '.jsp', '.asp']
                page_name = last_part
                for ext in common_extensions:
                    if page_name.lower().endswith(ext):
                        page_name = page_name[:-len(ext)]
                        break
                title = page_name.replace('-', ' ').replace('_', ' ').capitalize()
            
            # If title is still empty or only whitespace after URL parsing, set to "Untitled"
            if not title or not title.strip():
                title = "Untitled"

        # Site-specific extraction strategies
        main_html = ""
        if 'medium.com' in url:
            main_html = extract_medium_article(soup)
        elif 'wikipedia.org' in url:
            main_html = extract_wikipedia_article(soup)
        else:
            main_html = extract_generic_content(soup)

        markdown_content = html_to_markdown(main_html)
        
        # If markdown is still empty, fallback to all text
        if not markdown_content or not markdown_content.strip():
            markdown_content = soup.get_text(separator="\n", strip=True)
            
       
        lines = markdown_content.split('\n')
        clean_lines = []
        prev_header = None
        
        for line in lines:
            if line.startswith('#'):
                if line != prev_header:
                    clean_lines.append(line)
                    prev_header = line
            else:
                clean_lines.append(line)
                
        markdown_content = '\n'.join(clean_lines)

        # Check if we have LLM capability and if so, process the first 1000 characters
        use_llm = hasattr(self, 'llm_client') and self.llm_client is not None
        
        if use_llm:
            chunk = markdown_content[:8000]
            try:
                result = handleException(
                    max_retry=2,
                    fun=text_to_markdown_llm,
                    fallback_fun=text_to_markdown_fallback,
                    llm_client=self.llm_client,
                    llm_model=self.llm_model,
                    system_prompt=html_to_markdown_system_role_prompt(),
                    raw_text=chunk,
                    context="url"
                )
                markdown_content = result + '\n' + markdown_content[1000:]
            except Exception as e:
                logger.warning(f"LLM extraction failed for URL chunk: {e}")
        
        # Ensure markdown is never empty
        if not markdown_content.strip():
            markdown_content = soup.get_text(separator="\n", strip=True)

        markdown_full = f"# {title}\n\n{markdown_content}\n"

        page_result = PageResult(page_number=1, page_content=markdown_full)
        self._markdown = markdown_full
        return [page_result]
    
    def split_text(self, text, max_chars=4000):
        """
        Split text into chunks of approximately max_chars.
        This ensures we don't exceed LLM context limits.
        """
        return wrap(text, width=max_chars)
