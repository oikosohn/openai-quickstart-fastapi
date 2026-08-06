import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
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

MODEL = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")


@app.get("/", response_class=HTMLResponse)
def index(request: Request, result: str | None = None):
    return templates.TemplateResponse(
        request=request, name="index.html", context={"result": result}
    )


@app.post("/")
def generate(request: Request, animal: str = Form(...)):
    response = client.responses.create(
        model=MODEL,
        input=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": generate_prompt(animal)},
        ],
    )
    result = response.output_text
    # Post/Redirect/Get: answer the POST with a redirect so a reload or a Back
    # navigation re-runs the GET instead of resubmitting the previous animal.
    url = request.url_for("index").include_query_params(result=result)
    return RedirectResponse(url, status_code=303)


def generate_prompt(animal):
    return (
        f"Suggest three superhero names for this {animal}, in the style of "
        "'Captain Sharpclaw, Agent Fluffball, The Incredible Feline' for a cat. "
        "Reply with only the three names, separated by commas."
    )
