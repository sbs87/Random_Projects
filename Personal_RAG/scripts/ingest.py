# scripts/ingest.py
import os, re, json, hashlib
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Iterator

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader
import frontmatter

DATA_DIR = Path("data")
STORE_DIR = Path("store")
EMB_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

def normalize(text: str) -> str:
    # de-hyphenate line breaks like "bio-\ninformatics"
    text = re.sub(r'-\n', '', text)
    # join wrapped lines
    text = re.sub(r'\s*\n\s*', ' ', text)
    # collapse spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def chunk_recursive(text: str, max_tokens=800, overlap=150) -> List[str]:
    # naive token estimate via words (fine for MVP)
    words = text.split()
    chunks = []
    i = 0
    step = max_tokens - overlap
    while i < len(words):
        chunk = " ".join(words[i:i+max_tokens])
        chunks.append(chunk)
        i += step
    return chunks

def pdf_docs() -> Iterator[Dict]:
    for pdf_path in (DATA_DIR/"pdfs").glob("**/*.pdf"):
        reader = PdfReader(str(pdf_path))
        for p, page in enumerate(reader.pages):
            raw = page.extract_text() or ""
            txt = normalize(raw)
            if not txt.strip():
                continue
            for c in chunk_recursive(txt):
                yield {
                    "text": c,
                    "metadata": {
                        "source": str(pdf_path),
                        "doc_type": "pdf",
                        "title": pdf_path.stem,
                        "page": p+1,
                        "section": None,
                        "created_at": datetime.fromtimestamp(pdf_path.stat().st_mtime).strftime("%Y-%m-%d"),
                        "tags": ["pdf"]
                    }
                }

def md_docs() -> Iterator[Dict]:
    for md_path in (DATA_DIR/"notes").glob("**/*.md"):
        post = frontmatter.load(md_path)
        title = post.get("title", md_path.stem)
        created = post.get("date")
        tags = post.get("tags", [])
        text = normalize(post.content)
        # VERY SIMPLE: split by H2/H3 as separators; improve later
        sections = re.split(r'\n(?=## )', text) if "## " in text else [text]
        for sec in sections:
            # derive a section title
            sec_title = None
            m = re.match(r'^\s*(#+)\s*(.+)', sec)
            if m:
                sec_title = m.group(2).strip()
            for c in chunk_recursive(sec):
                yield {
                    "text": c,
                    "metadata": {
                        "source": str(md_path),
                        "doc_type": "markdown",
                        "title": title,
                        "page": None,
                        "section": sec_title,
                        "created_at": created or datetime.fromtimestamp(md_path.stat().st_mtime).strftime("%Y-%m-%d"),
                        "tags": ["notes"] + (tags if isinstance(tags, list) else [tags])
                    }
                }

def build_index(items: List[Dict], model_name=EMB_MODEL):
    model = SentenceTransformer(model_name)
    texts = [it["text"] for it in items]
    X = model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)  # cosine
    dim = X.shape[1]
    index = faiss.IndexFlatIP(dim)  # inner product with normalized = cosine
    index.add(X.astype(np.float32))
    # persist
    STORE_DIR.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(STORE_DIR/"faiss.index"))
    with open(STORE_DIR/"meta.jsonl", "w") as f:
        for it in items:
            f.write(json.dumps(it)+"\n")
    print(f"Indexed {len(items)} chunks. Dim={dim}")


## the following is alternative to faiss
# swap-in for build_index / retrieve
# from chromadb import Client
# from chromadb.config import Settings
# from sentence_transformers import SentenceTransformer

# chroma = Client(Settings(persist_directory="store/chroma"))
# collection = chroma.get_or_create_collection("personal")

# model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# def add_to_chroma(items):
#     texts = [it["text"] for it in items]
#     embs = model.encode(texts, convert_to_numpy=True).tolist()
#     ids = [str(i) for i in range(len(items))]
#     metas = [it["metadata"] for it in items]
#     collection.add(ids=ids, documents=texts, embeddings=embs, metadatas=metas)

# def chroma_search(query, k=6):
#     qemb = model.encode([query], convert_to_numpy=True).tolist()[0]
#     return collection.query(query_embeddings=[qemb], n_results=k)
### end alt 


if __name__ == "__main__":
    items = list(pdf_docs()) + list(md_docs())
    build_index(items)
