from doctomarkdown.factory import convert_to_markdown

result = convert_to_markdown(
    filepath="examples/sample_docs/sample.pdf",
    use_llm=False,
    extract_images=True,
    extract_tables=True,
    output_path="markdown_output"
)

for page in result.pages:
    print(f"Page Number: {page.page_number} | Page Content: {page.page_content}")