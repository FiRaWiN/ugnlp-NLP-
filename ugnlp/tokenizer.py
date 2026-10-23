"""Uyghur word/sentence segmentation and rule-based morphological suffix splitting.

Uyghur is an agglutinative Turkic language: suffixes stack onto a stem
(e.g.  ئۆي  "house" ->  ئۆيلەر  "houses" ->  ئۆيلەرنىڭ  "of the houses").
This module does a greedy longest-suffix split from the right, which is a
useful first pass for keyword extraction and search normalization.
"""

from __future__ import annotations

import re

_SENTENCE_RE = re.compile(r"(?<=[.!?؟۔—])\s+")

# Common inflectional suffixes (Arabic script), longest first.
# Not exhaustive — a curated list covering the most frequent cases.
_SUFFIXES_UG = [
    "لىرىدىكى", "لىرىمۇ", "لىرىغا", "لىرىنى", "لىرىدە", "لىرىدىن",
    "دىكىلەر", "تىكىلەر",
    "لىرى", "دىكى", "تىكى", "مۇشمۇ", "دىمۇ",
    "لارغا", "لەرگە", "لارنى", "لەرنى", "لاردا", "لەردە",
    "لاردىن", "لەردىن", "لارمۇ", "لەرمۇ",
    "دىمۇ", "تىمۇ", "دىنمۇ", "تىنمۇ",
    "غا", "قا", "گە", "كە", "نى", "نىڭ", "نىكى",
    "دا", "دە", "تا", "تە", "دىن", "تىن", "دۇن", "دۈن",
    "لار", "لەر", "مۇ", "مۇ", "شۇ", "يا",
]

# Same suffixes in Latin (ULY) form, longest first.
_SUFFIXES_LATIN = [
    "liridiki", "lirimu", "lirigha", "lirini", "liridé", "liridin",
    "dikilär",
    "liri", "diki", "tiki",
    "largha", "lärge", "larni", "lärni", "larda", "lärdä",
    "lardin", "lärdin", "larmu", "lärmu",
    "dimu", "timu", "dinmu", "tinmu",
    "gha", "qa", "gé", "ké", "ni", "ning", "niki",
    "da", "dä", "ta", "tä", "din", "tin", "dun", "dün",
    "lar", "lär", "mu", "shu", "ya",
]


def split_sentences(text: str) -> list[str]:
    """Split text into sentences (supports . ! ? and Arabic-script .؟ !)."""
    parts = _SENTENCE_RE.split(text.strip())
    return [p for p in (s.strip() for s in parts) if p]


def split_words(text: str) -> list[str]:
    """Whitespace/punctuation word tokenization for Arabic or Latin script."""
    text = re.sub(r"[،؛«»]", " ", text)
    return [w for w in re.split(r"\s+", text) if w]


def _split_suffixes_word(word: str, suffixes: list[str]) -> list[str]:
    parts: list[str] = [word]
    while True:
        stem = parts[0]
        if len(stem) <= 3:  # keep a minimal stem
            break
        stripped = False
        for suf in suffixes:
            if stem.endswith(suf) and len(stem) - len(suf) >= 3:
                parts[0] = stem[: -len(suf)]
                parts.insert(1, suf)
                stripped = True
                break
        if not stripped:
            break
    return parts


def split_suffixes(text: str) -> list[list[str]]:
    """Split every word into [stem, suffix, suffix, ...].

    Returns a list with one entry per word. Script is auto-detected.
    """
    from .translit import is_arabic_script

    arabic = is_arabic_script(text)
    suffixes = _SUFFIXES_UG if arabic else _SUFFIXES_LATIN
    return [_split_suffixes_word(w, suffixes) for w in split_words(text)]


def stems(text: str) -> list[str]:
    """Convenience: just the stems of all words (for search normalization)."""
    return [parts[0] for parts in split_suffixes(text)]
