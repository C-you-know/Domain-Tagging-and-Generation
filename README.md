[![PyPI version](https://badge.fury.io/py/ks-domain-tagger.svg)](https://pypi.org/project/ks-domain-tagger/)
[![Python Versions](https://img.shields.io/pypi/pyversions/ks-domain-tagger.svg)](https://pypi.org/project/ks-domain-tagger/)


# KS Domain Tagger

A Python tool to analyze a given paragraph, identify relevant Wikipedia articles, and score their relevance. It uses keyword extraction, Wikipedia API searches, and fuzzy string matching to determine the most appropriate articles.

## Features

*   **Keyword Extraction**: Identifies key terms, bigrams, and trigrams from the input text using TF-IDF and NLTK.
*   **Wikipedia Integration**: Searches Wikipedia for articles based on extracted keywords.
*   **Content Fetching**: Retrieves textual content (paragraphs) from Wikipedia articles.
*   **Relevance Scoring**: Compares the input paragraph with Wikipedia content using fuzzy matching (`rapidfuzz`) and normalizes scores using softmax.
*   **Two-Pass Search (Optional)**: Can perform a second pass by exploring links from initially matched Wikipedia pages for a more comprehensive search.
*   **Paragraph Validation**: Checks input paragraph length and cleans it by removing stop words.

## Installation

```bash
pip install ks-domain-tagger
```

## Usage

To use the `judge` function, you can import it into your Python script:

```python
from ks_domain_tagger import judge # Assuming __init__.py makes judge available

paragraph_to_analyze = """
Manmohan Singh, an economist and politician, served as the 13th Prime Minister of India
from 2004 to 2014. Renowned for his role in the economic reforms of the 1990s, Singh
was instrumental in steering the country toward liberalization, fostering economic growth,
and enhancing India's global standing. His tenure as Finance Minister in 1991, during a
time of economic crisis, marked a pivotal moment in India's transformation, with bold
measures such as trade liberalization, reducing government control, and encouraging
foreign investment. A man of humility and intellect, Singh's leadership was marked by
pragmatism and caution. He is widely respected for his integrity and efforts to balance
economic growth with social development. Despite his relatively low-key personality,
Manmohan Singh’s impact on India’s economic landscape remains indelible, solidifying his
legacy as a key architect of modern India’s economic foundation.
"""

# Basic usage
results = judge.judge(paragraph_to_analyze)
print(results)

# Usage with second pass and different thresholds
results_pass2 = judge.judge(
    para=paragraph_to_analyze,
    threshold=50,        # Initial similarity threshold for pass 1
    pass2=True,          # Enable second pass
    threshold2=53,       # Similarity threshold for pass 2
    visit_all_pages=False # For pass 2, only search links in summary sections
)
print(results_pass2)
```

The `judge` function returns a dictionary where keys are the titles of relevant Wikipedia articles and values are their softmax scores indicating relevance.

## Dependencies

The project relies on the following Python libraries:

*   `nltk>=3.6`
*   `scikit-learn>=1.0`
*   `requests>=2.25`
*   `beautifulsoup4>=4.9`
*   `rapidfuzz>=1.8`
*   `numpy>=1.20`
*   `termcolor>=1.1.0` (primarily for `test.py`)

These will be handled automatically if installing via pip from PyPI.

## How It Works

1.  **Input & Validation**: The input paragraph is validated for length and cleaned by removing common stop words.
2.  **Keyword Extraction**: Keywords (single words, bigrams, trigrams) are extracted using TF-IDF and NLTK.
3.  **Wikipedia Search (Pass 1)**: Keywords are used to find relevant articles via the Wikipedia API.
4.  **Content Fetching (Pass 1)**: Content from these articles is downloaded.
5.  **Scoring (Pass 1)**: The input paragraph is compared against fetched Wikipedia paragraphs using `rapidfuzz`. Scores are normalized using softmax.
6.  **Wikipedia Search (Pass 2 - Optional)**: If enabled, links from the top articles found in Pass 1 are explored to find more potentially relevant articles.
7.  **Content Fetching & Scoring (Pass 2 - Optional)**: Content from these new articles is fetched and scored similarly.
8.  **Output**: The system outputs a list of relevant Wikipedia titles and their relevance scores.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.