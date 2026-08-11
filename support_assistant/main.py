import os
import chromadb

from typing import TypedDict
from sentence_transformers import SentenceTransformer
from langgraph.graph import StateGraph, END
from pydantic import BaseModel, Field
from fastapi import FastAPI


model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.Client()

collection = client.get_or_create_collection(
    name="zepto_policies",
    metadata={"hnsw:space":"cosine"}
)

documents = []
ids = []

for filename in sorted(os.listdir("docs")):
    if filename.endswith(".txt"):
        with open(os.path.join("docs",filename),"r",encoding="utf-8") as file:
            documents.append(file.read())
            ids.append(filename.replace(".txt",""))

embeddings = model.encode(documents).tolist()

collection.upsert(
    ids=ids,
    documents=documents,
    embeddings=embeddings
)


prompt_template = """
Role:
You are a Zepto customer support assistant.

Context:
Use the Zepto policy context given below.
{context}

Task:
Answer the customer question using the given context.

Format:
Give a clear and direct answer.

Length:
Answer within 3 sentences.

Negative Constraint:
Do not answer using information that is not present in the provided context.

Few-shot Example:
Question: Can I return a damaged grocery item?
Answer: Yes. Damaged grocery items can be reported within 24 hours of delivery.

Question:
{query}

Answer:
"""


MOCK_LLM = os.getenv("MOCK_LLM","1")


class GraphState(TypedDict, total=False):
    query: str
    intent: str
    answer: str
    sources: list[str]
    confidence: float


policy_keywords = [
    "delivery",
    "return",
    "refund",
    "membership",
    "tracking",
    "cancel",
    "gift card",
    "support hours"
]


def classify_intent(state: GraphState):
    query = state["query"].lower()

    if MOCK_LLM != "0":
        if any(word in query for word in policy_keywords):
            return {"intent":"policy_question"}
        return {"intent":"general_question"}

    return {"intent":"general_question"}


def retrieve_and_answer(state: GraphState):
    query = state["query"]

    query_embedding = model.encode([query]).tolist()

    result = collection.query(
        query_embeddings=query_embedding,
        n_results=3
    )

    docs = result["documents"][0]
    ids = result["ids"][0]

    if MOCK_LLM != "0":
        return {
            "answer":f"Based on the retrieved context: {docs[0][:200]}",
            "sources":ids,
            "confidence":1.0
        }

    return {
        "answer":"Real LLM mode is not configured.",
        "sources":ids,
        "confidence":0.0
    }


def direct_answer(state: GraphState):
    if MOCK_LLM != "0":
        return {
            "answer":"I can only answer questions about Zepto policies right now.",
            "sources":[],
            "confidence":1.0
        }

    return {
        "answer":"Real LLM mode is not configured.",
        "sources":[],
        "confidence":0.0
    }


def route(state):
    return state["intent"]


graph = StateGraph(GraphState)

graph.add_node("classify_intent",classify_intent)
graph.add_node("retrieve_and_answer",retrieve_and_answer)
graph.add_node("direct_answer",direct_answer)

graph.set_entry_point("classify_intent")

graph.add_conditional_edges(
    "classify_intent",
    route,
    {
        "policy_question":"retrieve_and_answer",
        "general_question":"direct_answer"
    }
)

graph.add_edge("retrieve_and_answer",END)
graph.add_edge("direct_answer",END)

app_graph = graph.compile()


class AskRequest(BaseModel):
    query: str


class Answer(BaseModel):
    answer: str
    sources: list[str]
    confidence: float = Field(ge=0,le=1)


def ask_graph(query):
    result = app_graph.invoke({"query":query})

    return Answer(
        answer=result["answer"],
        sources=result["sources"],
        confidence=result["confidence"]
    )


def validate_llm_output(llm_function,prompt):
    for i in range(3):
        try:
            output = llm_function(prompt)
            return Answer.model_validate_json(output)
        except:
            prompt += "\nReturn valid JSON with answer, sources and confidence."

    return Answer(
        answer="Error: LLM output could not be validated.",
        sources=[],
        confidence=0.0
    )


app = FastAPI()


@app.post("/ask",response_model=Answer)
def ask(request: AskRequest):
    return ask_graph(request.query)