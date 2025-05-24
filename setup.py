from setuptools import setup, find_packages

setup(
    name='doctomarkdown',
    version='0.1',
    packages=find_packages(),
    author='docparseai',
    install_requires = [
        'PyMuPDF'
    ],
    description='Convert documents liek PDF to Markdown',
)