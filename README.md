# 🌿 ExploreLK

## Discover Sri Lanka's Hidden Gems

ExploreLK is an intelligent travel planning application that helps travelers discover hidden tourist destinations across Sri Lanka. The system generates personalized travel recommendations based on the user's budget, travel duration, starting location, and interests.

The application uses **LangGraph**, **Retrieval-Augmented Generation (RAG)**, **ChromaDB**, and **Groq Large Language Models** to provide accurate destination recommendations and personalized travel itineraries.

---

## ✨ Features

- 🌿 Discover hidden tourist destinations
- 🤖 Multi-Agent travel planning
- 📚 Retrieval-Augmented Generation (RAG)
- 📄 Knowledge Base with 29 PDF documents
- 🧠 ChromaDB Vector Database
- ⚡ Groq Llama Models
- 🎯 Personalized destination recommendations
- 🗓️ AI-generated travel itineraries
- 🌐 Interactive Streamlit web application

---

## 🛠️ Technologies Used

| Category | Technology |
|----------|------------|
| Programming Language | Python 3.14 |
| Frontend | Streamlit |
| AI Framework | LangChain |
| Multi-Agent Framework | LangGraph |
| Vector Database | ChromaDB |
| Embedding Model | sentence-transformers/all-MiniLM-L6-v2 |
| Large Language Model | Groq (Llama 3.3 70B & Llama 3.1 8B) |
| Data Processing | Pandas |
| Environment Variables | Python Dotenv |
| Knowledge Base | 29 PDF Documents |
| Dataset | Hidden Gems Sri Lanka Dataset (.xlsx) |

## 📁 Project Structure

```text
ExploreLK/
│
├── app.py
├── backend.py
├── requirements.txt
├── README.md
├── .env
├── .gitignore
│
├── data/
│   └── hidden_gems_srilanka.xlsx
│
├── knowledge_base/
│   └── 29 PDF Documents
│
└── chroma_db/
```
## 🏗️ System Architecture

```text
                     User
                       │
                       ▼
            Streamlit Web Interface
                       │
                       ▼
            LangGraph Workflow Engine
                       │
      ┌────────────────┼────────────────┐
      ▼                ▼                ▼
Preference Agent  Destination Agent   RAG Agent
      │                │                │
      └────────────────┼────────────────┘
                       ▼
              Itinerary Planner Agent
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
     ChromaDB      Knowledge Base    Groq LLM
     (Vectors)       (29 PDFs)     (Llama Models)
                       │
                       ▼
        Personalized Travel Recommendation
```
## 🤖 Multi-Agent Workflow

The ExploreLK system uses four specialized AI agents that work together through LangGraph.

### 1. Preference Agent
- Analyzes the user's travel preferences.
- Identifies budget, travel duration, starting location, and interests.

### 2. Destination Agent
- Selects suitable hidden destinations from the Sri Lanka dataset.
- Matches recommendations with user preferences.

### 3. RAG Agent
- Retrieves relevant information from the PDF knowledge base using ChromaDB.
- Provides contextual travel information.

### 4. Itinerary Planner Agent
- Generates a personalized travel itinerary.
- Suggests activities, travel tips, and recommended visit times.

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Dilki456/ExploreLK.git
cd ExploreLK
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment.

**Windows**

```bash
venv\Scripts\activate
```

**Mac/Linux**

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root and add your Groq API key.

```env
GROQ_API_KEY=your_groq_api_key_here
```

### 5. Run the Application

```bash
streamlit run app.py
```

After the application starts, open your browser and visit:

```
http://localhost:8501
```