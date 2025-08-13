# scripts/query.py
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from pathlib import Path

STORE_DIR = Path("store")
K = 6
EMB_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

def load_index():
    index = faiss.read_index(str(STORE_DIR/"faiss.index"))
    metas = [json.loads(l) for l in open(STORE_DIR/"meta.jsonl")]
    return index, metas

def retrieve(question: str, k=K):
    model = SentenceTransformer(EMB_MODEL)
    q = model.encode([question], convert_to_numpy=True, normalize_embeddings=True).astype(np.float32)
    index, metas = load_index()
    D, I = index.search(q, k)
    ctx = [metas[i] for i in I[0]]
    return ctx

def format_prompt(question, contexts):
    bullets = []
    for c in contexts:
        md = c["metadata"]
        src = f'{md["title"]} (p.{md["page"]})' if md["page"] else md["title"]
        bullets.append(f"[{src}] {c['text']}")
    context_text = "\n\n---\n".join(bullets)
    return f"""You are a helpful assistant. Use only the CONTEXT to answer.

QUESTION:
{question}

CONTEXT:
{context_text}

If insufficient context, say so and ask for the right file."""
    
if __name__ == "__main__":
    q = input("Ask: ")
    ctxs = retrieve(q)
    prompt = format_prompt(q, ctxs)
    with open("prompt.txt", "w") as f:
        f.write(prompt)