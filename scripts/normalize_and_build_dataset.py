#!/usr/bin/env python3
"""
Normalize content/* -> dataset/corpus.jsonl with deduplication & canonicalization.

Places:
 - reads: content/**/index.md  (front matter + markdown content)
 - prefers plain mirrors: plain/*.txt (if available)
 - writes: dataset/corpus.jsonl (one JSON object per line)
 - writes: dataset/manifest.json (summary)
 - writes: static/llms.txt and static/llms-full.txt

Canonical preference order (when collapsing duplicates):
  1) Metaphor Hacker
  2) Medium
  3) Substack
  4) other (alphabetical)

Near-duplicate threshold: RAPIDFUZZ partial_ratio >= 95 (applies to first 4000 chars)
Exact duplicate: SHA256 of final_text

Dependencies:
  pip install python-frontmatter rapidfuzz
"""
from __future__ import annotations
import pathlib, json, hashlib, datetime, re, sys
from rapidfuzz import fuzz
import frontmatter

REPO = pathlib.Path(".").resolve()
CONTENT = REPO / "content"
PLAIN = REPO / "plain"
DATASET = REPO / "dataset"
STATIC = REPO / "static"
DATASET.mkdir(parents=True, exist_ok=True)
STATIC.mkdir(parents=True, exist_ok=True)

OUT_JSONL = DATASET / "corpus.jsonl"
MANIFEST = DATASET / "manifest.json"
LLMS = STATIC / "llms.txt"
LLMS_FULL = STATIC / "llms-full.txt"

# canonical ordering map
SOURCE_RANK = {
    "Metaphor Hacker": 1,
    "Medium": 2,
    "Substack": 3
}
DEFAULT_SOURCE_RANK = 99

# near-duplicate threshold and sampling length
NEAR_DUP_THRESHOLD = 95
SAMPLE_CHARS = 4000

def md_to_text(md_body: str) -> str:
    # Very conservative Markdown -> plain text cleaning.
    t = md_body
    # remove YAML if present
    t = re.sub(r"(?s)^---\n.*?\n---\n", "", t).strip()
    # images -> alt text
    t = re.sub(r'!\[([^\]]*)\]\([^)]+\)', r'\1', t)
    # links -> text (url)
    t = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\1 (\2)', t)
    # code fences -> keep inner
    t = re.sub(r'```[^\n]*\n(.*?)```', r'\1', t, flags=re.S)
    # inline code ticks
    t = t.replace("`", "")
    # headings -> remove #
    t = re.sub(r'^\s*#{1,6}\s*', '', t, flags=re.M)
    # blockquote markers
    t = re.sub(r'^\s*>+\s?', '', t, flags=re.M)
    # multiple blank lines -> two
    t = re.sub(r'\n{3,}', '\n\n', t)
    # trim excessive whitespace
    t = re.sub(r'[ \t]+$', '', t, flags=re.M)
    return t.strip()

def load_posts():
    posts = []
    for idx in sorted(CONTENT.rglob("index.md")):
        try:
            p = frontmatter.load(idx)
        except Exception as e:
            print(f"[WARN] failed reading {idx}: {e}", file=sys.stderr)
            continue
        # Resolve fields
        meta = dict(p.metadata or {})
        title = meta.get("title") or p.get("title") or ""
        date = meta.get("date") or meta.get("publishDate") or ""
        try:
            # normalize date to YYYY-MM-DD if possible
            date = str(date)[:10]
        except Exception:
            date = ""
        source_data = meta.get("source", {})
        if isinstance(source_data, dict):
            source = source_data.get("name") or "unknown"
        else:
            source = str(source_data) if source_data else "unknown"
        canonical = meta.get("canonical_url") or meta.get("url") or meta.get("permalink") or ""
        pid = meta.get("id") or f"{date.replace('-','')}-{idx.parent.name}"
        # prefer plain mirror if exists
        plain_path = PLAIN / f"{pid}.txt"
        if plain_path.exists():
            text = plain_path.read_text(encoding="utf-8")
        else:
            text = md_to_text(p.content or "")
        # fallback to short summary if text empty
        if not text:
            text = (meta.get("summary") or meta.get("description") or "").strip()
        posts.append({
            "repo_path": str(idx),
            "id": str(pid),
            "title": str(title),
            "date": str(date),
            "source": str(source),
            "canonical_url": str(canonical),
            "tags": meta.get("tags") or meta.get("categories") or [],
            "license": meta.get("license") or "CC-BY-4.0",
            "language": meta.get("language") or "en",
            "text": text
        })
    return posts

