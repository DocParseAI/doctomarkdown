def pdf_to_markdown_system_prompt () -> str:
    return (
            "You are an expert OCR-to-Markdown engine. You must extract every visible detail from images—"
            "including all text, tables, headings, labels, lists, values, units, footnotes, and layout formatting. "
            "Preserve the structure in markdown exactly as seen."
        )

def pdf_to_markdown_user_role_prompt () -> str:
    return  (
            "Extract **every single visible element** from this image into **markdown** format. "
            "Preserve the hierarchy of information using appropriate markdown syntax: headings (#), subheadings (##), bold (**), lists (-), tables, etc. "
            "Include all numerical data, labels, notes, and even seemingly minor text. Do not skip anything. Do not make assumptions."
        )