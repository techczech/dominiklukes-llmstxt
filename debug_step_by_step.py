#!/usr/bin/env python3
import sys
sys.path.append('/Users/dominiklukes/gitrepos/dominiklukes-llmstxt/scripts')

print("Starting debug run...")

try:
    print("Importing modules...")
    import pathlib, json, hashlib, datetime, re
    from rapidfuzz import fuzz
    import frontmatter
    print("Modules imported successfully")
    
    REPO = pathlib.Path("/Users/dominiklukes/gitrepos/dominiklukes-llmstxt").resolve()
    CONTENT = REPO / "content"
    PLAIN = REPO / "plain"
    
    print(f"REPO: {REPO}, exists: {REPO.exists()}")
    print(f"CONTENT: {CONTENT}, exists: {CONTENT.exists()}")
    print(f"PLAIN: {PLAIN}, exists: {PLAIN.exists()}")
    
    if CONTENT.exists():
        indices = list(CONTENT.rglob("index.md"))
        print(f"Found {len(indices)} index.md files")
        
        posts = []
        for i, idx in enumerate(indices[:3]):  # Process first 3 for debug
            print(f"Processing {idx}")
            try:
                p = frontmatter.load(idx)
                meta = dict(p.metadata or {})
                title = meta.get("title", "No title")
                posts.append({
                    "id": f"test-{i}",
                    "title": str(title),
                    "date": str(meta.get("date", ""))[:10],
                    "source": str((meta.get("source") or {}).get("name") or "unknown"),
                    "text": "Sample text"
                })
                print(f"  Loaded: {title[:30]}...")
            except Exception as e:
                print(f"  ERROR: {e}")
        
        print(f"Successfully processed {len(posts)} posts")
        
    print("Debug run completed successfully")
    
except Exception as e:
    print(f"ERROR in debug run: {e}")
    import traceback
    traceback.print_exc()
