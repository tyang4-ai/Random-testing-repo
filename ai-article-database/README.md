# AI Article Database for Environmental Protection

A proof-of-concept demonstration system that uses AI to organize, search, and analyze environmental protection articles.

## Features

- **Semantic Search**: Search articles using natural language keywords (Chinese supported)
- **AI-Powered Reports**: Generate comprehensive research reports based on selected articles
- **Article Management**: Add, edit, and delete articles through admin interface
- **Local Deployment**: Everything runs locally - no cloud services required

## Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: React + Vite
- **Database**: SQLite
- **Vector Store**: ChromaDB
- **Embeddings**: BGE-large-zh-v1.5 (Chinese optimized)
- **LLM**: DeepSeek via Ollama

## Quick Start

See `部署说明.md` for detailed deployment instructions in Chinese.

### Prerequisites

- Python 3.10+
- Node.js 18+
- Ollama

### Installation

1. Install Ollama and pull DeepSeek model:
   ```bash
   ollama pull deepseek-v2
   ```

2. Start backend:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python load_sample_data.py  # Load sample articles
   python main.py
   ```

3. Start frontend (new terminal):
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. Open http://localhost:5173 in your browser

## Project Structure

```
ai-article-database/
├── backend/
│   ├── main.py              # FastAPI entry point
│   ├── database.py          # SQLite + ChromaDB setup
│   ├── models.py            # Data models
│   ├── schemas.py           # Pydantic schemas
│   ├── services/
│   │   ├── embedding.py     # BGE embedding service
│   │   ├── llm.py           # DeepSeek/Ollama service
│   │   └── search.py        # Semantic search
│   ├── routers/
│   │   ├── articles.py      # Admin CRUD API
│   │   └── search.py        # Search & report API
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── pages/
│       │   ├── UserPage.jsx   # Search interface (Chinese)
│       │   └── AdminPage.jsx  # Admin interface (Chinese)
│       └── services/api.js
├── data/
│   └── sample_articles.json  # 10 sample articles
├── 部署说明.md               # Deployment guide (Chinese)
└── README.md
```

## Sample Articles

The demo includes 10 Chinese environmental articles covering:
- Water pollution control in Yangtze River Delta
- Suzhou River ecological restoration
- Taihu Lake algae management
- Shanghai waste classification policy
- Yangtze River ecosystem protection
- Beijing-Tianjin-Hebei air pollution control
- Yellow River Delta wetland conservation
- Industrial wastewater zero-discharge technology
- Carbon neutrality policy analysis
- Smart environmental monitoring systems

## License

MIT
