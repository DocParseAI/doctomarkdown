<!-- Logo, Title, and Badges -->
<p align="center">
    <img src="https://img.icons8.com/ios-filled/100/000000/markdown.png" alt="Doctomarkdown Logo" width="100"/>
</p>

<h1 align="center">🚀 Doctomarkdown</h1>

<p align="center">
    <a href="https://pypi.org/project/doctomarkdown/">
        <img src="https://img.shields.io/pypi/v/doctomarkdown.svg?label=Latest%20Release&logo=pypi&logoColor=white" alt="PyPI Version"/>
    </a>
    <img src="https://img.shields.io/badge/pip%20install-doctomarkdown-blue?logo=python&logoColor=white" alt="PyPI - Install"/>
    <img src="https://img.shields.io/pypi/dm/doctomarkdown?label=Downloads&logo=download&logoColor=white" alt="PyPI - Downloads"/>
    <img src="https://img.shields.io/github/license/docparseai/doctomarkdown?label=License&logo=github" alt="License"/>
</p>

<p align="center">
    <b>Convert PDFs, DOCX, PPTX, CSV, images, and URLs to clean, readable Markdown in seconds!</b><br>
    <em>Now with LLM-powered extraction, image & table support, and blazing-fast performance.</em>
</p>

---

# ✨ What's New

