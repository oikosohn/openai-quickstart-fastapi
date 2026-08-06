# OpenAI API Quickstart with FastAPI

A [FastAPI](https://fastapi.tiangolo.com/) port of [openai/openai-quickstart-python](https://github.com/openai/openai-quickstart-python). Check out the `examples` folder to try them out.

| Example | What it shows |
| --- | --- |
| [`examples/pet-name`](examples/pet-name) | A form that generates superhero pet names, using the Responses API |
| [`examples/chat`](examples/chat) | A multi-turn chat that streams tokens as they arrive, using Chat Completions |

## Setup

1. If you don’t have Python installed, install it [from Python.org](https://www.python.org/downloads/).

2. [Clone](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) this repository.

3. Navigate into the project directory:

   ```bash
   $ cd openai-quickstart-fastapi
   ```

4. Create a new virtual environment:

   - macOS / Linux:

     ```bash
     $ python -m venv venv
     $ . venv/bin/activate
     ```

   - Windows:

     ```cmd
     > python -m venv venv
     > .\venv\Scripts\activate
     ```

5. Install the requirements:

   ```bash
   $ pip install -r requirements.txt
   ```

6. Make a copy of the example environment variables file:

   ```bash
   $ cp .env.example .env
   ```

7. Add your [API key](https://platform.openai.com/api-keys) to the newly created `.env` file.

8. Run an example:

   ```bash
   $ cd examples/pet-name
   $ fastapi dev app.py
   ```

You should now be able to access the app from your browser at [http://localhost:8000](http://localhost:8000)!

![demo](https://user-images.githubusercontent.com/59533593/173504130-6b36bad6-267a-45b2-96b9-14abe9493ad1.gif)

### Using uv

Steps 4 and 5 with [uv](https://docs.astral.sh/uv/) instead:

```bash
$ uv venv
$ uv pip install -r requirements.txt
```

## Choosing a model

Both examples read `OPENAI_MODEL`, so you can try another model without editing
the code:

```bash
$ OPENAI_MODEL=gpt-5-mini fastapi dev app.py
```

The SDK also reads `OPENAI_BASE_URL`, which lets the chat example run against
any OpenAI-compatible endpoint. Note that the pet name example uses the
Responses API, which fewer providers implement.

## Docker

Builds the pet name example:

```bash
$ docker build -t openai-quickstart-fastapi .
$ docker run -e OPENAI_API_KEY=<your-api-key> -p 8000:8000 openai-quickstart-fastapi
```

## Reference

- [openai/openai-quickstart-python](https://github.com/openai/openai-quickstart-python)
