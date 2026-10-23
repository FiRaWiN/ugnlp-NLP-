# ugnlp — 轻量级维吾尔语/中文 NLP 工具集

[![tests](https://github.com/FiRaWiN/ugnlp-NLP-/actions/workflows/tests.yml/badge.svg)](https://github.com/FiRaWiN/ugnlp-NLP-/actions/workflows/tests.yml)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

**English** | [中文](#中文)

A zero-dependency Python toolkit for Uyghur ↔ Chinese e-commerce text processing:
script conversion, morphological suffix splitting, bilingual product glossary,
and mixed-script digit normalization. Pure standard library — no installs needed.

## Why

Uyghur is an agglutinative Turkic language written in two scripts (official
Arabic-based UEY and internet-common Latin ULY). Sellers in cross-border
e-commerce constantly juggle Chinese / Uyghur / English product text, but
almost no open-source tooling exists for this niche. `ugnlp` is a pragmatic,
hackable starting point.

## Features

| Module | What it does |
|---|---|
| `translit` | Bidirectional ULY (Latin) ↔ UEY (Arabic) conversion, hamza-aware |
| `tokenizer` | Word & sentence segmentation; greedy stem + suffix splitting |
| `glossary` | Chinese ↔ Uyghur product-term glossary with exact + fuzzy lookup |
| `numbers` | Arabic-Indic ↔ ASCII digit normalization; Uyghur number words → int |

## Install

```bash
pip install .            # or just add the ugnlp/ folder to your project
```

Zero third-party dependencies. Python ≥ 3.10.

## CLI quick start

```bash
# Latin -> Arabic script
python -m ugnlp translit "salam dostum"
# -> ئاسالام دوستۇم style output

# Arabic -> Latin (auto-detected)
echo "ئىككى" | python -m ugnlp translit --to latin
# -> ikki

# Stem + suffix split (Uyghur is agglutinative)
python -m ugnlp suffix "ئۆيلەرنىڭ"
# -> [["ئۆي", "لەر", "نىڭ"]]   (house + PL + GEN)

# Bilingual product glossary
python -m ugnlp lookup 洗发水
# -> {"zh": "洗发水", "ug": "چاچ سوپۇنى", "en": "shampoo"}

# Digit normalization
python -m ugnlp digits --to ascii "٣ خالتە"
# -> 3 خالتە
```

## Python API

```python
from ugnlp import to_latin, to_arabic, split_suffixes, Glossary, convert_digits

to_latin("ئۈچ")                    # 'üch'
split_suffixes("ئۆيلەرنىڭ")        # [['ئۆي', 'لەر', 'نىڭ']]
Glossary().lookup("洗发水")         # {'zh': ..., 'ug': ..., 'en': 'shampoo'}
convert_digits("٤٥", to="ascii")    # '45'
```

## Extending

- **Glossary**: edit `ugnlp/data/ug_zh_glossary.json` — add your own product terms.
- **Suffix list**: `ugnlp/tokenizer.py` `_SUFFIXES_UG` — the suffix inventory is
  deliberately small; PRs adding (well-tested) suffixes are welcome.
- **Transliteration**: `ugnlp/translit.py` — mapping tables are plain dicts.

## Limitations (honest ones)

- Script conversion is rule-based: it does not model every UEY orthography
  exception (e.g. syllable-final spellings, loanword conventions).
- Suffix splitting is greedy longest-match, not full morphological analysis.
- The glossary is a starter set (~20 hair-care / cosmetics terms).

## Test

```bash
python -m unittest discover -s tests -v
```

## License

MIT — see [LICENSE](LICENSE).

---

<a id="中文"></a>
# ugnlp — 中文说明

零依赖的维吾尔语/中文 NLP 小工具集，面向跨境电商场景：拉丁-阿拉伯字母转写、
黏着语后缀切分、中维双语商品词库、混合文字数字归一化。纯 Python 标准库实现，
`pip install .` 即可用，也可以直接把 `ugnlp/` 文件夹拷进你的项目。

背景：维吾尔语有两种通行文字（官方阿拉伯字母 UEY、网络上常用的拉丁 ULY），
跨境电商卖家天天在中文/维语/英文商品文案之间切换，但这个细分领域几乎没有
开源工具。ugnlp 就是给这个空白补一个实用的起点。

运行示例见上面的 CLI quick start。测试：`python -m unittest discover -s tests`。
