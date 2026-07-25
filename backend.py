# ==========================================================
# ExploreLK AI Backend
# ==========================================================

import os
from typing import TypedDict

import pandas as pd
from dotenv import load_dotenv

from langchain_groq import ChatGroq

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import (
    StrOutputParser,
    JsonOutputParser
)

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from langgraph.graph import (
    StateGraph,
    START,
    END
)
# ==========================================================
# Environment Variables
# ==========================================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")

print("Environment Variables Loaded")
# ==========================================================
# Load Dataset
# ==========================================================

DATASET_PATH = "data/hidden_gems_srilanka.xlsx"

df = pd.read_excel(DATASET_PATH)

print(f"Dataset Loaded Successfully ({len(df)} records)")

dataset_text = df[
    [
        "Place_Name",
        "District",
        "Province",
        "Category",
        "Budget",
        "Activities",
        "Description"
    ]
].to_string(index=False)
# ==========================================================
# Load Knowledge Base
# ==========================================================

KNOWLEDGE_PATH = "knowledge_base"

loader = PyPDFDirectoryLoader(KNOWLEDGE_PATH)

documents = loader.load()

print(f"Knowledge Base Loaded ({len(documents)} PDF documents)")
# ==========================================================
# Text Chunking
# ==========================================================

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks = text_splitter.split_documents(documents)

print(f"Text Chunking Completed ({len(chunks)} chunks)")
# ==========================================================
# Embedding Model
# ==========================================================

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

print("Embedding Model Loaded")
# ==========================================================
# ChromaDB
# ==========================================================

CHROMA_PATH = "chroma_db"

if os.path.exists(CHROMA_PATH):
    vector_db = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embedding_model
    )
    print("Existing ChromaDB Loaded")

else:
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=CHROMA_PATH
    )
    print("New ChromaDB Created")

retriever = vector_db.as_retriever(
    search_kwargs={"k": 3}
)

print("Retriever Ready")
# ==========================================================
# Groq Models
# ==========================================================

fast_llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="llama-3.1-8b-instant",
    temperature=0
)

smart_llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="llama-3.3-70b-versatile",
    temperature=0.2
)

print("Groq Models Loaded")
# ==========================================================
# Preference Agent
# ==========================================================

preference_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are the User Preference Agent for ExploreLK AI.

Your ONLY task is to analyse the user's travel preferences.

Return a short structured summary including:

- Budget
- Number of Days
- Starting Location
- Interests
- Preferred Categories

Do NOT recommend destinations.
Do NOT create itineraries.
"""
    ),
    (
        "human",
        """
Budget: {budget}

Days: {days}

Location: {location}

Interests: {interests}
"""
    )
])

preference_agent = (
    preference_prompt
    | fast_llm
    | StrOutputParser()
)

print("Preference Agent Ready")
# ==========================================================
# Destination Agent
# ==========================================================

destination_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are the Destination Recommendation Agent for ExploreLK AI.

Your job is to recommend hidden destinations in Sri Lanka.

Rules:

- Use ONLY the provided dataset.
- Recommend a maximum of 5 destinations.
- Match the user's budget.
- Match the user's interests.
- Do NOT create an itinerary.
- Do NOT provide travel tips.

Return your answer in this format ONLY:

Destination: <Place Name>
Reason: <Short reason>

Destination: <Place Name>
Reason: <Short reason>
"""
    ),
    (
        "human",
        """
User Preferences:

{preferences}

Dataset:

{dataset}
"""
    )
])

destination_agent = (
    destination_prompt
    | smart_llm
    | StrOutputParser()
)

print("Destination Agent Ready")
# ==========================================================
# RAG Prompt
# ==========================================================

rag_prompt = ChatPromptTemplate.from_template("""
You are ExploreLK AI.

Use ONLY the retrieved context below.

If the answer cannot be found in the context,
say "I don't have enough information."

Context:
{context}

Question:
{question}
""")


# ==========================================================
# RAG Agent
# ==========================================================

def rag_agent(question: str):

    docs = retriever.invoke(question)

    context = "\n\n".join(doc.page_content for doc in docs)

    messages = rag_prompt.format_messages(
        context=context,
        question=question
    )

    response = smart_llm.invoke(messages)

    return response.content


print("RAG Agent Ready")


# ==========================================================
# Itinerary Planner
# ==========================================================

planner_prompt = ChatPromptTemplate.from_template("""
You are ExploreLK AI's itinerary planner.

Based on the travel information below, create a simple itinerary.

Travel Information

{travel_info}

Include:

- Destination
- Activities
- Best Time
- Budget
- Travel Tips
""")


def itinerary_planner(travel_info: str):

    messages = planner_prompt.format_messages(
        travel_info=travel_info
    )

    response = smart_llm.invoke(messages)

    return response.content


print("Itinerary Planner Ready")
# ==========================================================
# LangGraph State
# ==========================================================

class TravelState(TypedDict):
    budget: str
    days: str
    location: str
    interests: str

    preferences: str
    destinations: str
    travel_info: str
    itinerary: str


# ==========================================================
# Nodes
# ==========================================================

def preference_node(state: TravelState):

    state["preferences"] = preference_agent.invoke({
        "budget": state["budget"],
        "days": state["days"],
        "location": state["location"],
        "interests": state["interests"]
    })

    return state


def destination_node(state: TravelState):

    state["destinations"] = destination_agent.invoke({
        "preferences": state["preferences"],
        "dataset": dataset_text
    })

    return state


def rag_node(state: TravelState):

    question = f"""
Provide detailed travel information about these recommended destinations.

Recommended Destinations:

{state["destinations"]}

Include:
- Best time to visit
- Activities
- Entry fees (if available)
- Travel tips
- Nearby attractions
"""

    state["travel_info"] = rag_agent(question)

    state["itinerary"] = itinerary_planner(
        state["travel_info"]
    )

    return state

# ==========================================================
# Build Graph
# ==========================================================

builder = StateGraph(TravelState)

builder.add_node("Preference", preference_node)
builder.add_node("Destination", destination_node)
builder.add_node("RAG", rag_node)

builder.add_edge(START, "Preference")
builder.add_edge("Preference", "Destination")
builder.add_edge("Destination", "RAG")
builder.add_edge("RAG", END)

travel_graph = builder.compile()

print("LangGraph Ready")


# ==========================================================
# Main Function
# ==========================================================

def generate_trip(
    budget,
    days,
    location,
    interests
):

    result = travel_graph.invoke({
        "budget": budget,
        "days": days,
        "location": location,
        "interests": interests
    })

    return result

print("Backend Ready")

# ==========================================================
# Backend Initializer
# ==========================================================

_backend_initialized = False

def initialize_backend():
    global _backend_initialized

    if _backend_initialized:
        return

    print("ExploreLK AI Backend Initialized")
    _backend_initialized = True
