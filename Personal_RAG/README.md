# Purpose
Query an LLM based on personal RAG prompt

Note several files are not in github.

The structure is as follows
```
Personal_RAG/
├── data/
│   └── ...                # Data files (not in GitHub) includes subdirs like pdf/ and txt/
├── prompt/
│   └── prompt.txt        # Prompt with 'question_file' and personal document RAG (top k documents)
│   └── question_file.txt # Question to ask LLM without RAG info
├── scripts/
│   ├── ingest.py
│   ├── query.py
│   └── query_lmm.py
├── store/
│   ├── faiss.index   # Embeddings index of personal documents in data/
│   └── meta.jsonl.   # Assocaited metadata of personal documents in data/
├── README.md

```

# Usage
## Step 1
`python3 scripts/ingest.py`
## Step 2
`python3 scripts/query.py --question_file question_file`
## Step 3
`python scripts/query_lmm.py --prompt_file prompt/prompt.txt`

# Author and Date
Steve Smith, August 2025