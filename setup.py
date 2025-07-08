from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ks-domain-tagger", 
    version="0.1.0",
    author="Chinmay J S",
    author_email="Chinmay.you.know@gmail.com", 
    description="A tool to find relevant Wikipedia articles for a given paragraph and score them.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/C-you-know/Domain-Tagging-and-Generation", 
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", 
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7', 
    install_requires=[
        "nltk>=3.6",
        "scikit-learn>=1.0",
        "requests>=2.25",
        "beautifulsoup4>=4.9",
        "rapidfuzz>=1.8",
        "numpy>=1.20",
        "termcolor>=1.1.0"
    ],
    entry_points={
        'console_scripts': [
        ],
    },
)
