# 🧪 AI Scientist: Multi-Agent Research Assistant

An **industry-grade, modular, multi-agent AI system** that performs **automated literature discovery, iterative research exploration, synthesis, and evaluation** — with **human-in-the-loop control** and a **clean separation between reasoning and execution using MCP**.

---

## Project Overview

Given a research topic (e.g. *“continual learning in machine learning”*), the system:

1. Searches academic and web sources  
2. Iteratively proposes *new research queries* based on discovered evidence  
3. Allows a **human to approve, reject, or stop** exploration  
4. Deduplicates and ranks papers  
5. Synthesizes a structured literature review from abstracts  
6. Evaluates the quality of the synthesis using an independent evaluator agent  

All execution is routed through an **MCP (Model Context Protocol) server**, making the system **safe, auditable, and extensible**.

---

## Agents

### 1️⃣ Query Proposer Agent
- Reads accumulated paper abstracts
- Proposes **new search queries**
- Explains *why* each query is relevant
- Operates in a **human-in-the-loop loop**

### 2️⃣ Evaluator Agent
- Independently evaluates the final synthesis
- Uses structured quality metrics:
  - Coverage
  - Evidence sufficiency
  - Coherence
  - Missing areas

---

## MCP Integration

This project uses **Model Context Protocol (MCP)** to expose all execution capabilities as **tools**:

### MCP-Exposed Tools
- `search_arxiv`
- `search_semantic_scholar`
- `search_duckduckgo`
- `deduplicate_records`
- `rank_discovery_records`
- `synthesize_from_abstracts`
- `evaluate_synthesis`

---

## Repository Structure

```
src/
├── agents/
│   ├── query_proposer.py
│   └── evaluator.py
│
├── langgraph_pipeline.py
├── langgraph_state.py
│
├── tools/                # Core implementations
│   ├── search_arxiv.py
│   ├── search_semantic_scholar.py
│   └── search_duckduckgo.py
│
├── ranking/
│   ├── dedup.py
│   └── ranking.py
│
├── synthesis/
│   └── abstract_synthesis.py
│
├── mcp_server/
│   ├── server.py
│   └── tools/            # MCP wrappers
│       ├── search_arxiv.py
│       ├── search_semantic_scholar.py
│       ├── search_duckduckgo.py
│       ├── dedup.py
│       ├── ranking.py
│       ├── synthesis.py
│       └── evaluation.py
│
├── mcp_client.py
└── schemas.py

```
---

## Research Loop (Human-in-the-Loop)

1. Initial search on topic  
2. Query proposer suggests new queries  
3. Human chooses:
   - **Approve** → run search
   - **Reject** → next query
   - **Stop** → synthesis  
4. Loop repeats until stop or max iterations  
5. Final synthesis + evaluation  

This mirrors **real human research workflows**.

---

## Using This Project

### Prerequisites

- Python **3.10+**
- `pip` or `conda`
- An **OpenAI API key** (required for synthesis and evaluation)


### Clone the Repository

```bash
git clone https://github.com/your-username/ai-scientist.git
cd ai-scientist
```

### Create and Activate a Virtual Environment (Recommended)

Using conda:
```bash
conda create -n ai_scientist_env python=3.10
conda activate ai_scientist_env
```

Or using venv:
```bash
python -m venv venv
source venv/bin/activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Set Environment Variables

Create a .env file in the project root:
```bash
touch .env
```

Add your OpenAI API key:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

### Run the Research Pipeline

From the project root:
```bash
python -m src.langgraph_pipeline
```

You will see:
- Initial paper search results
- Proposed follow-up search queries
- Interactive prompts to Approve / Reject / Stop

Example interaction:
```bash
Proposed search query:
task-agnostic continual learning methods without explicit task boundaries

Approve / Reject / Stop ? approve
```

## Citation

If you use this work, please cite:

```bibtex
@article{nagaraj2026aiscientist,
  title={AI Scientist: Multi-Agent Research Assistant},
  author={Nagaraj, Balakrishnan},
  year={2026}
}
```