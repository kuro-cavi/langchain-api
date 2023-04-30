import os
import logging

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import UnstructuredURLLoader
from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI

logger = logging.getLogger('uvicorn')
openai_api_key = os.environ["OPENAI_API_KEY"]

app = FastAPI()


class UrlRequest(BaseModel):
    question: str
    urls: List[str]


class FormatRequest(BaseModel):
    message: str


@app.post("/url")
def url(request: UrlRequest):
    """
    URL Load
    ----------
    :see https://python.langchain.com/en/latest/modules/indexes/document_loaders/examples/url.html
    """
    loader = UnstructuredURLLoader(urls=request.urls)
    data = loader.load()

    text_splitter = CharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    docs = text_splitter.split_documents(data)

    chain = load_qa_chain(
        OpenAI(temperature=0),
        chain_type="stuff",
    )
    res = chain({"input_documents": docs, "question": request.question}, return_only_outputs=True)

    logger.info(res)
    return {"output": res['output_text'].strip()}


@app.post("/format")
def format(request: FormatRequest):
    """
    Template Format
    ----------
    :see https://python.langchain.com/en/latest/reference/modules/prompts.html
    :see https://python.langchain.com/en/latest/reference/modules/output_parsers.html
    """
    output_parser = CommaSeparatedListOutputParser()

    prompt = PromptTemplate(
        template="{message}車を教えてください？日本車でお願いします。\n{format_instructions}",
        input_variables=["message"],
        partial_variables={"format_instructions": output_parser.get_format_instructions()}
    )

    llm = OpenAI(temperature=0)

    _input = prompt.format(message=request.message)
    output = llm(_input)
    response = output_parser.parse(output)

    logger.info(response)
    return {"output": response}