def text_hash(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def source_rank(name: str) -> int:
    return SOURCE_RANK.get(name, DEFAULT_SOURCE_RANK)

def choose_preferred(a: dict, b: dict) -> dict:
    """Return preferred doc between a and b according to canonical rules."""
    # If either has canonical_url that matches other's canonical_url and one is MH prefer MH
    # Primary: source rank (smaller is better)
    ra, rb = source_rank(a["source"]), source_rank(b["source"])
    if ra != rb:
        return a if ra < rb else b
    # Secondary: longer text (prefer more complete)
    if len(a["text"]) != len(b["text"]):
        return a if len(a["text"]) > len(b["text"]) else b
    # Tertiary: earlier date (prefer original)
    try:
        da = datetime.datetime.fromisoformat(a["date"]) if a["date"] else None
        db = datetime.datetime.fromisoformat(b["date"]) if b["date"] else None
        if da and db and da != db:
            return a if da < db else b
    except Exception:
        pass
    # fallback: stable by id
    return a if a["id"] <= b["id"] else b

def deduplicate_and_cluster(posts: list[dict]):
    # exact de-dupe map
    hash_map = {}   # hash -> representative id
    representatives = []  # list of representative docs
    dropped = []  # list of (kept_id, removed_id, reason)
    # first pass: exact hash dedupe
    for p in posts:
        h = text_hash(p["text"])
        if h in hash_map:
            kept = hash_map[h]
            # find kept doc and decide preferred
            kept_doc = next(x for x in representatives if x["id"] == kept)
            preferred = choose_preferred(kept_doc, p)
            if preferred["id"] == kept_doc["id"]:
                # keep existing, record removal
                dropped.append((kept_doc["id"], p["id"], "exact-hash"))
            else:
                # replace representative
                representatives = [x for x in representatives if x["id"] != kept_doc["id"]]
                representatives.append(p)
                hash_map[h] = p["id"]
                dropped.append((p["id"], kept_doc["id"], "exact-hash-replaced"))
        else:
            hash_map[h] = p["id"]
            representatives.append(p)

    # second pass: near-duplicate clustering
    final = []
    seen_ids = set()
    # We'll compare each representative to those already finalised
    for rep in representatives:
        if rep["id"] in seen_ids:
            continue
        rep_sample = rep["text"][:SAMPLE_CHARS]
        cluster = [rep]
        seen_ids.add(rep["id"])
        # compare to all other reps not yet seen
        for other in representatives:
            if other["id"] in seen_ids or other["id"] == rep["id"]:
                continue
            other_sample = other["text"][:SAMPLE_CHARS]
            score = fuzz.partial_ratio(rep_sample, other_sample)
            if score >= NEAR_DUP_THRESHOLD:
                # near duplicate -> pick preferred
                preferred = choose_preferred(cluster[0], other)
                # preferred becomes cluster[0]
                if preferred["id"] != cluster[0]["id"]:
                    # replace cluster[0]
                    dropped.append((preferred["id"], cluster[0]["id"], f"near-dup({score})"))
                    cluster[0] = preferred
                else:
                    dropped.append((cluster[0]["id"], other["id"], f"near-dup({score})"))
                seen_ids.add(other["id"])
        final.append(cluster[0])

    return final, dropped

def build_dataset(final_docs: list[dict]):
    # Write JSONL
    with OUT_JSONL.open("w", encoding="utf-8") as fh:
        for d in sorted(final_docs, key=lambda x: x.get("date","")):
            row = {
                "id": d["id"],
                "title": d["title"],
                "date": d["date"],
                "url": d["canonical_url"] or "",
                "source": d["source"],
                "tags": d.get("tags") or [],
                "language": d.get("language") or "en",
                "license": d.get("license") or "CC-BY-4.0",
                "text": d["text"]
            }
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    # Manifest
    manifest = {
        "generated_at": datetime.datetime.utcnow().isoformat()+"Z",
        "n_documents": len(final_docs)
    }
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

def write_llms_txt(final_docs: list[dict]):
    base = ""  # placeholder; we will write relative paths for now
    lines = []
    lines.append("# llms.txt — index of available machine-readable artifacts")
    lines.append("")
    lines.append("## Dataset")
    lines.append(f"- dataset/corpus.jsonl")
    lines.append("")
    lines.append("## Plain-text mirrors")
    lines.append("- plain/  (one file per article where available)")
    lines.append("")
    lines.append("## Notes")
    lines.append("- Prefer `url` (canonical_url) for external citation if present.")
    lines.append("- License defaults to CC-BY-4.0 unless specified per document.")
    lines.append("")
    lines.append("## Documents (top 200)")
    for d in final_docs[:200]:
        # safe slug display
        lines.append(f"- id: {d['id']}  source: {d['source']}  date: {d['date']}")
    LLMS.write_text("\n".join(lines), encoding="utf-8")
    # full listing
    LLMS_FULL.write_text("\n".join([f"{d['id']}\t{d['date']}\t{d['source']}\t{d.get('canonical_url','')}" for d in final_docs]), encoding="utf-8")

def main():
    print("[1/4] Loading posts from content/")
    posts = load_posts()
    print(f"  loaded {len(posts)} posts")
    print("[2/4] Deduplicating (exact + near-dup)")
    final_docs, dropped = deduplicate_and_cluster(posts)
    print(f"  final documents: {len(final_docs)}  dropped pairs: {len(dropped)}")
    # write dataset
    print("[3/4] Writing dataset/corpus.jsonl")
    build_dataset(final_docs)
    print("[4/4] Writing llms.txt and llms-full.txt")
    write_llms_txt(final_docs)
    # write log summary
    summary = {
        "loaded": len(posts),
        "final": len(final_docs),
        "dropped_pairs": dropped[:200]
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    (DATASET / "dedupe_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print("Done.")

if __name__ == "__main__":
    main()
