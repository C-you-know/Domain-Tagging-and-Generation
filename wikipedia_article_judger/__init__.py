"""
Wikipedia Article Judger Package
--------------------------------

This package provides tools to analyze a given paragraph, find relevant
Wikipedia articles, and score their relevance.
"""

# Import the main function to make it available at the package level
from .judge import judge

# You can also define __all__ to specify what `from wikipedia_article_judger import *` imports
__all__ = ['judge']

# Package version (optional, can also be managed by setup.py or other tools)
__version__ = "0.1.0"
