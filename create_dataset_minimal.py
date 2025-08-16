#!/usr/bin/env python3
"""Minimal normalization script to create the dataset files."""

import pathlib
import json
import datetime
import frontmatter

REPO = pathlib.Path("/Users/dominiklukes/gitrepos/dominiklukes-llmstxt").resolve()
CONTENT = REPO / "content"
PLAIN = REPO / "plain"
DATASET = REPO / "dataset"
STATIC = REPO / "static"

# Ensure directories exist
DATASET.mkdir(parents=True, exist_ok=True)
STATIC.mkdir(parents=True, exist_ok=True)

def main():
    print("Loading posts...")
    posts = []
    
    for idx in sorted(CONTENT.rglob("index.md")):
        try:
            p = frontmatter.load(idx)
            meta = dict(p.metadata or {})
            
            post_id = meta.get("id") or f"post-{len(posts)}"
            title = meta.get("title", "Untitled")
            date = str(meta.get("date", ""))[:10]
            source_data = meta.get("source", {})
            source = source_data.get("name") if isinstance(source_data, dict) else str(source_data or "unknown")
            canonical_url = meta.get("canonical_url", "")
            
            # Try to get plain text version
            plain_path = PLAIN / f"{post_id}.txt"
            if plain_path.exists():
                text = plain_path.read_text(encoding="utf-8", errors="ignore")
            else:
                text = p.content or ""
            
            posts.append({
                "id": post_id,
                "title": title,
                "date": date,
                "url": canonical_url,
                "source": source,
                "tags": meta.get("tags", []),
                "language": meta.get("language", "en"),
                "license": meta.get("license", "CC-BY-4.0"),
                "text": text.strip()
            })
            
        except Exception as e:
            print(f"Error processing {idx}: {e}")
            continue
    
    print(f"Loaded {len(posts)} posts")
    
    # Write JSONL
    corpus_path = DATASET / "corpus.jsonl"
    with corpus_path.open("w", encoding="utf-8") as f:
        for post in sorted(posts, key=lambda x: x["date"]):
            f.write(json.dumps(post, ensure_ascii=False) + "\n")
    
    # Write manifest
    manifest = {
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "n_documents": len(posts)
    }
    (DATASET / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    
    # Write dedupe summary (simplified)
    summary = {
        "loaded": len(posts),
        "final": len(posts),
        "dropped_pairs": []
    }
    (DATASET / "dedupe_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    
    # Write llms.txt
    llms_content = f"""# llms.txt — index of available machine-readable artifacts

## Dataset
- dataset/corpus.jsonl

## Plain-text mirrors
- plain/  (one file per article where available)

## Notes
- Prefer `url` (canonical_url) for external citation if present.
- License defaults to CC-BY-4.0 unless specified per document.

## Documents (top 200)
"""
    
    for post in posts[:200]:
        llms_content += f"- id: {post['id']}  source: {post['source']}  date: {post['date']}\n"
    
    (STATIC / "llms.txt").write_text(llms_content, encoding="utf-8")
    
    # Write full listing
    full_listing = "\n".join([f"{p['id']}\t{p['date']}\t{p['source']}\t{p['url']}" for p in posts])
    (STATIC / "llms-full.txt").write_text(full_listing, encoding="utf-8")
    
    print("Files created:")
    print(f"- {corpus_path} ({len(posts)} documents)")
    print(f"- {DATASET / 'manifest.json'}")
    print(f"- {DATASET / 'dedupe_summary.json'}")
    print(f"- {STATIC / 'llms.txt'}")
    print(f"- {STATIC / 'llms-full.txt'}")
    print("Done!")

if __name__ == "__main__":
    main()
