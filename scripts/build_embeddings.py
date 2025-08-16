#!/usr/bin/env python3
"""
Build embeddings and FAISS index from dataset/corpus.jsonl

Dependencies:
  pip install openai tqdm ujson numpy faiss-cpu

Environment:
  OPENAI_API_KEY - required for OpenAI embeddings
"""
import json
import os
import pathlib
import sys
from typing import List, Dict, Any
import numpy as np
import openai
from tqdm import tqdm

try:
    import faiss
except ImportError:
    print("ERROR: faiss-cpu not installed. Run: pip install faiss-cpu")
    sys.exit(1)

REPO = pathlib.Path(".").resolve()
DATASET = REPO / "dataset"
CORPUS_FILE = DATASET / "corpus.jsonl"
EMBEDDINGS_FILE = DATASET / "embeddings.jsonl"
FAISS_INDEX_FILE = DATASET / "faiss.index"
FAISS_IDS_FILE = DATASET / "faiss_ids.json"

def load_corpus() -> List[Dict[str, Any]]:
    """Load corpus from JSONL file."""
    if not CORPUS_FILE.exists():
        print(f"ERROR: {CORPUS_FILE} not found")
        sys.exit(1)
    
    docs = []
    with CORPUS_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                docs.append(json.loads(line))
    
    print(f"Loaded {len(docs)} documents from {CORPUS_FILE}")
    return docs

def get_embeddings(texts: List[str], model: str = "text-embedding-3-small") -> List[List[float]]:
    """Get embeddings from OpenAI API."""
    client = openai.OpenAI()
    
    embeddings = []
    batch_size = 100  # OpenAI batch limit
    
    for i in tqdm(range(0, len(texts), batch_size), desc="Getting embeddings"):
        batch_texts = texts[i:i + batch_size]
        
        try:
            response = client.embeddings.create(
                model=model,
                input=batch_texts
            )
            
            batch_embeddings = [data.embedding for data in response.data]
            embeddings.extend(batch_embeddings)
            
        except Exception as e:
            print(f"ERROR getting embeddings for batch {i//batch_size}: {e}")
            # Add zero vectors as fallback
            embeddings.extend([[0.0] * 1536] * len(batch_texts))
    
    return embeddings

def build_faiss_index(embeddings: List[List[float]], doc_ids: List[str]) -> None:
    """Build and save FAISS index."""
    embeddings_array = np.array(embeddings, dtype=np.float32)
    
    # Create FAISS index
    dimension = embeddings_array.shape[1]
    index = faiss.IndexFlatIP(dimension)  # Inner product (cosine similarity)
    
    # Normalize vectors for cosine similarity
    faiss.normalize_L2(embeddings_array)
    
    # Add embeddings to index
    index.add(embeddings_array)
    
    # Save index
    faiss.write_index(index, str(FAISS_INDEX_FILE))
    
    # Save document IDs mapping
    with FAISS_IDS_FILE.open("w", encoding="utf-8") as f:
        json.dump(doc_ids, f, ensure_ascii=False, indent=2)
    
    print(f"Built FAISS index with {index.ntotal} vectors")
    print(f"Saved index to {FAISS_INDEX_FILE}")
    print(f"Saved ID mapping to {FAISS_IDS_FILE}")

def main():
    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("ERROR: OPENAI_API_KEY environment variable not set")
        sys.exit(1)
    
    # Load corpus
    docs = load_corpus()
    
    # Prepare texts for embedding
    texts = []
    doc_ids = []
    
    for doc in docs:
        # Combine title and text for better embeddings
        title = doc.get("title", "")
        text = doc.get("text", "")
        combined_text = f"{title}\n\n{text}".strip()
        
        texts.append(combined_text)
        doc_ids.append(doc["id"])
    
    # Get embeddings
    print("Getting embeddings from OpenAI...")
    embeddings = get_embeddings(texts)
    
    # Save embeddings to JSONL
    with EMBEDDINGS_FILE.open("w", encoding="utf-8") as f:
        for i, (doc, embedding) in enumerate(zip(docs, embeddings)):
            entry = {
                "id": doc["id"],
                "embedding": embedding
            }
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    
    print(f"Saved embeddings to {EMBEDDINGS_FILE}")
    
    # Build FAISS index
    print("Building FAISS index...")
    build_faiss_index(embeddings, doc_ids)
    
    print("Done!")

if __name__ == "__main__":
    main()
