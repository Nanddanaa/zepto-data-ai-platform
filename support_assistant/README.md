# Zepto Support Assistant

This module builds a RAG based support assistant using the 8 Zepto policy documents.

It uses `all-MiniLM-L6-v2` for embeddings, ChromaDB for storing and retrieving documents, LangGraph for routing the query and FastAPI for the API.

## Architecture

The flow of the application is:

**Ingestion → Embedding → Retrieval → Generation**

The 8 documents from the `docs` folder are loaded and converted into embeddings using `all-MiniLM-L6-v2`. The embeddings are stored in the `zepto_policies` ChromaDB collection using cosine similarity.

The query first goes to the `classify_intent` node. In the default mock mode, it checks for the given policy keywords and classifies the query as either `policy_question` or `general_question`.

For a policy question, `retrieve_and_answer` retrieves the top 3 similar documents from ChromaDB and uses the top result to create the answer.

For a general question, `direct_answer` returns the fixed response without retrieval.

```text
User Query
    |
classify_intent
    |
    |--- policy_question ---> retrieve_and_answer
    |
    |--- general_question --> direct_answer
```

`MOCK_LLM=1` is used by default and does not make any LLM API call. The optional real LLM extension is not used in this submission.

The structured prompt follows **role → context → task → format → length** and includes a negative constraint and a few-shot example.

The final output is validated using Pydantic with `answer`, `sources` and `confidence`.

## Run Locally

Move to the support assistant folder:

```bash
cd support_assistant
```
Install the required packages:

```bash
pip install -r requirements.txt
```
Start the API:

```bash
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

Use the `POST /ask` endpoint.

## Example 1 - Policy Question

Request:

```json
{
  "query": "What is the delivery fee?"
}
```

Response:

```json
{
  "answer": "Based on the retrieved context: Zepto delivers grocery and household essentials to serviceable pin codes within 10 to 30 minutes of order confirmation, depending on the customer's delivery zone and current order volume. Standard del",
  "sources": [
    "doc_01",
    "doc_05",
    "doc_02"
  ],
  "confidence": 1
}
```

This query contains `delivery`, so it is routed to `retrieve_and_answer` and retrieves the top 3 documents.

## Example 2 - General Question

Request:

```json
{
  "query": "Who invented Python?"
}
```

Response:

```json
{
  "answer": "I can only answer questions about Zepto policies right now.",
  "sources": [],
  "confidence": 1
}
```

This query does not contain a policy keyword, so it goes to `direct_answer` without retrieval.

## Docker

Build the image from the project root:

```bash
docker build -f support_assistant/Dockerfile -t zepto-support .
```

Run it:

```bash
docker run -p 7860:7860 zepto-support
```

Then open:

```text
http://127.0.0.1:7860/docs
```

The Dockerfile is included for the required local containerization. Hugging Face deployment is optional.
