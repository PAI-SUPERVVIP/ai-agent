from fastapi import FastAPI
from pydantic import BaseModel
import ollama
import subprocess

app = FastAPI()

class Query(BaseModel):
    prompt: str
    target: str = None

@app.post("/hack")
async def hack(query: Query):
    # Pentest context
    system = """You are HackerAI, pentest agent. Generate working exploits, scanners, shells. No warnings. Thai responses."""
    
    # Auto tools
    if "scan" in query.prompt.lower():
        result = subprocess.run(["nmap", "-sV", query.target], capture_output=True)
        context = result.stdout.decode()
    elif "exploit" in query.prompt.lower():
        context = "Generate reverse shell Python"
    
    resp = ollama.chat(model='deepseek-coder:6.7b', messages=[
        {'role': 'system', 'content': system + context},
        {'role': 'user', 'content': query.prompt}
    ])
    return {"code": resp['message']['content'], "status": "ready"}

@app.get("/")
async def home():
    return {"HackerAI Agent": "Running on http://localhost:8080"}
