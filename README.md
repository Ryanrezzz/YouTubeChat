<div align="center">

# 🎬 YouTube Chat

### _Have a conversation with any YouTube video_

[![Streamlit App](https://img.shields.io/badge/🚀_Live_Demo-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://youtubechat-jsclfvinhrpdbazgtz5jdv.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![LangChain](https://img.shields.io/badge/🦜_LangChain-Framework-1C3C3C?style=for-the-badge)](https://langchain.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

<br/>

> **Paste a YouTube URL → Get instant answers from the video.**
> No more scrubbing through hour-long videos to find that one piece of information.

<br/>

```
  ┌─────────────────────────────────────────────────┐
  │  🔗  Paste YouTube URL                          │
  │  📝  Transcript extracted automatically         │
  │  🧠  RAG pipeline processes & indexes content   │
  │  💬  Ask anything — get contextual answers      │
  └─────────────────────────────────────────────────┘
```

</div>

---

## ✨ Features

| Feature | Description |
|:--------|:------------|
| 🎯 **Instant Q&A** | Ask natural language questions about any YouTube video and get accurate, context-aware answers |
| 🔄 **Conversational Memory** | Multi-turn chat with full conversation history — follow-up questions just work |
| ⚡ **Auto Transcript Extraction** | Automatically fetches video transcripts via the Supadata API — no manual effort needed |
| 🧩 **Smart Chunking** | Transcripts are split into overlapping chunks (1000 chars, 200 overlap) for precise retrieval |
| 🔍 **Semantic Search** | FAISS vector store with Google Gemini embeddings for lightning-fast similarity search |
| 🤖 **Powered by Llama 3.3 70B** | Groq-hosted LLM for fast, high-quality responses |
| 🖥️ **Embedded Video Player** | Watch the video right inside the app alongside the chat |
| 🌐 **Live on Streamlit Cloud** | Deployed and accessible from anywhere — no setup required |

---

## 🏗️ Architecture

```
                          ┌──────────────────┐
                          │   YouTube URL    │
                          └────────┬─────────┘
                                   │
                          ┌────────▼─────────┐
                          │   Supadata API   │
                          │  (Transcript)    │
                          └────────┬─────────┘
                                   │
                   ┌───────────────▼───────────────┐
                   │  RecursiveCharacterTextSplitter │
                   │    chunk_size=1000              │
                   │    chunk_overlap=200            │
                   └───────────────┬───────────────┘
                                   │
               ┌───────────────────▼────────────────────┐
               │        Google Gemini Embeddings         │
               │     (gemini-embedding-2-preview)        │
               └───────────────────┬────────────────────┘
                                   │
                          ┌────────▼─────────┐
                          │   FAISS Vector   │
                          │     Store        │
                          └────────┬─────────┘
                                   │
          ┌────────────────────────▼────────────────────────┐
          │              LangChain RAG Chain                │
          │                                                │
          │  RunnableParallel                               │
          │  ├── context  → Retriever (k=5) → format_docs  │
          │  ├── question → passthrough                     │
          │  └── chat_history → passthrough                 │
          │           │                                     │
          │    ChatPromptTemplate → ChatGroq → StrParser    │
          │              (Llama 3.3 70B)                    │
          └────────────────────────┬────────────────────────┘
                                   │
                          ┌────────▼─────────┐
                          │  💬 Chat Answer  │
                          └──────────────────┘
```

---

## 🛠️ Tech Stack

<div align="center">

| Layer | Technology |
|:------|:-----------|
| **Frontend** | Streamlit |
| **LLM** | Llama 3.3 70B via Groq |
| **Embeddings** | Google Gemini (`gemini-embedding-2-preview`) |
| **Vector Store** | FAISS (Facebook AI Similarity Search) |
| **Orchestration** | LangChain (Runnables, Prompts, Output Parsers) |
| **Transcript API** | Supadata |
| **Language** | Python 3.10+ |

</div>

---

## 📂 Project Structure

```
YouTubeChat/
├── app.py              # Streamlit UI — chat interface, session state, video embedding
├── main.py             # Core RAG pipeline — vector store, retriever, chain, CLI mode
├── requirements.txt    # Python dependencies
├── .gitignore          # Ignored files (env, cache, venv)
└── README.md           # You are here ✨
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- API keys for **Groq**, **Google Generative AI**, and **Supadata**

### 1️⃣ Clone the repo

```bash
git clone https://github.com/yourusername/YouTubeChat.git
cd YouTubeChat
```

### 2️⃣ Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Set up environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
GOOGLE_API_KEY=your_google_api_key
SUPADATA_API_KEY=your_supadata_api_key
```

### 5️⃣ Run the app

**Streamlit UI (recommended):**
```bash
streamlit run app.py
```

**CLI mode:**
```bash
python main.py
```

---

## 🔑 Environment Variables

| Variable | Description | Required |
|:---------|:------------|:--------:|
| `GROQ_API_KEY` | API key for Groq (LLM inference) | ✅ |
| `GOOGLE_API_KEY` | API key for Google Gemini Embeddings | ✅ |
| `SUPADATA_API_KEY` | API key for Supadata (transcript extraction) | ✅ |

---

## 💡 How It Works

1. **Paste a URL** — Enter any YouTube video link into the input field
2. **Transcript Extraction** — Supadata API fetches the full video transcript
3. **Chunking** — The transcript is split into overlapping chunks using `RecursiveCharacterTextSplitter`
4. **Embedding & Indexing** — Each chunk is embedded with Google Gemini and stored in a FAISS vector index
5. **Ask Questions** — Your question is embedded → top-5 similar chunks are retrieved → sent to Llama 3.3 70B with conversation history
6. **Get Answers** — The LLM generates a grounded answer based on the retrieved transcript context

---

## 🌐 Live Demo

👉 **[Try it now on Streamlit Cloud](https://youtubechat-jsclfvinhrpdbazgtz5jdv.streamlit.app/)**

---

<div align="center">

**Built with ❤️ using LangChain, Groq, and Streamlit**

</div>
