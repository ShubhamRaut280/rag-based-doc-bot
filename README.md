# RAG PDF Bot

A **Retrieval-Augmented Generation (RAG)** API that lets you upload PDFs and ask questions about their content. Built with FastAPI, it parses PDFs, chunks and embeds text, stores vectors in Pinecone, and answers questions using Google Gemini with retrieved context.

## Features

- **PDF upload** – Upload one or more PDFs via API
- **Text extraction** – Parse PDFs with pypdf and extract text per page
- **Chunking** – Split text with LangChain’s `RecursiveCharacterTextSplitter` (500 chars, 100 overlap)
- **Embeddings** – Encode chunks with `sentence-transformers` (all-MiniLM-L6-v2, 384 dimensions)
- **Vector store** – Pinecone serverless index for similarity search
- **Q&A** – Ask questions; the API retrieves relevant chunks and uses Google Gemini to answer with cited sources

## Project structure

```
rag-pdf-bot/
├── app/
│   ├── main.py              # FastAPI app and router registration
│   ├── core/
│   │   └── config.py        # Paths and upload directory
│   ├── routes/
│   │   ├── upload.py        # POST /upload – PDF upload and indexing
│   │   └── chat.py         # POST /chat – question answering
│   └── services/
│       ├── pdf_parser.py    # PDF → list of {page, text, source}
│       ├── chunker.py       # Pages → chunks with metadata
│       ├── embedder.py      # Chunks → embeddings (SentenceTransformer)
│       ├── vector_store.py  # Pinecone upsert and similarity search
│       └── qa.py            # RAG: embed query → search → Gemini answer + sources
├── requirements.txt
├── Dockerfile
├── .env.example
└── README.md
```

## Prerequisites

- **Python 3.11+**
- **Google AI API key** (Gemini)
- **Pinecone API key** and an index name (index is created automatically if missing)

## Setup

1. **Clone and enter the project**

   ```bash
   cd rag-pdf-bot
   ```

2. **Create a virtual environment (recommended)**

   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**

   Copy `.env.example` to `.env` and set your keys:

   ```bash
   cp .env.example .env
   ```

   Edit `.env`:

   ```
   GOOGLE_API_KEY=your_google_api_key
   PINECONE_API_KEY=your_pinecone_api_key
   PINECONE_INDEX_NAME=pdf-rag
   ```

   The app creates a Pinecone serverless index named `PINECONE_INDEX_NAME` with dimension **384** (for all-MiniLM-L6-v2) if it does not exist.

## Running the app

**Local (development):**

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Docker:**

```bash
docker build -t rag-pdf-bot .
docker run -p 8000:8000 --env-file .env rag-pdf-bot
```

Or pull the pre-built image:

```bash
docker run -p 8000:8000 --env-file .env shubham9689/rag-bot:latest
```

API base URL: **http://localhost:8000**

- **Docs:** http://localhost:8000/docs  
- **ReDoc:** http://localhost:8000/redoc  

## API

### Upload PDFs

**`POST /upload/`**

- **Body:** multipart form with one or more files; `content-type` must be `application/pdf`.
- **Response:** `{ "msg": "Files are uploaded", "saved_files": [ ... ] }`
- Files are saved under the `uploads/` directory, then parsed, chunked, embedded, and upserted into Pinecone.

### Ask a question

**`POST /chat/`**

- **Body:** form or JSON with `question` (string).
- **Response:**  
  `{ "answer": "<model answer>", "sources": [ [ { metadata for each retrieved chunk } ] ] }`
- Uses the same embedder to turn the question into a vector, runs a Pinecone similarity search (top 3), then sends the retrieved text plus the question to Gemini and returns the answer and source metadata.

## Tech stack

| Layer        | Technology |
|-------------|------------|
| API         | FastAPI, Uvicorn |
| PDF         | pypdf |
| Chunking    | langchain-text-splitters |
| Embeddings  | sentence-transformers (all-MiniLM-L6-v2) |
| Vector DB   | Pinecone (serverless, cosine, 384 dims) |
| LLM         | LangChain + Google Gemini (gemini-2.5-flash) |
| Config      | python-dotenv |

## License

Use and modify as needed for your project.
