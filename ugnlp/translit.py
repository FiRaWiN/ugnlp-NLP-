"""Bidirectional conversion between Uyghur scripts.

Supported scripts:
- UEY  (Uyghur Ereb Yëziqi): Arabic script, used in Xinjiang / official documents
- ULY  (Uyghur Latin Yëziqi): Latin script, common on the internet

Note: conversion is rule-based and practical (not a full orthography engine).
Multi-character Latin clusters (zh, sh, ch, gh, ng) are matched greedily;
word-initial vowels get a hamza carrier (ئ) in Arabic script per UEY rules.
"""

from __future__ import annotations

# Latin (ULY) -> Arabic (UEY)
_LATIN_TO_ARABIC: dict[str, str] = {
    "zh": "ژ",
    "sh": "ش",
    "ch": "چ",
    "gh": "غ",
    "ng": "ڭ",
    "b": "ب",
    "p": "پ",
    "t": "ت",
    "j": "ج",
    "x": "خ",
    "d": "د",
    "r": "ر",
    "z": "ز",
    "s": "س",
    "f": "ف",
    "q": "ق",
    "k": "ك",
    "g": "گ",
    "l": "ل",
    "m": "م",
    "n": "ن",
    "h": "ھ",
    "w": "ۋ",
    "y": "ي",
    "a": "ا",
    "e": "ې",
    "é": "ە",
    "i": "ى",
    "o": "و",
    "u": "ۇ",
    "ö": "ۆ",
    "ü": "ۈ",
}

# Arabic (UEY) -> Latin (ULY)
_ARABIC_TO_LATIN: dict[str, str] = {
    "ژ": "zh",
    "ش": "sh",
    "چ": "ch",
    "غ": "gh",
    "ڭ": "ng",
    "ب": "b",
    "پ": "p",
    "ت": "t",
    "ج": "j",
    "خ": "x",
    "د": "d",
    "ر": "r",
    "ز": "z",
    "س": "s",
    "ف": "f",
    "ق": "q",
    "ك": "k",
    "گ": "g",
    "ل": "l",
    "م": "m",
    "ن": "n",
    "ھ": "h",
    "ه": "h",
    "و": "o",
    "ۇ": "u",
    "ۆ": "ö",
    "ۈ": "ü",
    "ۋ": "w",
    "ي": "y",
    "ى": "i",
    "ی": "i",
    "ا": "a",
    "ې": "e",
    "ە": "é",
}

# Word-initial vowels need a hamza carrier in UEY.
_VOWELS = set("aeéiouöü")

# Hamza + vowel combos -> plain Latin vowel
_HAMZA_VOWEL = {
    "ئا": "a",
    "ئې": "e",
    "ئە": "é",
    "ئى": "i",
    "ئو": "o",
    "ئۇ": "u",
    "ئۆ": "ö",
    "ئۈ": "ü",
}

_VOWEL_ARABIC = {
    "a": "ا",
    "e": "ې",
    "é": "ە",
    "i": "ى",
    "o": "و",
    "u": "ۇ",
    "ö": "ۆ",
    "ü": "ۈ",
}


def to_arabic(text: str) -> str:
    """Convert Uyghur Latin (ULY) text to Arabic script (UEY)."""
    out: list[str] = []
    i = 0
    word_start = True
    while i < len(text):
        ch = text[i]
        if ch.isspace() or ch in ".,!?;:-()\"'" + "،؟؛—«»":
            out.append(ch)
            word_start = True
            i += 1
            continue
        if not ch.isascii():
            out.append(ch)
            word_start = False
            i += 1
            continue
        low = ch
        # try two-char cluster first (lowercase-insensitive handled below)
        pair = text[i : i + 2].lower()
        if pair in _LATIN_TO_ARABIC and pair not in _VOWELS:
            out.append(_LATIN_TO_ARABIC[pair])
            i += 2
            word_start = False
            continue
        v = low if low in _VOWELS else low
        if v in _VOWELS:
            if word_start:
                out.append("ئ" + _VOWEL_ARABIC[v])
            else:
                out.append(_VOWEL_ARABIC[v])
            word_start = False
            i += 1
            continue
        if low in _LATIN_TO_ARABIC:
            out.append(_LATIN_TO_ARABIC[low])
            word_start = False
            i += 1
            continue
        out.append(ch)
        word_start = False
        i += 1
    return "".join(out)


def to_latin(text: str) -> str:
    """Convert Uyghur Arabic script (UEY) text to Latin (ULY)."""
    out: list[str] = []
    i = 0
    while i < len(text):
        pair = text[i : i + 2]
        if pair in _HAMZA_VOWEL:
            out.append(_HAMZA_VOWEL[pair])
            i += 2
            continue
        ch = text[i]
        if ch == "ئ":
            # bare hamza carrier before consonant or standalone: soft marker
            i += 1
            continue
        if ch in _ARABIC_TO_LATIN:
            out.append(_ARABIC_TO_LATIN[ch])
            i += 1
            continue
        out.append(ch)
        i += 1
    return "".join(out)


def is_arabic_script(text: str) -> bool:
    """Heuristic: does the text look like Arabic-script Uyghur?"""
    arabic = sum(1 for c in text if "\u0600" <= c <= "\u06ff")
    return arabic > len(text.replace(" ", "")) / 2
