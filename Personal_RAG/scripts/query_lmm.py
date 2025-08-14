"""
Script to send a prompt to a local LLM server and get a response.

Steve Smith
August 2025

query_lmm.py --prompt_file prompt/prompt.txt

"""
import requests, json   
import argparse


parser = argparse.ArgumentParser(description="Send query to an LLLM.")
parser.add_argument("--prompt_file",  type=str, help="Input file prompt to send to LLM. Can be RAG-assocaited.")
args = parser.parse_args()
prompt_file=args.prompt_file


def generate(prompt, model="llama3"):
    if model=="llama3":
        r = requests.post("http://localhost:11434/api/generate", json={"model":"llama3","prompt":prompt, "stream":False})
        return r.json()["response"]
    
    #TODO add other providers like local LLMs, etc

if __name__ == "__main__":
    with open(prompt_file, 'r') as f:
        prompt = f.read().strip()
    #prompt = "What is the capital of France?"
    response = generate(prompt)
    print(response)