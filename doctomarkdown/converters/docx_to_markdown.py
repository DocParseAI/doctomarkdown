from doctomarkdown.base import BaseConverter, PageResult
from doctomarkdown.converters.pdf_to_markdown import PdfToMarkdown
from docx2pdf import convert as docx2pdf_convert
import tempfile
import os
import shutil
import logging

logger = logging.getLogger(__name__)

class DocxToMarkdown(BaseConverter):
    """Converter for DOCX files to Markdown format using LLM or fallback."""

    def __init__(
        self,
        filepath,
        extract_images=False,
        extract_tables=False,
        output_path=None,
        llm_client=None,
        llm_model=None,
        system_prompt=None,
        user_prompt_template=None,
        output_type='markdown',
        **kwargs
    ):
        super().__init__(
            filepath=filepath,
            extract_images=extract_images,
            extract_tables=extract_tables,
            output_path=output_path,
            llm_client=llm_client,
            llm_model=llm_model,
            output_type=output_type,
            **kwargs
        )
        self.system_prompt = system_prompt or "You are a helpful assistant that converts DOCX documents into Markdown."
        self.user_prompt_template = user_prompt_template or "Convert the following document content into Markdown:\n\n{content}"

    def extract_content(self):
        temp_dir = tempfile.mkdtemp()
        try:
            input_docx = self.filepath
            output_pdf = os.path.join(temp_dir, os.path.splitext(os.path.basename(input_docx))[0] + ".pdf")

            # Convert DOCX to PDF
            docx2pdf_convert(input_docx, output_pdf)

            if not os.path.exists(output_pdf):
                raise FileNotFoundError(f"PDF not found after DOCX to PDF conversion: {output_pdf}")

            # Use PdfToMarkdown to extract
            pdf_converter = PdfToMarkdown(
                filepath=output_pdf,
                llm_client=self.llm_client,
                llm_model=self.llm_model,
                system_prompt=self.system_prompt,
                user_prompt_template=self.user_prompt_template,
                extract_images=self.extract_images,
                extract_tables=self.extract_tables,
                output_path=None,
                output_type=self.output_type,
            )

            pages = pdf_converter.extract_content()
            self._markdown = getattr(pdf_converter, "_markdown", None)
            logger.info(f"[SUCCESS] Extracted content from DOCX via PDF: {self.filepath}")
            return pages

        except Exception as e:
            logger.error(f"[ERROR] DOCX extraction failed: {e}")
            raise
        finally:
            shutil.rmtree(temp_dir)

    def call_llm(self, content):
        if not self.llm_client or not self.llm_model:
            raise ValueError("LLM client or model not provided.")
        
        prompt = self.user_prompt_template.format(content=content)
        try:
            response = self.llm_client.chat.completions.create(
                model=self.llm_model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"[LLM ERROR] Failed to call LLM: {e}")
            raise
