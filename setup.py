from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="wikipedia_article_judger", # Replace with your own username
    version="0.1.0",
    author="Your Name", # Replace with your name
    author_email="your.email@example.com", # Replace with your email
    description="A tool to find relevant Wikipedia articles for a given paragraph and score them.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/wikipedia_article_judger", # Replace with your project's URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", # Assuming MIT License, update if different
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7', # Based on f-strings and type hints, Python 3.7+ is a safe bet
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
            # If you want a command-line interface, define it here
            # 'wikijudge=wikipedia_article_judger.judge:main_cli_function', # Example
        ],
    },
)
