FROM python:3.9

RUN pip install fastapi uvicorn

RUN pip install langchain openai unstructured pdfminer-six

WORKDIR /app
