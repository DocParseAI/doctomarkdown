from doctomarkdown.base import BaseConverter, PageResult, ConversionResult
from typing import Optional
import fitz #PyMuPDF
import os
from doctomarkdown.utils.markdown_helpers import image_bytes_to_base64
import logging

logger = logging.getLogger(__name__)

class PdfToMarkdown(BaseConverter):
    def extract_content(self):
        doc = fitz.open(self.filepath)
        pages = []
        markdown_lines = []
        use_llm = self.llm_client is not None and self.llm_model is not None
        llm_client = self.llm_client
        llm_model = self.llm_model

        for page_number, page in enumerate(doc, 1):
            text = page.get_text("text")
            page_content = text.strip()
            # If LLM client and model are provided, send page image to LLM for markdown extraction
            if use_llm:
                try:
                    pix = page.get_pixmap()
                    base64_image = image_bytes_to_base64(pix.tobytes())
                    response = llm_client.chat.completions.create(
                        model=llm_model,
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "You are an expert OCR-to-Markdown engine. You must extract every visible detail from images—"
                                    "including all text, tables, headings, labels, lists, values, units, footnotes, and layout formatting. "
                                    "Preserve the structure in markdown exactly as seen."
                                )
                            },
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": (
                                            "Extract **every single visible element** from this image into **markdown** format. "
                                            "Preserve the hierarchy of information using appropriate markdown syntax: headings (#), subheadings (##), bold (**), lists (-), tables, etc. "
                                            "Include all numerical data, labels, notes, and even seemingly minor text. Do not skip anything. Do not make assumptions."
                                        )
                                    },
                                    {
                                        "type": "image_url",
                                        "image_url": {"url": f"data:image/png;base64,{base64_image}"}
                                    }
                                ]
                            }
                        ],
                        temperature=0,
                    )
                    page_content = response.choices[0].message.content
                except Exception as e:
                    logger.warning(f"LLM extraction failed for page {page_number}: {e}")
            pages.append(PageResult(page_number, page_content))
            markdown_lines.append(f"## Page {page_number}\n\n{page_content}\n")

            if self.extract_images:
                images = page.get_images(full=True)
                for img_index, img in enumerate(images):
                    xref = img[0]
                    pix = fitz.Pixmap(doc, xref)
                    if pix.n < 5:
                        img_path = f"{self.output_path}/page{page_number}_img{img_index}.png"
                        pix.save(img_path)
                        markdown_lines.append(f"![Image]({img_path})")
                    pix = None

        self._markdown = "\n".join(markdown_lines)
        return pages