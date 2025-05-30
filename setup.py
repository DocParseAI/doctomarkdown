from setuptools import setup, find_packages
import os

# Read the content of README.md file
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='doctomarkdown',
    version='0.1.7',
    packages=find_packages(),
    author='docparseai',
    author_email='sayantanghosh.work@gmail.com',
    description='Convert documents to Markdown',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/DocParseAI/doctomarkdown',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.10',
    install_requires=[
        'PyMuPDF',
        'Pillow',
        'pytesseract',
        'typing-extensions',
        'python-docx',
        'python-pptx',
        'pandas',
        'tabulate',
        'html2text',
        'beautifulsoup4'
    ],
    extras_require={
        'llm': [
            'google-generativeai',
            'pytesseract'
        ],
    },
)






