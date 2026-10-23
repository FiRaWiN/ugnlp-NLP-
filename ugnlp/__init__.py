"""ugnlp — 轻量级维吾尔语 / 中文 NLP 工具集 (pure Python, zero dependencies)."""

from .translit import to_latin, to_arabic
from .tokenizer import split_words, split_suffixes, split_sentences
from .glossary import Glossary
from .numbers import convert_digits

__version__ = "0.1.0"

__all__ = [
    "to_latin",
    "to_arabic",
    "split_words",
    "split_suffixes",
    "split_sentences",
    "Glossary",
    "convert_digits",
    "__version__",
]
