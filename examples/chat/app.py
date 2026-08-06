import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from openai import OpenAI

load_dotenv()

# Relative to this file, not the working directory, so the app runs from anywhere.
HERE = Path(__file__).parent

app = FastAPI()
app.mount("/static", StaticFiles(directory=HERE / "static"), name="static")
templates = Jinja2Templates(directory=HERE / "templates")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Not a reasoning model, so tokens start arriving right away - which is the
# whole point of this example. Override with OPENAI_MODEL to try another one.
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

SYSTEM_MESSAGE = {"role": "system", "content": "You are a helpful assistant."}


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.post("/chat")
async def chat(request: Request):
    # The browser keeps the history and sends it back with every message, so the
    # server holds no per-user state and two visitors never share a conversation.
    messages = (await request.json())["messages"]

    def stream():
        with client.chat.completions.create(
            model=MODEL,
            messages=[SYSTEM_MESSAGE, *messages],
            stream=True,
        ) as chunks:
            for chunk in chunks:
                text = chunk.choices[0].delta.content
                if text:
                    yield text

    return StreamingResponse(stream(), media_type="text/plain")
