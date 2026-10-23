"""Bilingual Chinese-Uyghur product glossary.

Use case: cross-border e-commerce sellers who list products in Chinese and
need consistent Uyghur (and English) product terms, e.g. for listings,
customer service replies, and keyword alignment.
"""

from __future__ import annotations

import json
from difflib import SequenceMatcher
from pathlib import Path
from typing import Optional

_DATA_FILE = Path(__file__).parent / "data" / "ug_zh_glossary.json"


class Glossary:
    """A small bilingual glossary loaded from a JSON file."""

    def __init__(self, entries: list[dict] | None = None, path: Path | None = None):
        if entries is not None:
            self.entries = entries
        else:
            with open(path or _DATA_FILE, encoding="utf-8") as f:
                self.entries = json.load(f)
        self._by_zh = {e["zh"]: e for e in self.entries}
        self._by_ug = {e["ug"]: e for e in self.entries}
        self._by_en = {e.get("en", "").lower(): e for e in self.entries if e.get("en")}

    # -- exact lookup -------------------------------------------------------
    def lookup(self, term: str) -> Optional[dict]:
        term = term.strip()
        if term in self._by_zh:
            return self._by_zh[term]
        if term in self._by_ug:
            return self._by_ug[term]
        return self._by_en.get(term.lower())

    # -- fuzzy search -------------------------------------------------------
    def search(self, term: str, limit: int = 5) -> list[tuple[dict, float]]:
        """Fuzzy match against zh/ug/en fields, best first."""
        scored = []
        term = term.strip().lower()
        for e in self.entries:
            fields = [e["zh"], e["ug"], e.get("en", "")]
            score = max(
                SequenceMatcher(None, term, f.lower()).ratio() for f in fields
            )
            # substring bonus
            if term and any(term in f.lower() for f in fields if f):
                score = min(1.0, score + 0.15)
            scored.append((e, score))
        scored.sort(key=lambda x: -x[1])
        return scored[:limit]

    def __len__(self) -> int:
        return len(self.entries)
