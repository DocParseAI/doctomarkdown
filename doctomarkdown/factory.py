import os
from doctomarkdown.converters.pdf_to_markdown import PdfToMarkdown
# Future Converters can be imported similarly

from doctomarkdown.base import BaseConverter

def get_converter_class(extension: str):
    """Returns appropiate converted class for a given extension"""
    ext = extension.lower()

    if ext == ".pdf":
        return PdfToMarkdown
    # elif ext == ".csv":
    #     return CsvToMarkdown

    raise ValueError(f"Unsupported file format: {ext}")

def convert_to_markdown(
        filepath:str,
        use_llm: bool = False,
        extract_images: bool = False,
        extract_tables: bool = False,
        output_path: str = None,
        **kwargs
) -> str:
    ext = os.path.splitext(filepath)[1]
    ConverterClass = get_converter_class(ext)

    converter: BaseConverter = ConverterClass(
        filepath=filepath,
        use_llm=use_llm,
        extract_images=extract_images,
        extract_tables=extract_tables,
        output_path=output_path,
        **kwargs
    )

    return converter.convert()