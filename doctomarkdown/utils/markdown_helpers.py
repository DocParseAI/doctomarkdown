import base64
from typing import BinaryIO
import html2text
from bs4 import BeautifulSoup

def image_file_to_base64(image_path: str) -> str:
    """
    Read an image file and return its base64-encoded string.
    """
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

def image_bytes_to_base64(image_bytes: bytes) -> str:
    """
    Convert image bytes to base64 string.
    """
    return base64.b64encode(image_bytes).decode("utf-8")

def html_to_markdown(html: str) -> str:
    """
    Convert HTML to Markdown while preserving formatting using html2text.
    """
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = False
    h.body_width = 0
    h.protect_links = True
    return h.handle(html)

def generate_markdown_from_text(llm_client, llm_model, text: str, system_prompt: str) -> str:
    """
    Use the LLM client to convert extracted text to enhanced Markdown.
    """
    if hasattr(llm_client, "chat"):
        def call_llm():
            return llm_client.chat.completions.create(
                model=llm_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text}
                ],
                temperature=0,
            ).choices[0].message.content
        return call_llm()
    else:
        raise ValueError("Unsupported LLM client type.")