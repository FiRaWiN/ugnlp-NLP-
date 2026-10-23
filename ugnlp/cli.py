"""Command-line interface: python -m ugnlp <command> ..."""

from __future__ import annotations

import argparse
import json
import sys

from . import __version__
from .glossary import Glossary
from .numbers import convert_digits
from .tokenizer import split_sentences, split_suffixes, split_words
from .translit import is_arabic_script, to_arabic, to_latin


def _read_stdin() -> str:
    return sys.stdin.read()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="ugnlp",
        description="Lightweight Uyghur/Chinese NLP toolkit (zero dependencies).",
    )
    parser.add_argument("--version", action="version", version=f"ugnlp {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("translit", help="Convert between ULY (Latin) and UEY (Arabic)")
    p.add_argument("--to", choices=["latin", "arabic", "auto"], default="auto")
    p.add_argument("text", nargs="*", help="Text to convert (default: stdin)")

    p = sub.add_parser("tokenize", help="Word segmentation")
    p.add_argument("text", nargs="*")

    p = sub.add_parser("suffix", help="Split words into stem + suffixes")
    p.add_argument("text", nargs="*")

    p = sub.add_parser("sentences", help="Sentence segmentation")
    p.add_argument("text", nargs="*")

    p = sub.add_parser("digits", help="Normalize digits")
    p.add_argument("--to", choices=["ascii", "arabic"], default="ascii")
    p.add_argument("text", nargs="*")

    p = sub.add_parser("lookup", help="Look up a term in the zh/ug product glossary")
    p.add_argument("term")

    p = sub.add_parser("stems", help="Extract word stems (search normalization)")
    p.add_argument("text", nargs="*")

    args = parser.parse_args(argv)
    text_arg = getattr(args, "text", None) or getattr(args, "term", None)
    text = " ".join(text_arg) if text_arg else _read_stdin().strip()

    if args.command == "translit":
        target = args.to
        if target == "auto":
            target = "latin" if is_arabic_script(text) else "arabic"
        print(to_latin(text) if target == "latin" else to_arabic(text))
    elif args.command == "tokenize":
        print(json.dumps(split_words(text), ensure_ascii=False))
    elif args.command == "suffix":
        print(json.dumps(split_suffixes(text), ensure_ascii=False, indent=2))
    elif args.command == "sentences":
        print(json.dumps(split_sentences(text), ensure_ascii=False, indent=2))
    elif args.command == "digits":
        print(convert_digits(text, to=args.to))
    elif args.command == "stems":
        print(json.dumps(split_suffixes(text), ensure_ascii=False))
    elif args.command == "lookup":
        g = Glossary()
        hit = g.lookup(args.term)
        if hit:
            print(json.dumps(hit, ensure_ascii=False, indent=2))
        else:
            matches = g.search(args.term, limit=3)
            if matches:
                print("No exact match. Fuzzy results:")
                for e, score in matches:
                    print(f"  {e['zh']}  ↔  {e['ug']}  ({e.get('en', '')})  [{score:.2f}]")
            else:
                print("No match found.")
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
