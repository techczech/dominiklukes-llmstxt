#!/usr/bin/env python3
"""
One-off scrape of Dyslexia Action Tech Blog from the Wayback Machine.

Source index (Wayback snapshot):
  https://web.archive.org/web/20170613010952/http://www.dyslexiaaction.org.uk/tech-blog

This script crawls all paginated index pages, collects post URLs and dates,
fetches each post page, extracts title and main content, converts to Markdown,
and writes into `content/<year>/<slug>/index.md` with a plain text copy in `plain/`.

Usage:
  python scripts/scrape_dyslexiaaction_tech_blog.py           # scrape pages 0..7
  python scripts/scrape_dyslexiaaction_tech_blog.py --force   # overwrite existing
  python scripts/scrape_dyslexiaaction_tech_blog.py --pages 0 7  # set page range

Notes:
  - Relies on requests, trafilatura, markdownify, python-frontmatter, python-slugify
  - Uses regex to parse index listing links and dates; uses trafilatura for post body
  - Canonical URL points to the original domain (without the Wayback prefix)
"""

from __future__ import annotations
import argparse
import datetime as dt
import pathlib
import re
import time
from typing import Iterable, Tuple

import requests
from trafilatura import extract
from markdownify import markdownify as md
from slugify import slugify
import frontmatter


ROOT = pathlib.Path(".").resolve()
RAW_DIR = ROOT / "sources" / "dyslexiaaction" / "raw"
OUT_CONTENT = ROOT / "content"
OUT_PLAIN = ROOT / "plain"

for d in (RAW_DIR, OUT_CONTENT, OUT_PLAIN):
    d.mkdir(parents=True, exist_ok=True)

WAYBACK_BASE = "https://web.archive.org"
INDEX_SNAPSHOT = "20170613010952"
INDEX_URL_BASE = f"{WAYBACK_BASE}/web/{INDEX_SNAPSHOT}/http://www.dyslexiaaction.org.uk/tech-blog"
# Known good snapshot timestamps around 2016 listings
SNAPSHOTS = [
    "20170613010952",  # used by landing page
    "20170504173908",  # used by inner paginated pages
    "20170428003223",
]


def http_get(url: str, timeout: int = 60, retries: int = 5) -> str:
    last_exc: Exception | None = None
    for attempt in range(retries):
        try:
            r = requests.get(url, timeout=timeout, headers={
                "User-Agent": "Mozilla/5.0 (compatible; DA-Scraper/1.0)",
                "Accept": "text/html,application/xhtml+xml"
            }, allow_redirects=True)
            if r.status_code == 429:
                # rate limited; respect Retry-After if present
                ra = r.headers.get("Retry-After")
                wait = int(ra) if ra and ra.isdigit() else (2 * (attempt + 1))
                time.sleep(wait)
                continue
            r.raise_for_status()
            return r.text
        except requests.exceptions.SSLError as exc:
            last_exc = exc
            # Fallback to http (non-TLS) for Wayback if HTTPS has handshake issues
            if url.startswith("https://web.archive.org/"):
                alt = url.replace("https://web.archive.org/", "http://web.archive.org/")
                try:
                    r = requests.get(alt, timeout=timeout, headers={
                        "User-Agent": "Mozilla/5.0 (compatible; DA-Scraper/1.0)",
                        "Accept": "text/html,application/xhtml+xml"
                    }, allow_redirects=True, verify=True)
                    r.raise_for_status()
                    return r.text
                except Exception as exc2:
                    last_exc = exc2
            if attempt < retries - 1:
                time.sleep(1.0 * (attempt + 1))
                continue
            raise
        except requests.exceptions.RequestException as exc:
            last_exc = exc
            if attempt < retries - 1:
                time.sleep(1.0 * (attempt + 1))
                continue
            raise


def html_to_md(html: str) -> str:
    return md(html or "", heading_style="ATX", strip=["script", "style"]).strip()


