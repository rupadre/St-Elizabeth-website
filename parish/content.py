"""Loads the site's content from the content/ folder.

This module has no Django imports, so the same code serves the Django views
and the preview builder (build_preview.py). Pages are Markdown files with a
short header between --- lines, e.g.:

    ---
    title: Your first visit
    order: 1
    ---
    Body text in Markdown...
"""
import json
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"


def _parse(path):
    text = path.read_text(encoding="utf-8")
    meta, body = {}, text
    if text.startswith("---"):
        _, header, body = text.split("---", 2)
        for line in header.strip().splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                meta[key.strip()] = value.strip()
    meta["slug"] = path.stem
    meta["html"] = markdown.markdown(body, extensions=["extra", "sane_lists", "attr_list"])
    meta["order"] = int(meta.get("order", 999))
    return meta


def page(section, slug):
    return _parse(CONTENT / section / f"{slug}.md")


def section_pages(section):
    pages = [_parse(p) for p in (CONTENT / section).glob("*.md") if p.stem != "index"]
    return sorted(pages, key=lambda p: (p["order"], p["slug"]))


def data(name):
    return json.loads((CONTENT / f"{name}.json").read_text(encoding="utf-8"))


def raw_html(name):
    return (CONTENT / f"{name}.html").read_text(encoding="utf-8")
