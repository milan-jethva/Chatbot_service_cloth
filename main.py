from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from faq_index_build import faq_index,load_faq_engines
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
from smartIndex import smartIndex
import os

os.environ["GOOGLE_API_KEY"] = "AIzaSyDP459yeAgZvP0wlqppLt5zSusBtux1sd0"
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.7,
    max_tokens=1024
    )
Settings.llm = llm
Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
    )

faq_index()
faq_query_engine= load_faq_engines()

app = FastAPI()

# Allow frontend calls (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
chat_h = []

class Message(BaseModel):
    message: str

@app.post("/chat")
def chat_api(data: Message):
    query = data.message
    chat_h.append({"role": "user", "content": query})

    # Classify intent
    intent_prompt = PromptTemplate(
        input_variables=["query"],
        template='''Classify the query as Product (about items) or FAQ (about service/policy/track).
Answer in one word only.

Query: {query}'''
    )
    intent = (intent_prompt | llm).invoke({"query": query}).content.strip().lower()

    if intent == 'faq':
        response = faq_query_engine.query(query)
        return {"type": "faq", "reply": response.response}

    elif intent == 'product':
        return smartIndex(query)
        
    else:
        return {"type": "unknown", "reply": "Sorry, I can't handle that."}

