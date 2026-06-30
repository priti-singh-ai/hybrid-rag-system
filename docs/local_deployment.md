# Local Deployment Guide

## Overview

This project implements a **Hybrid Retrieval-Augmented Generation (Hybrid RAG)** system that combines semantic search using **PGVector** with lexical search using **BM25**, followed by reranking using a Cross Encoder and response generation using a locally hosted Large Language Model (LLM) through **Ollama**.

The current implementation is a **local deployment**, which means every component runs on the local machine without any cloud infrastructure.

---

# System Architecture

```text
                          User
                            │
                            ▼
                     Terminal / FastAPI
                            │
                            ▼
                         main.py
                            │
                            ▼
                  HybridRetriever
                ┌──────────┴──────────┐
                │                     │
                ▼                     ▼
         Vector Search          BM25 Search
                │                     │
                ▼                     ▼
      PostgreSQL + PGVector     Local PDF Documents
                └──────────┬──────────┘
                           ▼
                  Metadata Filtering
                           ▼
                    Cross Encoder
                      Reranker
                           ▼
                 Context Construction
                           ▼
                  Conversation Memory
                           ▼
                    Ollama (Qwen2.5)
                           ▼
                     Final Response
```

---

# Project Workflow

The execution of the project begins from `main.py`, which acts as the orchestrator for the complete Hybrid RAG pipeline.

For every user query, the following sequence of operations is executed.

```text
User Question
      │
      ▼
Hybrid Retrieval
      │
      ▼
Metadata Filtering
      │
      ▼
Cross Encoder Reranking
      │
      ▼
Context Generation
      │
      ▼
Conversation History
      │
      ▼
LLM (Ollama)
      │
      ▼
Generated Answer
      │
      ▼
Save Chat History
```

---

# Component Description

## 1. User Interface

Currently, the application runs through the terminal.

Example:

```bash
python main.py
```

The user enters a question:

```text
Ask Question:
```

In the future, this terminal interface can easily be replaced with FastAPI.

---

## 2. main.py

The `main.py` file controls the complete execution flow.

Responsibilities include:

- Accept user queries
- Call the Hybrid Retriever
- Filter retrieved documents
- Rerank retrieved documents
- Construct context
- Load conversation history
- Generate answers using Ollama
- Save conversation history
- Display the final response

This file acts as the controller of the entire application.

---

## 3. Hybrid Retriever

The Hybrid Retriever combines two different retrieval techniques.

### Vector Retrieval

Vector Retrieval performs semantic search.

Workflow:

```text
Question
    │
    ▼
Generate Embedding
    │
    ▼
PostgreSQL + PGVector
    │
    ▼
Top K Semantic Chunks
```

The query embedding is generated using the embedding model.

The generated embedding is compared against stored embeddings inside PostgreSQL using the PGVector extension.

---

### BM25 Retrieval

BM25 performs keyword-based retrieval.

Workflow:

```text
Question
      │
      ▼
Tokenization
      │
      ▼
BM25 Ranking
      │
      ▼
Top K Documents
```

Unlike Vector Search, BM25 searches using lexical similarity.

---

### Hybrid Search

The results from Vector Search and BM25 Search are merged together.

This allows the system to retrieve:

- Semantic matches
- Exact keyword matches

Hybrid Retrieval improves document recall compared to using only one retrieval technique.

---

# 4. Metadata Filtering

After retrieval, metadata filtering removes documents that do not satisfy predefined conditions.

Example:

```text
Year = 2025
```

Only matching documents proceed to the reranking stage.

This reduces unnecessary computation and improves answer quality.

---

# 5. Cross Encoder Reranker

The reranker improves document relevance.

Input:

```text
Question

Document
```

↓

Cross Encoder

↓

Relevance Score

↓

Sorted Documents

Unlike Vector Search and BM25, the Cross Encoder evaluates the question and document together to estimate their semantic relevance.

The highest-scoring documents become the final retrieval context.

---

# 6. Context Construction

The top-ranked documents are combined into one context block.

Example:

```text
Document 1

Document 2

Document 3

Document 4

Document 5
```

