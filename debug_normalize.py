#!/usr/bin/env python3
import pathlib
import frontmatter
import sys

REPO = pathlib.Path("/Users/dominiklukes/gitrepos/dominiklukes-llmstxt").resolve()
CONTENT = REPO / "content"

print(f"REPO: {REPO}")
print(f"CONTENT: {CONTENT}")
print(f"REPO exists: {REPO.exists()}")
print(f"CONTENT exists: {CONTENT.exists()}")

if CONTENT.exists():
    indices = list(CONTENT.rglob("index.md"))
    print(f"Found {len(indices)} index.md files")
    
    for i, idx in enumerate(indices[:5]):  # Show first 5
        print(f"  {i+1}. {idx}")
        try:
            p = frontmatter.load(idx)
            print(f"     Title: {p.metadata.get('title', 'No title')}")
            print(f"     Source: {p.metadata.get('source', 'No source')}")
        except Exception as e:
            print(f"     ERROR: {e}")
else:
    print("Content directory does not exist")
