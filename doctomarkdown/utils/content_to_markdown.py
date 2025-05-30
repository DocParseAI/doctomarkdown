from doctomarkdown.utils.prompts import pdf_to_markdown_system_prompt, pdf_to_markdown_user_role_prompt,docx_to_markdown_system_role_prompt,docx_to_markdown_user_role_prompt
from doctomarkdown.llmwrappers.GeminiWrapper import GeminiVisionWrapper
from PIL import Image
import pytesseract

def image_to_markdown_llm(llm_client, llm_model, base64_image: str) -> str:
    """
    Convert an image (base64-encoded) to markdown using the provided LLM client and model.
    Supports Gemini and Groq-style clients.
    """
    if not llm_model and hasattr(llm_client, 'model_name') and "gemini" in llm_client.model_name:
        from PIL import Image
        import io
        import base64
        gemini_client = GeminiVisionWrapper(llm_client)
        image_data = base64.b64decode(base64_image)
        image = Image.open(io.BytesIO(image_data))
        response = gemini_client.generate_content([
            {"text": pdf_to_markdown_system_prompt()},
            {"text": pdf_to_markdown_user_role_prompt()},
            image
        ])
        return response.text
    elif hasattr(llm_client, "chat"):
        def call_groqai():
            return llm_client.chat.completions.create(
                model=llm_model,
                messages=[
                    {"role": "system", "content": pdf_to_markdown_system_prompt()},
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": pdf_to_markdown_user_role_prompt()},
                            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
                        ]
                    }
                ],
                temperature=0,
            ).choices[0].message.content
        return call_groqai()
    else:
        raise ValueError("Unsupported LLM client type.")

def image_to_markdown_ocr(pix) -> str:
    """
    Convert an image to markdown text using OCR (pytesseract).
    Accepts a PIL Image object.
    """
    mode = "RGB" if pix.n < 4 else "RGBA"
    img = Image.frombytes(mode, (pix.width, pix.height), pix.samples)
    # Use pytesseract for OCR
    text = pytesseract.image_to_string(img)
    return text.strip() if text.strip() else "[No text found by OCR]"

def text_to_markdown_llm(llm_client, llm_model, system_prompt, raw_text):
    # LLM function to convert docx file into markdown
    if hasattr(llm_client, "generate_content"):  # Gemini's method
        response = llm_client.generate_content(
            [  
                docx_to_markdown_system_role_prompt(),
                raw_text
            ]
        )
        return response.text
    elif hasattr(llm_client.chat, "completions"):  # OpenAI-like fallback
        return llm_client.chat.completions.create(
            model=llm_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": [
                    # {"type":"text", "text": docx_to_markdown_user_role_prompt()},
                    {"type":"text", "text": raw_text}
                ]}
            ],
            temperature=0,
        ).choices[0].message.content
    else:
        raise ValueError("Unsupported LLM client")
    
def text_to_markdown_fallback(raw_text):
    # Basic fallback for docx to markdown: just return as-is or wrap in code block
    return f"```\n{raw_text}\n```"
