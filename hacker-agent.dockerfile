FROM ollama/ollama
RUN ollama pull deepseek-coder:6.7b
RUN ollama pull mistral:7b

# Web UI + API
RUN apt update && apt install -y nodejs npm python3 python3-pip
RUN npm i -g express ollama-js
RUN pip install flask fastapi uvicorn

COPY agent.py /app/
COPY webui.html /app/
WORKDIR /app
EXPOSE 8080 11434
CMD ollama serve & uvicorn agent:app --host 0.0.0.0 --port 8080
