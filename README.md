# [AI] 중급 프로젝트: 입찰메이트 (BidMate)

> **RAG (Retrieval-Augmented Generation) System for Korean RFP Analysis**

This project implements a high-performance RAG system designed to analyze and extract key information from complex Request for Proposal (RFP) documents. It addresses the challenge of reviewing hundreds of technical documents by providing an automated, context-aware question-answering service for "BidMate" consultants.

## 🚀 Key Features

- **Hybrid Search Algorithm**: Combines dense vector retrieval (Chroma, `text-embedding-3-small`) with sparse keyword retrieval (BM25) using a custom **Char-Bigram Tokenizer** optimized for Korean technical terms.
- **Smart Chunking & Context Injection**: Solves information fragmentation by isolating budget sections and injecting `[Organization] [Project Name]` context into every text chunk.
- **Quantitative Evaluation Framework**: 
    - Auto-generates evaluation datasets (QA pairs) using `generate_dataset.py`.
    - Scores performance (1-5 scale) using an **LLM-as-a-Judge** approach via `evaluate.py`.
    - **Current Baseline Score: 3.29 / 5.0** (Top-30 Context Window).
- **Dual Architecture Support**:
    - **Scenario A (On-Premise)**: Self-hosted LLM on GCP (vLLM, L4 GPU).
    - **Scenario B (Cloud API)**: OpenAI GPT-5-mini.

## 🛠️ Tech Stack

| Category | Technology | Description |
| :--- | :--- | :--- |
| **Language** | Python 3.11+ | Core development language |
| **LLM Serving** | **vLLM** | High-throughput serving for local models (GCP) |
| **Framework** | LangChain | RAG pipeline orchestration |
| **Vector DB** | ChromaDB | Local vector store for dense retrieval |
| **PDF Parsing** | Upstage API | High-accuracy layout analysis for tables/charts |
| **Dependency** | `uv` | Modern, fast Python package manager |

## 📁 Directory Structure

```
project-2/
├── config/             # Configuration (Chunking size, Retrieval k, etc.)
├── data/               # Processed data storage (Raw files excluded from repo)
├── debug_tools/        # Scripts for debugging retrieval, ranking, and DB
├── RAG_LLM/            # Chatbot implementation
├── src/                # Core Source Code
│   ├── pipeline/       # Data Processing (Chunker, Parser)
│   ├── generator.py    # RAG Chain & Prompt Engineering
│   ├── indexer.py      # Vector DB Indexing
│   ├── loader.py       # Data Loading & Context Injection
│   └── retriever.py    # Hybrid Search Implementation (BM25+Chroma)
├── evaluate.py         # Async Evaluation Script (Quantitative Analysis)
├── generate_dataset.py # Evaluation Dataset Generator
├── main.py             # CLI Chat Application
├── pipeline.py         # Data Pipeline Orchestrator
└── README.md           # Project Documentation
```

## ⚠️ Data Privacy Notice

> [!IMPORTANT]
> **Raw Data Not Included**: Per the data privacy agreement, the original RFP documents (`data/raw_data`) and files (`data/files`) are **NOT** included in this repository.
> The `data/` directory only contains processed intermediate files necessary for the system to function if raw data is provided locally.

## 🛠️ Setup & Installation

**Prerequisites**: Python 3.10+, `uv` installed.

1.  **Initialize & Sync**:
    ```bash
    # This project uses uv for dependency management.
    uv sync
    ```
2.  **Environment Variables**: Create `.env` file based on `.env.example`:
    ```ini
    OPENAI_API_KEY=sk-...     # For Generator & Evaluator
    UPSTAGE_API_KEY=...       # For PDF Parsing (Pipeline)
    ```

## 🏃 Usage

### 1. Data Pipeline
Run the full data processing pipeline (HWP Convert -> PDF Parse -> Process -> Vector DB).
*Note: Requires raw HWP/PDF files in `data/raw_data`.*

```bash
# Run all steps
python pipeline.py --step all

# Run specific steps
python pipeline.py --step convert  # HWP to PDF
python pipeline.py --step parse    # PDF to Layout-Analyzed JSON
python pipeline.py --step clean    # Semantic Chunking & Cleaning
python pipeline.py --step index    # Build Vector Index
```

### 2. Chat Application
Interact with the system specifically designed for BidMate consultants:
```bash
python main.py
```

### 3. Quantitative Evaluation
Run the automated evaluation against the technical dataset:
```bash
python evaluate.py --data data/eval_set_100.json --output evaluation_result.csv
```

## 📊 Performance Benchmark

| Metric | Score | Note |
| :--- | :--- | :--- |
| **Baseline (Top-10)** | 2.90 / 5.0 | Missed details in broad summarization tasks. |
| **Expanded (Top-30)** | **3.29 / 5.0** | Significantly improved coverage for "System Requirements". |

## 📝 Team & Resources

### 👥 Team Members

| Team Member | Role | Work Log |
| :--- | :--- | :--- |
| **주재홍** | **PM / Data Pipeline** | - |
| **서준범** | **Model Engineering** | [Link](https://www.notion.so/Daily-2cae2cccbd88803eafabe85a695162f7?source=copy_link) |
| **전예린** | - | - |
| **김장현** | - | - |

### 📄 Documentation
- **Project Presentation**: [View PDF](https://drive.google.com/file/d/1W9RDTffGqoEwBWKtAqdaFv-int5G7tj1/view?usp=sharing)