This context is passed to the LLM.

---

# 7. Conversation Memory

The project maintains conversation history using LangChain Memory.

Workflow:

```text
Previous Question
        │
        ▼
Previous Answer
        │
        ▼
Conversation Buffer
        │
        ▼
Current Prompt
```

This enables multi-turn conversations by preserving earlier interactions.

The memory is updated after every successful response.

---

# 8. Ollama

The project uses Ollama to host the language model locally.

Current model:

```text
qwen2.5:7b
```

Prompt sent to Ollama contains:

- Retrieved Context
- Conversation History
- Current User Question

Ollama generates the final answer without requiring any external API.

Everything runs locally.

---

# Current Local Infrastructure

The complete application currently runs on a single machine.

```text
Windows Machine
│
├── Python Virtual Environment
│
├── PostgreSQL
│      │
│      └── PGVector Extension
│
├── Ollama Server
│      │
│      └── qwen2.5:7B Model
│
└── Hybrid RAG Application
```

No cloud resources are used.

---

# Local Request Flow

```text
User

↓

main.py

↓

Hybrid Retriever

↓

Vector Search
        +
BM25 Search

↓

Metadata Filter

↓

Cross Encoder

↓

Top Ranked Documents

↓

Conversation Memory

↓

Ollama

↓

Generated Response

↓

Display Answer
```

---

# Running the Project Locally

## Step 1

Activate the virtual environment.

```bash
hybrid_rag_env\Scripts\activate
```

---

## Step 2

Start PostgreSQL.

Ensure the PostgreSQL service is running and the PGVector extension is enabled.

---

## Step 3

Verify Ollama.

```bash
ollama list
```

Expected output:

```text
qwen2.5:7b
```

If the model is not available:

```bash
ollama pull qwen2.5:7b
```

---

## Step 4

Run the application.

```bash
python main.py
```

---

# Local Deployment Using FastAPI

Currently, the project is executed through the terminal.

The next step is to expose the application using FastAPI.

The architecture becomes:

```text
                Browser / Postman
                        │
                        ▼
                    FastAPI
                        │
                        ▼
                     main.py
                        │
                        ▼
                 Hybrid Retriever
                        │
                        ▼
               Retrieval Pipeline
                        │
                        ▼
                    Ollama
                        │
                        ▼
                  JSON Response
```

FastAPI acts only as the API layer.

It does not change the retrieval pipeline.

Its responsibilities are:

- Accept HTTP requests
- Validate input
- Call the Hybrid RAG pipeline
- Return JSON responses

---

# Local Deployment Using Docker

Docker packages the application and its dependencies into containers.

A local Docker architecture would look like:

```text
                   Docker Desktop
                          │
        ┌─────────────────┴─────────────────┐
        │                                   │
        ▼                                   ▼
 FastAPI + Python Container        PostgreSQL Container
                                           │
                                           ▼
                                      PGVector
```

The Ollama server can either:

- Run directly on the host machine, or
- Be containerized separately.

Docker provides:

- Environment consistency
- Dependency isolation
- Easier project setup
- Reproducible local development

Although Docker is not mandatory for local execution, it prepares the application for future production deployment.

---

# Why FastAPI?

FastAPI provides:

- REST API endpoints
- Request validation
- Automatic OpenAPI documentation
- Easy integration with frontend applications
- High performance asynchronous APIs

Instead of interacting through the terminal, users will be able to send HTTP requests.

---

# Why Docker?

Docker simplifies deployment by:

- Packaging the application with all dependencies
- Eliminating environment-specific issues
- Making the application portable
- Preparing the project for cloud deployment


---

# Summary

The current implementation represents a fully functional **local Hybrid RAG system**. The application executes entirely on the local machine, where PostgreSQL with PGVector stores vector embeddings, BM25 retrieves keyword-based documents, the Cross Encoder reranks the retrieved results, and Ollama generates responses using a locally hosted language model.

The next stage of development is to expose the application through **FastAPI**, package it using **Docker**, and eventually deploy it to a cloud environment while preserving the same retrieval and generation pipeline.