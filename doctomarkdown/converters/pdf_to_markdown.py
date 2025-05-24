from doctomarkdown.base import BaseConverter, PageResult, ConversionResult
from typing import Optional
import fitz #PyMuPDF


class PdfToMarkdown(BaseConverter):
    def extract_content(self):
        doc = fitz.open(self.filepath)
        pages = []
        markdown_lines = []

        for page_number, page in enumerate(doc, 1):
            text = page.get_text("text")
            page_content = text.strip()
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