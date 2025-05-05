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
import re

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

def get_last_two_user_queries(chat_history):
    user_queries = []
    for message in reversed(chat_history):
        if message.get("role") == "user":
            user_queries.append(message.get("content", "").strip())
        if len(user_queries) == 2:
            break
    return list(reversed(user_queries))

def extract_query(response_text):
    match = re.search(r"^query:\s*(.+)$", response_text, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return response_text
app = FastAPI()

# Allow frontend calls (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
chat_product_history = []
chat_faq_history=[]
class Message(BaseModel):
    message: str

@app.post("/chat")
def chat_api(data: Message):
    query = data.message
    chat_product_history.append({"role": "user", "content": query})

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
        chat_history = get_last_two_user_queries(chat_product_history)
        chat_product_history.append({"role": "user", "content": query})
        chat_prompt = PromptTemplate(
        input_variables=["query","chat_history"],
            template = '''You are a smart AI assistant that helps users shop for clothes.
Given the previous conversation ({chat_history}) and the new user input ({query}), respond with:

1. A dynamic sentence that sounds like a natural follow-up from a smart shopping assistant. It should show you're engaging, e.g., asking a clarifying question or confirming a detail (like size, sleeve type, etc.).

2. A line starting with "Query:" followed by a short, clean product-related query to use in search.

Format:

<Dynamic assistant message>

query: <short product query>
''')
        intent_run = chat_prompt | llm
        results = intent_run.invoke({"query": query,"chat_history":chat_history}).content.strip().lower()
            
        new_ext_query = extract_query(results)
           
        product_result = smartIndex(new_ext_query)
        
        chat_product_history.append({"role": "bot", "content": product_result})
        return {"bot : ":results , "product":product_result}
    else:
        return {"type": "unknown", "reply": "Sorry, I can't handle that."}

