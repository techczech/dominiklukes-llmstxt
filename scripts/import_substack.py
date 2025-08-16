#!/usr/bin/env python3
"""
Import Substack posts via RSS.

Usage:
  python scripts/import_substack.py            # uses FEEDS list
  python scripts/import_substack.py --force    # overwrite existing outputs
  python scripts/import_substack.py --feed URL # add feed(s) on the CLI

Notes:
- Substack feeds are usually https://<publication>.substack.com/feed
- Requires: feedparser trafilatura markdownify python-frontmatter python-slugify requests
"""

from __future__ import annotations
import argparse
import pathlib
import datetime
import json
import re
import time
import feedparser
import requests
from trafilatura import extract, fetch_url
from markdownify import markdownify as md
from slugify import slugify
import frontmatter

# Edit feeds: add your Substack publication or author feeds here
FEEDS = [
    "https://promisingparagraphs.substack.com/feed",
    # "https://your-substack.substack.com/feed",
]

ROOT = pathlib.Path(".").resolve()
RAW_DIR = ROOT / "sources" / "substack" / "raw"
OUT_CONTENT = ROOT / "content"
OUT_PLAIN = ROOT / "plain"

for d in (RAW_DIR, OUT_CONTENT, OUT_PLAIN):
    d.mkdir(parents=True, exist_ok=True)

def html_to_md(html: str) -> str:
    return md(html or "", heading_style="ATX", strip=["script", "style"]).strip()

def fetch_full_html(url: str) -> str | None:
    try:
        html = fetch_url(url, timeout=60)
        if not html:
            r = requests.get(url, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
            r.raise_for_status()
            return r.text
        return html
    except Exception as e:
        print(f"[WARN] fetch_full_html failed for {url}: {e}")
        return None

def extract_main_html(html: str) -> str | None:
    try:
        text = extract(html, include_comments=False, output_format='xml')
        if not text:
            text = extract(html, include_comments=False, output_format='text')
        return text
    except Exception as e:
        print(f"[WARN] trafilatura.extract failed: {e}")
        return None

def normalize_title(title: str) -> str:
    if not title:
        return "untitled"
    return re.sub(r"\s+", " ", title).strip()

def make_slug(title: str) -> str:
    return slugify(title, max_length=80)

def process_entry(entry: dict, feed_url: str, force: bool = False) -> None:
    # dates
    published_parsed = entry.get("published_parsed") or entry.get("updated_parsed")
    if published_parsed:
        date = datetime.date(*published_parsed[:3])
    else:
        date = datetime.date.today()
    date_str = date.isoformat()
    year = date_str[:4]

    # canonical link
    canonical = entry.get("link") or entry.get("id") or ""
    if entry.get("links"):
        for l in entry["links"]:
            if l.get("rel") in ("alternate", None) and l.get("href"):
                canonical = l.get("href"); break

    title = normalize_title(entry.get("title") or entry.get("summary") or "Untitled")
    slug = make_slug(title)
    nid = f"sb-{date_str.replace('-','')}-{slug}"

    dest_dir = OUT_CONTENT / year / slug
    dest_md = dest_dir / "index.md"
    dest_txt = OUT_PLAIN / f"{nid}.txt"

    if dest_md.exists() and not force:
        print(f"[SKIP] {nid} (exists)")
        return

    # get HTML from feed
    content_html = ""
    if entry.get("content"):
        try:
            content_html = entry.get("content")[0].get("value", "")
        except Exception:
            content_html = entry.get("content")
    elif entry.get("summary_detail"):
        content_html = entry.get("summary") or ""

    if not content_html or len(content_html) < 200:
        fetched = fetch_full_html(canonical)
        if fetched:
            main = extract_main_html(fetched)
            if main:
                content_html = main

    body_md = html_to_md(content_html or "")
    if not body_md:
        body_md = (entry.get("summary") or "").strip()

    fm = {
        "id": nid,
        "title": title,
        "date": date_str,
        "source": {"name": "Substack", "url": feed_url},
        "canonical_url": canonical,
        "tags": [t.get("term") if isinstance(t, dict) else t for t in entry.get("tags", [])] if entry.get("tags") else [],
        "language": "en",
        "license": "CC-BY-4.0",
        "original_format": "html",
    }

    dest_dir.mkdir(parents=True, exist_ok=True)
    post = frontmatter.Post(body_md, **fm)
    dest_md.write_text(frontmatter.dumps(post), encoding="utf-8")
    # plain text cleanup
    plain = re.sub(r"(?m)^\s*$", "\n", re.sub(r"\s+", " ", re.sub(r"\r", "", post.content.strip())))
    dest_txt.write_text(plain, encoding="utf-8")
    print(f"[OK]   {nid} -> {dest_md.relative_to(ROOT)}")

def run(feeds: list[str], force: bool = False):
    for f_url in feeds:
        print(f"[FEED] {f_url}")
        d = feedparser.parse(f_url)
        rawfn = RAW_DIR / (slugify(f_url)[:50] + ".json")
        rawfn.write_text(json.dumps(d, ensure_ascii=False, default=str, indent=2), encoding="utf-8")
        entries = d.entries or []
        print(f"  entries: {len(entries)}")
        for e in entries:
            try:
                process_entry(e, f_url, force=force)
            except Exception as exc:
                print(f"[ERROR] processing entry: {exc}")
            time.sleep(0.1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--feed", action="append", help="additional feed URL to process")
    args = parser.parse_args()
    FEEDS_RUN = FEEDS + (args.feed or [])
    run(FEEDS_RUN, force=args.force)
