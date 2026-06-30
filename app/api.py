from fastapi import FastAPI
from pydantic import BaseModel

from main import ask_question

app = FastAPI()


class Query(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "Hybrid RAG Running"
    }


@app.post("/chat")
def chat(query: Query):

    result = ask_question(query.question)

    return result