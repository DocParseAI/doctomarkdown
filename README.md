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
$ git clone https://github.com/DocParseAI/doctomarkdown.git
$ cd doctomarkdown

# Install dependencies
$ pip install -r requirements.txt

# Install the package in editable mode
$ pip install -e .
```

> **Note:** Requires Python 3.10+

---

## Usage Example

### 1. Convert PDF to Markdown (No LLM)

```python
from doctomarkdown import DocToMarkdown

app = DocToMarkdown()

result = app.convert_pdf_to_markdown(
    filepath="sample_docs/sample.pdf",
    extract_images=True,
    extract_tables=True,
    output_path="markdown_output"
)

for page in result.pages:
    print(f"Page Number: {page.page_number} | Page Content: {page.page_content}")
```

### 2. Convert PDF to Markdown using Groq LLM Client

```python
from groq import Groq
from doctomarkdown import DocToMarkdown
from dotenv import load_dotenv
import os
load_dotenv()

client_groq = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

app = DocToMarkdown(
    llm_client=client_groq,
    llm_model='meta-llama/llama-4-scout-17b-16e-instruct'
)
```

### 3. Convert PDF to Markdown using Gemini LLM Client

```python
from google import genai
from dotenv import load_dotenv
import os
load_dotenv()
import google.generativeai as genai
from doctomarkdown import DocToMarkdown

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
vision_model = genai.GenerativeModel("gemini-1.5-flash")  # Choose your Gemini Vision model

app = DocToMarkdown(
    llm_client=vision_model
)
```

### 4. Convert PDF to Markdown using AzureOpenAI Client

```python
from openai import AzureOpenAI
from dotenv import load_dotenv
load_dotenv()

clinet = AzureOpenAI(
    api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
    api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
)

app = DocToMarkdown(llm_client=clinet, 
                    llm_model='gpt-4o')
```

### 5. Convert PDF to Markdown using Ollama Client

```python
from openai import OpenAI

ollama_client = OpenAI(
    base_url = 'http://localhost:11434/v1',
    api_key='ollama',
)

app = DocToMarkdown(llm_client=ollama_client, 
                    llm_model='gemma3:4b')
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

## File Structure

```
doctomarkdown/
├── base.py
├── factory.py
├── __init__.py
├── converters/
│   ├── pdf_to_markdown.py
│   ├── docx_to_markdown.py
│   ├── pptx_to_markdown.py
│   ├── csv_to_markdown.py
│   └── __init__.py
├── utils/
│   ├── markdown_helpers.py
│   └── __init__.py
examples/
├── pdf_example.py
├── sample_docs/
│   └── sample.pdf
markdown_output/
├── sample.md
setup.py
requirements.txt
README.md
LICENSE
```

---

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## License

This project is licensed under the MIT License.