- **[v0.2.0](https://pypi.org/project/doctomarkdown/)** (2025-06):  
    - 🖼️ Improved image extraction for PDFs and DOCX  
    - 🤖 Enhanced LLM support: Gemini, Groq, Ollama  
    - 🏷️ Custom output directory and file type  
    - 🐍 Python 3.10+ compatibility  
    - ⚡ Performance and stability improvements

---

# Doctomarkdown

**Doctomarkdown** is a robust Python library for converting documents—including PDF, DOCX, PPTX, CSV, images, and URLs—into clean, readable Markdown. It supports extracting text, images, and tables, and is easily extensible for more document types. Advanced extraction is available via LLM (Large Language Model) clients.

---

## Features

- 📄 **Convert PDF, DOCX, PPTX, CSV, URL, and Images to Markdown**
- 🖼️ **Extract images** from documents (optional)
- 📊 **Extract tables** from documents (optional)
- 🤖 **LLM support**: Azure OpenAI, OpenAI, Groq, Gemini, Ollama
- 🗂️ **Extensible**: Add support for more document types
- 🏷️ **Custom output directory**

---

## Supported File Types

| File Type | Function Name                  | Example File Extension |
|-----------|-------------------------------|-----------------------|
| PDF       | `convert_pdf_to_markdown`      | `.pdf`                |
| DOCX      | `convert_docx_to_markdown`     | `.docx`               |
| PPTX      | `convert_pptx_to_markdown`     | `.pptx`               |
| CSV       | `convert_csv_to_markdown`      | `.csv`                |
| Image     | `convert_image_to_markdown`    | `.png`, `.jpg`, `.jpeg`|
| URL       | `convert_url_to_markdown`      | (web link)            |

---

## Supported LLM Clients

| LLM Client      | How to Initialize |
|-----------------|-------------------|
| **OpenAI**      | See below         |
| **Azure OpenAI**| See below         |
| **Groq**        | See below         |
| **Gemini**      | See below         |
| **Ollama**      | See below         |

**OpenAI**
```python
from openai import OpenAI
client = OpenAI(api_key="your-api-key")
```

**Azure OpenAI**
```python
from openai import AzureOpenAI
client = AzureOpenAI(
    api_key="your-api-key",
    azure_endpoint="https://your-resource-name.openai.azure.com/",
    api_version="2023-05-15"
)
```

**Groq**
```python
from groq import Groq
client = Groq(api_key="your-api-key")
```

**Gemini**
```python
import google.generativeai as genai
genai.configure(api_key="your-api-key")
client = genai.GenerativeModel("gemini-pro")
```

**Ollama**
```python
from openai import OpenAI
client = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama')
```

---

## Installation

```bash
pip install doctomarkdown
```
> **Note:** Requires Python 3.10+

---

## Basic Usage

Below is the main usage pattern with the specific function to call for each file type:

```python
from doctomarkdown import DocToMarkdown
# Import and initialize your LLM client if needed (see table above)

app = DocToMarkdown(
    llm_client=client,        # Optional: pass your LLM client here
    llm_model='your-model'    # Optional: pass your LLM model name
)

# Choose the appropriate function for your file type:
# PDF:   app.convert_pdf_to_markdown()
# DOCX:  app.convert_docx_to_markdown()
# PPTX:  app.convert_pptx_to_markdown()
# CSV:   app.convert_csv_to_markdown()
# Image: app.convert_image_to_markdown()
# URL:   app.convert_url_to_markdown()

result = app.convert_pdf_to_markdown(  # Change function based on file type
    filepath="path/to/your/file.pdf",  # Change extension based on file type
    extract_images=True,      # Optional
    extract_tables=True,      # Optional
    output_path="markdown_output",  # Optional
    output_type="markdown"   # or 'text' for .txt output
)

for page in result.pages:
    print(f"Page Number: {page.page_number} | Page Content: {page.page_content}")
```

---

## Examples: Using OpenAI Client for All File Types

### 1. PDF to Markdown
```python
from openai import OpenAI
from doctomarkdown import DocToMarkdown
import os
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
app = DocToMarkdown(llm_client=client, llm_model='gpt-4o')

result = app.convert_pdf_to_markdown(
    filepath="sample_docs/sample-1.pdf",
    extract_images=True,
    extract_tables=True,
    output_path="markdown_output",
    output_type="markdown"
)
for page in result.pages:
    print(f"Page Number: {page.page_number} | Page Content: {page.page_content}")
```

### 2. DOCX to Markdown
```python
from openai import OpenAI
from doctomarkdown import DocToMarkdown
import os
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
app = DocToMarkdown(llm_client=client, llm_model='gpt-4o')

result = app.convert_docx_to_markdown(
    filepath="sample_docs/sample_document.docx",
    extract_images=True,
    extract_tables=True,
    output_path="markdown_output",
    output_type="markdown"
)
for page in result.pages:
    print(f"Page Number: {page.page_number} | Page Content: {page.page_content}")
```

### 3. PPTX to Markdown
```python
from openai import OpenAI
from doctomarkdown import DocToMarkdown
import os
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
app = DocToMarkdown(llm_client=client, llm_model='gpt-4o')

result = app.convert_pptx_to_markdown(
    filepath="sample_docs/sample_ppt_2.pptx",
    extract_images=True,
    extract_tables=True,
    output_path="markdown_output",
    output_type="markdown"
)
for page in result.pages:
    print(f"Page Number: {page.page_number} | Page Content: {page.page_content}")
```

### 4. CSV to Markdown
```python
from openai import OpenAI
from doctomarkdown import DocToMarkdown
import os
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
app = DocToMarkdown(llm_client=client, llm_model='gpt-4o')

result = app.convert_csv_to_markdown(
    filepath="sample_docs/sample.csv",
    extract_images=True,
    extract_tables=True,
    output_path="markdown_output",
    output_type="markdown"
)
for page in result.pages:
    print(f"Page Number: {page.page_number} | Page Content: {page.page_content}")
```

### 5. Image to Markdown
```python
from openai import OpenAI
from doctomarkdown import DocToMarkdown
import os
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
app = DocToMarkdown(llm_client=client, llm_model='gpt-4o')

result = app.convert_image_to_markdown(
    filepath="sample_docs/sample_image.png",
    extract_images=True,
    extract_tables=True,
    output_path="markdown_output",
    output_type="text"
)
for page in result.pages:
    print(f"Page Number: {page.page_number} | Page Content: {page.page_content}")
```

### 6. URL to Markdown
```python
from openai import OpenAI
from doctomarkdown import DocToMarkdown
import os
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
app = DocToMarkdown(llm_client=client, llm_model='gpt-4o')

result = app.convert_url_to_markdown(
    urlpath="https://medium.com/the-ai-forum/build-a-local-reliable-rag-agent-using-crewai-and-groq-013e5d557bcd",
    extract_images=True,
    extract_tables=True,
    output_path="markdown_output",
    output_type="markdown"
)
for page in result.pages:
    print(f"Page Number: {page.page_number}")
    print(f"Content Preview: {page.page_content[:500]}...")
    print(f"Total Length: {len(page.page_content)} characters")
```

---

## License

This project is licensed under the MIT License.