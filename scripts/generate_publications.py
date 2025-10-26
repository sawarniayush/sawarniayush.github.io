#!/usr/bin/env python3
"""Generate the publications include from a BibTeX file."""
from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
BIB_PATH = ROOT / "publications.bib"
OUTPUT_PATH = ROOT / "_includes" / "publications.md"
PRIMARY_AUTHOR = "Ayush Sawarni"

LINK_FIELDS: List[Tuple[str, str]] = [
    ("pdf", "PDF"),
    ("slides", "Slides"),
    ("poster", "Poster"),
    ("talk", "Talk"),
    ("video", "Video"),
    ("code", "Code"),
    ("website", "Website"),
    ("doi", "DOI"),
]


def _load_bibtex() -> str:
    if not BIB_PATH.exists():
        raise SystemExit(f"BibTeX file not found: {BIB_PATH}")
    return BIB_PATH.read_text(encoding="utf-8")


def _split_entries(text: str) -> List[str]:
    entries: List[str] = []
    buffer = []
    depth = 0
    in_entry = False
    for char in text:
        if char == "@" and not in_entry:
            in_entry = True
            buffer = [char]
            depth = 0
            continue
        if in_entry:
            buffer.append(char)
            if char == "{" and (len(buffer) < 2 or buffer[-2] != "\\"):
                depth += 1
            elif char == "}" and (len(buffer) < 2 or buffer[-2] != "\\"):
                depth -= 1
                if depth <= 0:
                    entries.append("".join(buffer).strip())
                    in_entry = False
    return entries


def _parse_entry(entry: str) -> Dict[str, str]:
    match = re.match(r"@(?P<type>\w+)\s*\{(?P<key>[^,]+),", entry, re.DOTALL)
    if not match:
        raise ValueError(f"Invalid BibTeX entry: {entry}")
    entry_type = match.group("type").lower()
    body = entry[match.end():].rstrip("}").strip()

    fields: Dict[str, str] = {"entrytype": entry_type, "key": match.group("key").strip()}

    # Simple field parser that expects `name = {value}` pairs.
    field_pattern = re.compile(r"(\w+)\s*=\s*\{", re.MULTILINE)
    pos = 0
    while True:
        field_match = field_pattern.search(body, pos)
        if not field_match:
            break
        name = field_match.group(1).lower()
        value_start = field_match.end()
        brace_depth = 1
        value_chars = []
        i = value_start
        while i < len(body) and brace_depth > 0:
            char = body[i]
            if char == "{" and (i == value_start or body[i - 1] != "\\"):
                brace_depth += 1
            elif char == "}" and body[i - 1] != "\\":
                brace_depth -= 1
                if brace_depth == 0:
                    i += 1
                    break
            value_chars.append(char)
            i += 1
        value = "".join(value_chars).strip()
        fields[name] = value
        pos = i
    return fields


def _format_authors(author_field: str, author_note: str | None) -> str:
    authors = [name.strip() for name in author_field.replace("\n", " ").split(" and ") if name.strip()]
    formatted = []
    for name in authors:
        if name.lower() == PRIMARY_AUTHOR.lower():
            formatted.append(f"<strong>{name}</strong>")
        else:
            formatted.append(name)
    author_text = ", ".join(formatted)
    if author_note:
        author_text = f"{author_text} {author_note.strip()}"
    return author_text


def _format_periodical(fields: Dict[str, str]) -> str:
    custom = fields.get("periodical", "").strip()
    if custom:
        return custom

    entry_type = fields.get("entrytype", "")
    year = fields.get("year", "").strip()
    if entry_type in {"inproceedings", "article"}:
        venue = fields.get("booktitle") or fields.get("journal") or ""
        venue_html = venue.strip()
        if venue_html:
            return f"<em>{venue_html}</em> {year}".strip()
    if entry_type in {"mastersthesis", "phdthesis"}:
        school = fields.get("school", "").strip()
        return school or year
    return fields.get("periodical", "").strip()


def _build_links(fields: Dict[str, str]) -> List[str]:
    links: List[str] = []
    for field, label in LINK_FIELDS:
        url = fields.get(field, "").strip()
        if url:
            links.append(
                f'      <a href="{url}" class="btn btn-sm z-depth-0" role="button" target="_blank" style="font-size:12px;">{label}</a>'
            )
    highlight = fields.get("highlight", "").strip()
    if highlight:
        color = fields.get("highlight_color", "#e74d3c").strip() or "#e74d3c"
        links.append(f'      <strong><i style="color:{color}">{highlight}</i></strong>')
    return links


def _render_entry(fields: Dict[str, str], index: int) -> str:
    title = fields.get("title", "").strip()
    url = fields.get("url", "").strip()
    author_note = fields.get("author_note", "").strip()
    author_text = _format_authors(fields.get("author", ""), author_note if author_note else None)
    periodical = _format_periodical(fields)
    links = _build_links(fields)

    parts = [
        "<div class=\"pub-row\">",
        "  <div class=\"col-sm-9\" style=\"position: relative;padding-right: 15px;padding-left: 20px;\">",
    ]
    if url:
        parts.append(f'    <div class="title"><a href="{url}">{title}</a></div>')
    else:
        parts.append(f'    <div class="title"><a href="">{title}</a></div>')
    prefix = " " if author_text.startswith("<") else ""
    parts.append(f'    <div class="author">{prefix}{author_text}</div>')
    if periodical:
        parts.append(f"    <div class=\"periodical\">{periodical}</div>")
    if links:
        parts.append('    <div class="links">')
        parts.extend(links)
        parts.append("    </div>")
    parts.append("  </div>")
    parts.append("</div>")
    spacer = "  " if index < 2 else ""
    parts.append(spacer)
    return "\n".join(parts)


def _sort_key(fields: Dict[str, str]) -> Tuple[int, str]:
    year_str = fields.get("year", "").strip()
    try:
        year_value = int(year_str)
    except ValueError:
        year_value = -10**9
    title = fields.get("title", "").strip().lower()
    return year_value, title


def _render(entries: Iterable[Dict[str, str]]) -> str:
    output_lines = [
        "<!-- This file is auto-generated by scripts/generate_publications.py. Do not edit by hand. -->",
        '<h2 id="publications" style="margin: 2px 0px -15px;">Publications</h2>',
        "",
        '<div class="publications">',
        '<ol class="bibliography">',
        "",
        "<li>",
    ]

    for index, entry in enumerate(entries):
        output_lines.append(_render_entry(entry, index))

    output_lines.extend([
        "</li>",
        "  ",
        "<br>",
        "",
        "</ol>",
        "</div>",
        "",
    ])

    content = "\n".join(output_lines)
    if not content.endswith("\n"):
        content += "\n"
    if not content.endswith("\n\n"):
        content += "\n"
    return content


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="only verify that the generated include is up to date",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    text = _load_bibtex()
    entries = [_parse_entry(entry) for entry in _split_entries(text)]
    entries.sort(key=_sort_key, reverse=True)

    content = _render(entries)

    if args.check:
        if not OUTPUT_PATH.exists():
            raise SystemExit(
                "Publications include does not exist. Run the generator to create it."
            )
        current = OUTPUT_PATH.read_text(encoding="utf-8")
        if current != content:
            raise SystemExit(
                "Publications include is out of date. Run the generator script to refresh it."
            )
        print("Publications include is up to date.")
        return

    OUTPUT_PATH.write_text(content, encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
