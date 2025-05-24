from doctomarkdown.base import BaseConverter
from typing import Optional
import fitz #PyMuPDF


class PdfToMarkdown(BaseConverter):
    def extract_content(self) -> str:
        doc = fitz.open(self.filepath)
        markdown_lines = []

        for page_number, page in enumerate(doc, 1):
            text = page.get_text("text")
            markdown_lines.append(f"## Page {page_number}\n\n{text.strip()}\n")

            if self.extract_images:
                images = page.get_images(full=True)
                for img_index, img in enumerate(images):
                    xref = img[0]
                    pix = fitz.Pixmap(doc, xref)
                    if pix.n < 5: #If this is GRAY or RGB
                        pix.save(f"{self.output_path}/page{page_number}_img{img_index}.png")
                        markdown_lines.append(f"![Image] (page{page_number}_img{img_index}.png)")
                    pix = None
                
        return "\n".join(markdown_lines)