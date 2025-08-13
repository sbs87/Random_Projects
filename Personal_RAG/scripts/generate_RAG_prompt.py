"""
Script to generate a prompt for an LLM based on RAG.
Reads a question from a text file, retrieves relevant context chunks from the indexed documents,
and formats a prompt for the LLM.

Steve Smith
August 2025
generate_RAG_prompt.py --question_file questions/q1.txt

"""
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from pathlib import Path
import argparse

#TODO make the folloiwng configurable: 
## STORE_DIR, PROMPT_DIR, K, EMB_MODEL, index and meta paths
## basic analytics like how RAG docs were chosen, number of chunks, avg chunk size, etc

# Variables
STORE_DIR = Path("store")
PROMPT_DIR = Path("prompt")
EMB_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Arguments
parser = argparse.ArgumentParser(description="Query the RAG system with a question.")
parser.add_argument("--question_file", type=str, help="Path to a text file containing the question.")
parser.add_argument("--prompt_file", default="prompt.txt", type=str, help="Output file to the RAG-assocated prompt.")
parser.add_argument("--k", default=6, type=int, help="Number of context chunks to retrieve.")
args = parser.parse_args()
prompt_dir_str = str(PROMPT_DIR)
prompt_outfile = f"{prompt_dir_str}/{args.prompt_file}"
question_file=args.question_file
K = args.k

# Functions
## Loads previously built index and metadata for RAG retrieval
def load_index():
    index = faiss.read_index(str(STORE_DIR/"faiss.index"))
    metas = [json.loads(l) for l in open(STORE_DIR/"meta.jsonl")]
    return index, metas

## Retirves top-k relevant context chunks for a given question
def retrieve(question: str, k=K):
    model = SentenceTransformer(EMB_MODEL)
    q = model.encode([question], convert_to_numpy=True, normalize_embeddings=True).astype(np.float32)
    index, metas = load_index()
    D, I = index.search(q, k)
    ctx = [metas[i] for i in I[0]]
    return ctx

## Formats the prompt for the LLM using the question and retrieved contexts
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
    # Read in the question
    with open(question_file, "r") as f:
        q = f.read().strip()
    # Retireve context and format prompt
    ctxs = retrieve(q)
    prompt = format_prompt(q, ctxs)

    # Output the prompt to a file
    with open(prompt_outfile, "w") as f:
        f.write(prompt)
    print(f"Wrote {prompt_outfile}. Use this with your LLM of choice.")