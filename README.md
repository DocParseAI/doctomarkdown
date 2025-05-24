<!-- Logo and Title -->
<p align="center">
  <img src="https://img.icons8.com/ios-filled/100/000000/markdown.png" alt="Doctomarkdown Logo" width="100"/>
</p>

<h1 align="center">Doctomarkdown</h1>

---

# Doctomarkdown

**Doctomarkdown** is a Python library to convert documents (like PDF) into clean, readable Markdown format. It supports extracting text, images, and tables, and is easily extensible for more document types.

---

## Features

- 📄 **Convert PDF to Markdown**
- 🖼️ **Extract images** from documents (optional)
- 📊 **Extract tables** from documents (optional)
- 🤖 **LLM support** for advanced extraction (optional)
- 🗂️ **Extensible**: Add support for DOCX, PPTX, CSV, and more
- 🏷️ **Custom output directory**

---

## Installation

Clone the repository and install in editable mode:

```bash
# Clone the repository
$ git clone <your-repo-url>
$ cd doctomarkdown

# Install dependencies
$ pip install -r requirements.txt

# Install the package in editable mode
$ pip install -e .
```

> **Note:** Requires Python 3.7+

---

## Usage Example

```python
from doctomarkdown.factory import convert_to_markdown

output_path = convert_to_markdown(
    filepath="examples/sample_docs/sample.pdf",
    use_llm=False,
    extract_images=True,
    extract_tables=True,
    output_path="markdown_output"
)

print(f"Markdown saved at: {output_path}")
```

---

## Command Line Example

You can also run the example script:

```bash
python examples/pdf_example.py
```

---

## Supported File Types

- PDF (more coming soon: DOCX, PPTX, CSV)

---

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## License

This project is licensed under the MIT License.