def parse_index(html: str) -> Tuple[list[str], list[str]]:
    """Return (post_urls, date_strs) from an index page HTML.

    - post_urls are Wayback-relative like "/web/…/http://www.dyslexiaaction.org.uk/page/..."
    - date_strs like "Monday, 5 December, 2016 - 14:18"
    """
    # Limit to the title anchors inside listing rows to avoid menu links
    hrefs = re.findall(
        r'<div class="views-field views-field-title">\s*<span class="field-content">\s*<a href="(/web/\d+/http://www\.dyslexiaaction\.org\.uk/(?:page|news)/[^"]+)"',
        html,
        flags=re.I | re.S,
    )
    # Deduplicate while preserving order (should be one per row, but keep safe)
    post_urls: list[str] = []
    seen = set()
    for h in hrefs:
        if h not in seen:
            post_urls.append(h)
            seen.add(h)

    # Dates extracted from the index rows
    date_strs = re.findall(
        r'<div class="views-field views-field-created">\s*<span class="field-content">(.*?)</span>',
        html,
        flags=re.S | re.I,
    )
    return post_urls, [re.sub(r"\s+", " ", d).strip() for d in date_strs]


def normalize_date(date_str: str) -> str:
    """Convert 'Monday, 5 December, 2016 - 14:18' -> '2016-12-05'."""
    # Isolate the day-month-year part and parse without time.
    m = re.search(r"(\d{1,2})\s+([A-Za-z]+),?\s+(\d{4})", date_str)
    if not m:
        # Fallback: today
        return dt.date.today().isoformat()
    day, month_name, year = m.group(1), m.group(2), m.group(3)
    try:
        d = dt.datetime.strptime(f"{day} {month_name} {year}", "%d %B %Y").date()
    except Exception:
        return dt.date.today().isoformat()
    return d.isoformat()


def strip_wayback_prefix(url: str) -> str:
    """Return the original URL without the Wayback prefix if present."""
    m = re.match(r"https?://web\.archive\.org/web/\d+/(https?://.+)", url)
    if m:
        return m.group(1)
    m2 = re.match(r"/web/\d+/(https?://.+)", url)
    if m2:
        return m2.group(1)
    return url


def extract_title(html: str) -> str:
    # Prefer the hero-title wrapper, fallback to first h1
    m = re.search(r"<div class=\"hero-title\">\s*<h1>(.*?)</h1>", html, flags=re.S | re.I)
    if m:
        return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(1))).strip()
    m2 = re.search(r"<h1[^>]*>(.*?)</h1>", html, flags=re.S | re.I)
    if m2:
        return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m2.group(1))).strip()
    return "Untitled"


def extract_body_html(html: str) -> str | None:
    # First try trafilatura main content extraction (as HTML/XML)
    try:
        main = extract(html, include_comments=False, output_format='xml')
        if not main:
            main = extract(html, include_comments=False, output_format='html')
        if not main:
            main = extract(html, include_comments=False, output_format='text')
        return main
    except Exception:
        pass

    # Fallback: attempt to capture Drupal body field
    m = re.search(
        r'<div class=\"field field-name-body[^>]*>\s*<div class=\"field-items\">\s*<div class=\"field-item[^>]*>(.*?)</div>',
        html,
        flags=re.S | re.I,
    )
    if m:
        return m.group(1)
    return None


def write_post(date_iso: str, title: str, body_md: str, canonical: str) -> None:
    year = date_iso[:4]
    slug = slugify(title or "untitled", max_length=80)
    nid = f"da-{date_iso.replace('-', '')}-{slug}"

    dest_dir = OUT_CONTENT / year / slug
    dest_md = dest_dir / "index.md"
    dest_txt = OUT_PLAIN / f"{nid}.txt"

    dest_dir.mkdir(parents=True, exist_ok=True)
    fm = {
        "id": nid,
        "title": title,
        "date": date_iso,
        "source": {"name": "Dyslexia Action Tech Blog", "url": INDEX_URL_BASE},
        "canonical_url": canonical,
        "tags": [],
        "language": "en",
        "license": "Unknown",
        "original_format": "html",
    }

    post = frontmatter.Post(body_md, **fm)
    dest_md.write_text(frontmatter.dumps(post), encoding="utf-8")

    # Plain text (simple whitespace normalization)
    plain = re.sub(r"(?m)^\s*$", "\n", re.sub(r"\s+", " ", re.sub(r"\r", "", post.content.strip())))
    dest_txt.write_text(plain, encoding="utf-8")

    print(f"[OK]   {nid} -> {dest_md.relative_to(ROOT)}")


