FROM python:3.10

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./examples/pet-name /code

# Pass the key at run time: docker run -e OPENAI_API_KEY=... -p 8000:8000 <image>
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]