#!/usr/bin/env python3
"""
Import articles from Medium RSS feeds into the monorepo.

Usage:
  python scripts/import_medium.py               # uses FEEDS list below
  python scripts/import_medium.py --force       # overwrite existing outputs

Notes:
- Add or remove feeds in FEEDS below (author/profile or publication feed URLs).
- If the feed entry lacks full content, the script will fetch the article page and
  attempt to extract main content via trafilatura.

Requires:
  pip install feedparser trafilatura markdownify python-frontmatter python-slugify requests pyyaml
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

# EDIT THIS LIST: your Medium profile(s) / publication feed URLs
FEEDS = [
    "https://medium.com/feed/@techczech",
    "https://medium.com/feed/metaphor-hacker",  # add any additional feed URLs here
]

ROOT = pathlib.Path(".").resolve()
RAW_DIR = ROOT / "sources" / "medium" / "raw"
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
            # fallback to requests if trafilatura fetch failed
            r = requests.get(url, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
            r.raise_for_status()
            return r.text
        return html
    except Exception as e:
        print(f"[WARN] fetch_full_html failed for {url}: {e}")
        return None

def extract_main_html(html: str) -> str | None:
    try:
        text = extract(html, include_comments=False, output_format='xml')  # xml contains markup
        if not text:
            # fallback to plain text extraction (trafilatura)
            text = extract(html, include_comments=False, output_format='text')
            return text
        return text
    except Exception as e:
        print(f"[WARN] trafilatura.extract failed: {e}")
        return None

def normalize_title(title: str) -> str:
    if not title:
        return "untitled"
    # strip stray newlines & html entities
    return re.sub(r"\s+", " ", title).strip()

def make_slug(title: str, published: datetime.date, feed_slug: str) -> str:
    s = slugify(title, max_length=80)
    # ensure uniqueness-ish by including feed nickname (short)
    return f"{s}"

def process_entry(entry: dict, feed_url: str, force: bool = False) -> None:
    # id & dates
    published_parsed = entry.get("published_parsed") or entry.get("updated_parsed")
    if published_parsed:
        date = datetime.date(*published_parsed[:3])
    else:
        date = datetime.date.today()
    date_str = date.isoformat()
    year = date_str[:4]

    # try to detect canonical URL
    link = entry.get("link") or entry.get("id") or ""
    canonical = ""
    # medium sometimes has 'links' or 'media_content'
    if entry.get("links"):
        for l in entry.get("links"):
            if l.get("rel") == "alternate" and l.get("href"):
                canonical = l.get("href"); break
    if not canonical:
        canonical = link

    title = normalize_title(entry.get("title") or entry.get("summary") or "Untitled")
    slug = make_slug(title, date, feed_url)
    nid = f"md-{date_str.replace('-','')}-{slug}"

    dest_dir = OUT_CONTENT / year / slug
    dest_md = dest_dir / "index.md"
    dest_txt = OUT_PLAIN / f"{nid}.txt"

    if dest_md.exists() and not force:
        print(f"[SKIP] {nid} (already exists)")
        return

    # get HTML content from feed if available
    content_html = ""
    if entry.get("content"):
        # feedparser returns a list of content dicts
        try:
            content_html = entry.get("content")[0].get("value", "")
        except Exception:
            content_html = entry.get("content")
    elif entry.get("summary_detail"):
        content_html = entry.get("summary") or ""

    # If content is short or looks like a teaser, fetch the page and extract
    if not content_html or len(content_html) < 200:
        fetched = fetch_full_html(canonical or link)
        if fetched:
            main = extract_main_html(fetched)
            if main:
                content_html = main

    body_md = html_to_md(content_html or "")
    # If still empty, fall back to summary or leave blank but include metadata
    if not body_md:
        body_md = (entry.get("summary") or "").strip()

    # front matter
    fm = {
        "id": nid,
        "title": title,
        "date": date_str,
        "source": {"name": "Medium", "url": feed_url},
        "canonical_url": canonical,
        "tags": [t.get("term") if isinstance(t, dict) else t for t in entry.get("tags", [])] if entry.get("tags") else [],
        "language": "en",
        "license": "CC-BY-4.0",
        "original_format": "html",
    }

    # persist
    dest_dir.mkdir(parents=True, exist_ok=True)
    post = frontmatter.Post(body_md, **fm)
    dest_md.write_text(frontmatter.dumps(post), encoding="utf-8")
    dest_txt.write_text(re.sub(r"(?m)^\s*$", "\n", re.sub(r"\s+", " ", re.sub(r"\n{3,}", "\n\n", re.sub(r"\r", "", re.sub(r"\s+\n", "\n", post.content.strip()))))), encoding="utf-8")

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
    parser.add_argument("--force", action="store_true", help="overwrite existing outputs")
    parser.add_argument("--feed", action="append", help="additional feed URL to process (can be repeated)")
    args = parser.parse_args()
    FEEDS_RUN = FEEDS + (args.feed or [])
    run(FEEDS_RUN, force=args.force)
