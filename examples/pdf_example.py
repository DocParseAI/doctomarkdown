from doctomarkdown.factory import convert_to_markdown

output_path = convert_to_markdown(
    filepath="examples/sample_docs/sample.pdf",
    use_llm=False,
    extract_images=False,
    extract_tables=False,
    output_path = "markdown_output"
)

print(f"Markdown saved at: {output_path}")