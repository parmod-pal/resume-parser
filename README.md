# 📄 AI-Powered Resume Parser (Groq + FastAPI)

A full-stack asynchronous application that extracts structured JSON data from PDF and DOCX resumes using Large Language Models (LLM). This project demonstrates a production-grade AI pipeline from document ingestion to cloud deployment.

## 🚀 Live Demo
* **Frontend (Streamlit):** [https://resume-parser-czjzsuwynv5rnjzqllkmot.streamlit.app](https://resume-parser-czjzsuwynv5rnjzqllkmot.streamlit.app)
* **API Documentation:** [https://resume-parser-7nma.onrender.com/docs](https://resume-parser-7nma.onrender.com/docs)

## ✨ Key Features
* **Hybrid Extraction:** Combines traditional text scraping (PyMuPDF/Docx) with Llama 3 (via Groq) for high-accuracy entity extraction.
* **Structured Output:** Uses Pydantic models to ensure JSON consistency for Name, Contact, Skills, Experience, and Education.
* **Async Processing:** Built with FastAPI for high-performance, non-blocking API calls.
* **Robust UI:** Streamlit-based dashboard with real-time feedback and JSON visualization.

## 🛠️ Tech Stack
* **Language:** Python 3.12
* **Backend:** FastAPI
* **Frontend:** Streamlit
* **AI/LLM:** Groq Cloud API (Llama 3.1)
* **Libraries:** PyMuPDF (Fitz), Pydantic, Requests, Loguru, python-docx

## 📦 Project Structure
```text
├── app/
│   ├── main.py          # FastAPI entry point & Middleware
│   ├── routes/          # API endpoints (/api/upload)
│   ├── services/        # LLM Logic & Document Parsers
│   └── utils/           # Configuration & Logging
├── ui/
│   └── streamlit_app.py # Streamlit UI logic & API integration
├── data/                # Local storage for uploads (git-ignored)
├── requirements.txt     # Production dependencies
└── README.md
```

## ⚙️ Local Setup

### Clone the repository:

```bash
git clone https://github.com/parmod-pal/resume-parser.git
cd resume-parser
```

### Set up Environment Variables:

Create a `.env` file in the root directory:

```plaintext
GROQ_API_KEY=your_api_key_here
```

### Install Dependencies:

```bash
pip install -r requirements.txt
```

### Run the Backend:

```bash
uvicorn app.main:app --reload
```

### Run the Frontend:

```bash
streamlit run ui/streamlit_app.py
```
