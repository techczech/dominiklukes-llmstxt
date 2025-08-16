#!/usr/bin/env python3
"""
Ingest pre-existing Metaphor Hacker Markdown files into the monorepo layout.

Input:
  sources/metaphorhacker_md/incoming/*.md  (filenames: YYYY-MM-DD-slug.md)

Output:
  content/YYYY/slug/index.md      (with normalized YAML front matter)
  plain/mh-YYYYMMDD-slug.txt      (plain-text mirror of body content)
"""

import argparse
import pathlib
import re
from datetime import datetime
import frontmatter

ROOT = pathlib.Path(".").resolve()
IN_DIR = ROOT / "sources" / "metaphorhacker_md" / "incoming"
OUT_CONTENT = ROOT / "content"
OUT_PLAIN = ROOT / "plain"
OUT_CONTENT.mkdir(parents=True, exist_ok=True)
OUT_PLAIN.mkdir(parents=True, exist_ok=True)

FILENAME_RE = re.compile(r"^(?P<y>\d{4})-(?P<m>\d{2})-(?P<d>\d{2})-(?P<slug>.+)\.md$", re.IGNORECASE)

def md_to_text(md_body: str) -> str:
    """Minimal Markdown → plain text cleanup (keeps code, drops markup)."""
    text = md_body
    # strip YAML front matter if any slipped in
    text = re.sub(r"(?s)^---\n.*?\n---\n", "", text).strip()
    # images ![alt](url) -> alt
    text = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", text)
    # links [text](url) -> text (url)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1 (\2)", text)
    # inline code `code` -> code
    text = text.replace("`", "")
    # bold/italics **strong** *em* -> strong / em
    text = text.replace("**", "").replace("*", "").replace("_", "")
    # headings: remove leading # and extra spaces
    text = re.sub(r"^#{1,6}\s*", "", text, flags=re.MULTILINE)
    # blockquotes: drop >
    text = re.sub(r"^\s*>\s?", "", text, flags=re.MULTILINE)
    # horizontal rules
    text = re.sub(r"^\s*[-*_]{3,}\s*$", "", text, flags=re.MULTILINE)
    return text.strip()

def derive_title(content_body: str, slug: str) -> str:
    # Use first ATX heading (# Title) if present
    m = re.search(r"^\s*#\s+(.+)$", content_body, flags=re.MULTILINE)
    if m:
        return m.group(1).strip()
    # Fallback: slug → Title Case-ish
    return re.sub(r"[-_]+", " ", slug).strip().capitalize()

def enrich_front_matter(fm: dict, date_str: str, slug: str) -> dict:
    ymd = date_str.replace("-", "")
    fm.setdefault("id", f"mh-{ymd}-{slug}")
    fm.setdefault("date", date_str)
    fm.setdefault("source", {"name": "Metaphor Hacker", "url": "https://metaphorhacker.net/"})
    fm.setdefault("canonical_url", "")
    fm.setdefault("tags", [])
    fm.setdefault("categories", [])
    fm.setdefault("language", "en")
    fm.setdefault("license", "CC-BY-4.0")
    fm.setdefault("original_format", "md")
    return fm

def process_file(md_path: pathlib.Path, force: bool = False) -> str:
    m = FILENAME_RE.match(md_path.name)
    if not m:
        return f"[SKIP] {md_path.name} (filename does not match YYYY-MM-DD-slug.md)"

    year, month, day = m.group("y"), m.group("m"), m.group("d")
    slug = m.group("slug")
    date_str = f"{year}-{month}-{day}"

    # Load (and preserve) any existing front matter
    post = frontmatter.load(md_path)
    body = post.content or ""
    if "title" not in post or not post["title"]:
        post["title"] = derive_title(body, slug)

    post.metadata = enrich_front_matter(dict(post.metadata), date_str, slug)

    # Destination paths
    dest_dir = OUT_CONTENT / year / slug
    dest_md = dest_dir / "index.md"
    dest_txt = OUT_PLAIN / f"mh-{year}{month}{day}-{slug}.txt"

    if dest_md.exists() and not force:
        return f"[SKIP] {md_path.name} (exists; use --force to overwrite)"

    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_md.write_text(frontmatter.dumps(post), encoding="utf-8")
    dest_txt.write_text(md_to_text(body), encoding="utf-8")

    return f"[OK]   {md_path.name} -> {dest_md.relative_to(ROOT)} ; {dest_txt.relative_to(ROOT)}"

def main():
    parser = argparse.ArgumentParser(description="Ingest Metaphor Hacker Markdown files.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing outputs")
    args = parser.parse_args()

    if not IN_DIR.exists():
        print(f"[ERROR] Input directory not found: {IN_DIR}")
        return

    md_files = sorted(IN_DIR.glob("*.md"))
    if not md_files:
        print(f"[WARN] No .md files found in {IN_DIR}")
        return

    for p in md_files:
        print(process_file(p, force=args.force))

if __name__ == "__main__":
    main()
