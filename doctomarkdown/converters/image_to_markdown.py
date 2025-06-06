from doctomarkdown.utils.markdown_helpers import image_bytes_to_base64
from doctomarkdown.utils.content_to_markdown import image_to_markdown_llm, image_to_markdown_ocr
from doctomarkdown.llmwrappers.ExceptionWrapper import handleException
from PIL import Image
from doctomarkdown.base import BaseConverter, PageResult
import logging
import os
import base64

logger = logging.getLogger(__name__)

class ImageToMarkdownConverter(BaseConverter):
    def __init__(self, filepath, extract_images=False, extract_tables=False, output_path=None, llm_client=None, llm_model=None, output_type='markdown', **kwargs):
        super().__init__(filepath=filepath, extract_images=extract_images, extract_tables=extract_tables, output_path=output_path, llm_client=llm_client, llm_model=llm_model, output_type=output_type, **kwargs)
    
    def extract_content(self):
        image = Image.open(self.filepath)
        
        # Read the file for base64 encoding (for the LLM approach)
        with open(self.filepath, "rb") as image_file:
            base64_image =  base64.b64encode(image_file.read()).decode("utf-8")
    
        #base64_image = image_bytes_to_base64(image_bytes)
        logger.info(f"[INFO] Base64 image size: {len(base64_image)} bytes for image {self.filepath}")

        use_llm = self.llm_client is not None
        page_content = ""
        try:
            if use_llm:
                logger.info(f"[INFO] Using LLM extraction for image {self.filepath}")
                llm_result = handleException(
                    max_retry=2,
                    fun=image_to_markdown_llm,
                    fallback_fun=image_to_markdown_ocr,
                    llm_client=self.llm_client,
                    llm_model=self.llm_model,
                    base64_image=base64_image,
                    pix=image,  # Pass the PIL Image for fallback
                    context="image"
                )
                page_content = f"\n{llm_result}"
                logger.info(f"[SUCCESS] LLM extraction successful for image {self.filepath}")
            else:
                # Use OCR directly if no LLM is provided
                page_content = image_to_markdown_ocr(image)
        except Exception as e:
            logger.error(f"[ERROR] Extraction failed for image {self.filepath}: {e}")
            page_content = "[Extraction failed]"

        self._markdown = page_content
        return [PageResult(1, page_content)]