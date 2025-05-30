<!-- Logo and Title -->
<p align="center">
  <img src="https://img.icons8.com/ios-filled/100/000000/markdown.png" alt="Doctomarkdown Logo" width="100"/>
</p>

<h1 align="center">Doctomarkdown</h1>

---

# Doctomarkdown

**Doctomarkdown** is a robust Python library for converting documents—including PDF, DOCX, PPTX, and CSV—into clean, readable Markdown. It supports extracting text, images, and tables, and is easily extensible for more document types. Advanced extraction is available via LLM (Large Language Model) clients.

---

## Features

- 📄 **Convert PDF, DOCX, PPTX, and CSV to Markdown**
- 🖼️ **Extract images** from documents (optional)
- 📊 **Extract tables** from documents (optional)
- 🤖 **LLM support** : Supports AzureOpenAI, Groq, Gemini, OpenAI, Ollama
- 🗂️ **Extensible**: Add support for more document types
- 🏷️ **Custom output directory**

---

## Installation

```bash
$ pip install doctomarkdown
```

> **Note:** Requires Python 3.10+

---

## Usage Examples

### 1. Convert PDF to Markdown (No LLM)

```python
from doctomarkdown import DocToMarkdown

app = DocToMarkdown()

result = app.convert_pdf_to_markdown(
    filepath="sample_docs/Non-text-searchable.pdf",
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

result = app.convert_pdf_to_markdown(
    filepath="sample_docs/Non-text-searchable.pdf",
    extract_images=True,
    extract_tables=True,
    output_path="markdown_output"
)

for page in result.pages:
    print(f"Page Number: {page.page_number} | Page Content: {page.page_content}")
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

result = app.convert_pdf_to_markdown(
    filepath="sample_docs/Non-text-searchable.pdf",
    extract_images=True,
    extract_tables=True,
    output_path="markdown_output"
)

for page in result.pages:
    print(f"Page Number: {page.page_number} | Page Content: {page.page_content}")
```

### 4. Convert PDF to Markdown using Azure OpenAI Client

```python
from doctomarkdown import DocToMarkdown
from openai import AzureOpenAI
from dotenv import load_dotenv
import os
load_dotenv()

client = AzureOpenAI(
    api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
    api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
)

app = DocToMarkdown(
    llm_client=client,
    llm_model='gpt-4o'
)

result = app.convert_pdf_to_markdown(
    filepath="sample_docs/Non-text-searchable.pdf",
    extract_images=True,
    extract_tables=True,
    output_path="markdown_output"
)

for page in result.pages:
    print(f"Page Number: {page.page_number} | Page Content: {page.page_content}")
```

### 5. Convert PDF to Markdown using Ollama API Client

```python
from doctomarkdown import DocToMarkdown
from openai import OpenAI

ollama_client = OpenAI(
    base_url = 'http://localhost:11434/v1',
    api_key='ollama',
)

app = DocToMarkdown(llm_client=ollama_client, llm_model='gemma3:4b')
result = app.convert_pdf_to_markdown(
    filepath="sample_docs/Non-text-searchable.pdf",
    extract_images=True,
    extract_tables=True,
    output_path="markdown_output"
)

for page in result.pages:
    print(f"Page Number: {page.page_number} | Page Content: {page.page_content}")
```

### 6. Convert PDF to Markdown using OpenAI LLM Client

```python
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

app = DocToMarkdown(llm_client=client, 
                    llm_model='gpt-4o')

result = app.convert_pdf_to_markdown(
    filepath="sample_docs/sample-1.pdf",
    extract_images=True,
    extract_tables=True,
    output_path="markdown_output"
)

for page in result.pages:
    print(f"Page Number: {page.page_number} | Page Content: {page.page_content}")

```
---

### 6. Convert DOCX to Markdown

```python
from doctomarkdown import DocToMarkdown
from dotenv import load_dotenv
load_dotenv()

from groq import Groq


client_groq = Groq(
    # api_key=os.environ.get("GROQ_API_KEY")
)

app = DocToMarkdown(llm_client=client_groq, 
                    llm_model='llama3-8b-8192')

result = app.convert_docx_to_markdown(
    filepath="sample_docs/Sampledoc-1.docx",
    extract_images=True,
    extract_tables=True,
    output_path="markdown_output"
)

for page in result.pages:
    print(f"Page Number: {page.page_number} | Page Content: {page.page_content}")
```

---

### 7. Convert PPTX to Markdown

```python
from doctomarkdown import DocToMarkdown
from dotenv import load_dotenv
load_dotenv()

app = DocToMarkdown()

result = app.convert_pptx_to_markdown(
    filepath="sample_docs/sample-ppt-1.pptx",
    extract_images=True,
    extract_tables=True,
    output_path="markdown_output"
)

for page in result.pages:
    print(f"Page Number: {page.page_number} | Page Content: {page.page_content}")
```

---

### 8. Convert CSV to Markdown

```python
from doctomarkdown import DocToMarkdown

app = DocToMarkdown()

result = app.convert_csv_to_markdown(
    filepath="sample_docs/sample.csv",
    extract_images=True,
    extract_tables=True,
    output_path="markdown_output"
)
```

### 8. Convert URL to Markdown

```python
from doctomarkdown import DocToMarkdown
from dotenv import load_dotenv
load_dotenv()

app = DocToMarkdown()

# Convert Medium article
result = app.convert_url_to_markdown(
    urlpath="https://medium.com/the-ai-forum/build-a-local-reliable-rag-agent-using-crewai-and-groq-013e5d557bcd",
    extract_images=True,
    extract_tables=True,
    output_path="markdown_output"
)

# Display first 500 chars to preview
for page in result.pages:
    print(f"Page Number: {page.page_number}")
    print(f"Content Preview: {page.page_content[:500]}...")
    print(f"Total Length: {len(page.page_content)} characters")
```

---

## License

This project is licensed under the MIT License.