def find_next_index_href(html: str) -> str | None:
    m = re.search(r'<li class=\"pager-next\">\s*<a[^>]+href=\"([^\"]+)\"', html, flags=re.I)
    if m:
        return m.group(1)
    return None


def discover_index_urls(start_url: str, limit: int = 20) -> list[str]:
    """Discover all paginated index page URLs by following pager links on Wayback.

    Returns absolute Wayback URLs for each index page variant.
    """
    urls: list[str] = []
    seen: set[str] = set()
    queue: list[str] = [start_url]
    while queue and len(urls) < limit:
        u = queue.pop(0)
        if u in seen:
            continue
        seen.add(u)
        try:
            html = http_get(u)
        except Exception as exc:
            print(f"[WARN] index fetch failed {u}: {exc}")
            continue
        urls.append(u)
        # collect pager links (both numbered and next/last)
        for href in re.findall(r'<li class=\"pager-(?:item|next|last)\">\s*<a[^>]+href=\"([^\"]+)\"', html, flags=re.I):
            full = href if href.startswith("http") else f"{WAYBACK_BASE}{href}"
            if full not in seen:
                queue.append(full)
    return urls


def fetch_index_for_page(page_num: int) -> tuple[str, str]:
    """Return (url, html) for an index listing page, trying known snapshots.

    Ensures we hit a capture that actually contains listing content.
    """
    base_http = "http://www.dyslexiaaction.org.uk/tech-blog"
    http_url = base_http if page_num == 0 else f"{base_http}?page={page_num}"
    last_exc: Exception | None = None
    for snap in SNAPSHOTS:
        url = f"{WAYBACK_BASE}/web/{snap}/{http_url}"
        try:
            html = http_get(url)
        except Exception as exc:
            last_exc = exc
            continue
        # Quick heuristic: expect at least one listing title container
        if re.search(r'<div class="views-field views-field-title">', html, flags=re.I):
            return url, html
    # Fallback to latest attempt even if no marker
    if last_exc:
        raise last_exc
    # As a last resort, just return the first URL with empty html
    return f"{WAYBACK_BASE}/web/{SNAPSHOTS[0]}/{http_url}", ""


def run(start_page: int, end_page: int, force: bool = False) -> None:
    # Discover all index page URLs via pager links
    # Process each requested page directly using fallback snapshots
    for p in range(start_page, end_page + 1):
        try:
            use_url, html = fetch_index_for_page(p)
        except Exception as exc:
            print(f"[WARN] index fetch failed for page {p}: {exc}")
            continue
        print(f"[INDEX] page {p}: {use_url}")
        (RAW_DIR / f"index-page{p}.html").write_text(html, encoding="utf-8")
        post_urls, date_strs = parse_index(html)
        if len(post_urls) > len(date_strs):
            post_urls = post_urls[: len(date_strs)]
        print(f"  posts: {len(post_urls)}, dates: {len(date_strs)}")

        for i, (rel_url, dstr) in enumerate(zip(post_urls, date_strs), start=1):
            full_url = rel_url if rel_url.startswith("http") else f"{WAYBACK_BASE}{rel_url}"
            canonical = strip_wayback_prefix(full_url)
            date_iso = normalize_date(dstr)
            try:
                post_html = http_get(full_url)
                (RAW_DIR / f"post-p{p}-{i:02d}.html").write_text(post_html, encoding="utf-8")
                title = extract_title(post_html)
            except Exception as exc:
                print(f"[WARN] fetch failed for {full_url}: {exc}")
                continue

            slug = slugify((title or "untitled"), max_length=80)
            year = date_iso[:4]
            dest_md = (OUT_CONTENT / year / slug / "index.md")
            if dest_md.exists() and not force:
                print(f"[SKIP] {year}/{slug} (exists)")
                continue

            body_html = extract_body_html(post_html) or ""
            body_md = html_to_md(body_html)
            write_post(date_iso, title or "Untitled", body_md, canonical)
            time.sleep(0.1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="overwrite existing outputs")
    parser.add_argument("--pages", nargs=2, type=int, metavar=("START", "END"), help="page range inclusive (default 0 7)")
    args = parser.parse_args()
    start, end = (0, 7) if not args.pages else (args.pages[0], args.pages[1])
    run(start, end, force=args.force)
