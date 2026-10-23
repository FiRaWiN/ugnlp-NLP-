"""Digit and basic number handling for Uyghur text.

Uyghur text mixes Arabic-Indic digits (٠-٩ / ۰-۹) with ASCII digits.
E-commerce copy often needs one consistent style — this normalizes it.
"""

from __future__ import annotations

import re

# Eastern Arabic-Indic (Uyghur standard) and Persian variants
_ARABIC_INDIC = "٠١٢٣٤٥٦٧٨٩"
_PERSIAN = "۰۱۲۳۴۵۶۷۸۹"

_NUM_WORDS_UG = {
    "نۆل": 0, "بىر": 1, "ئىككى": 2, "ئۈچ": 3, "تۆت": 4,
    "بەش": 5, "ئالتە": 6, "يەتتە": 7, "سەككىز": 8, "توققۇز": 9, "ئون": 10,
}

_NUM_WORDS_LATIN = {
    "nöl": 0, "bir": 1, "ikki": 2, "üch": 3, "töt": 4,
    "besh": 5, "altä": 6, "yettä": 7, "sekkiz": 8, "toqquz": 9, "on": 10,
}


def convert_digits(text: str, to: str = "ascii") -> str:
    """Normalize digits in *text*.

    to="ascii":  Arabic-Indic / Persian digits -> 0-9
    to="arabic": 0-9 -> Arabic-Indic digits (Uyghur standard)
    """
    if to == "ascii":
        table = str.maketrans(_ARABIC_INDIC + _PERSIAN, "0123456789" * 2)
        return text.translate(table)
    if to == "arabic":
        table = str.maketrans("0123456789", _ARABIC_INDIC)
        return text.translate(table)
    raise ValueError(f"unknown target: {to!r}")


def ug_number_to_int(word: str) -> int | None:
    """Return the integer value of a single Uyghur number word (0-10), or None."""
    w = word.strip()
    if w in _NUM_WORDS_UG:
        return _NUM_WORDS_UG[w]
    return _NUM_WORDS_LATIN.get(w.lower())


def extract_numbers(text: str) -> list[int]:
    """Extract integers from mixed-script text (digits or Uyghur number words)."""
    text = convert_digits(text, to="ascii")
    out = [int(m) for m in re.findall(r"\d+", text)]
    for token in re.split(r"[\s،,.]+", text):
        v = ug_number_to_int(token)
        if v is not None:
            out.append(v)
    return out
