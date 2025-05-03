# 🔧 Install Required Packages
# pip install openai langchain llama-index firebase-admin

import firebase_admin
from firebase_admin import credentials, firestore
from llama_index.core import Document, VectorStoreIndex, Settings
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import json
from langchain_google_genai import ChatGoogleGenerativeAI
import os
os.environ["GOOGLE_API_KEY"] = "AIzaSyBAMMgRvgEpVIhZAGB3_WGYxfrC03MvOD0"

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.7,
    max_tokens=1024
)
# ----------------------
# 1. Firebase Setup
# ----------------------
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# ----------------------
# 2. Initialize LLM and Context
# ----------------------

Settings.llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.7,
    max_tokens=1024
)
# ----------------------
# 3. Load FAQs from Firebase
# ----------------------
faq_docs = db.collection("faqs").stream()
faq_texts = [f"Q: {d.to_dict()['question']}\nA: {d.to_dict()['answer']}" for d in faq_docs]
faq_documents = [Document(text=t) for t in faq_texts]
faq_index = VectorStoreIndex.from_documents(faq_documents)
faq_query_engine = faq_index.as_query_engine()

# ----------------------
# 4. Load Products from Firebase

product_docs = db.collection("products").stream()
products_data = [d.to_dict() for d in product_docs]

# Convert product data to searchable text
product_texts = [
    f"{p['name']} - ₹{p['price']}, Category: {p['category']}, Description: {p['description']}, Link: {p['link']}, Image: {p['image_url']}"
    for p in products_data
]
product_documents = [Document(text=t) for t in product_texts]
product_index = VectorStoreIndex.from_documents(product_documents)
product_query_engine = product_index.as_query_engine()

# ----------------------
# 5. Classify Intent (FAQ or Product)
# ----------------------
intent_prompt = PromptTemplate(
    input_variables=["query"],
    template="""
You are a chatbot. Classify the user's intent.

Query: "{query}"

Reply with one word: "faq" or "product"
"""
)
intent_chain = LLMChain(llm=llm, prompt=intent_prompt)

# ----------------------
# 6. Handle User Input
# ----------------------
def chatbot():
    while True:
        query = input("\n👤 You: ")
        if query.lower() in ["exit", "quit"]:
            break

        intent = intent_chain.run(query=query).strip().lower()

        if intent == "faq":
            answer = faq_query_engine.query(query)
            print(f"🤖 FAQ Answer:\n{answer}")

        elif intent == "product":
            results = product_query_engine.query(query)
            print(f"🛍️ Product Result:\n{results}")

        else:
            print("🤖 Sorry, I couldn't understand the query type.")

# ----------------------
# 7. Run the Bot
# ----------------------
if __name__ == "__main__":
    print("🧠 Welcome to the AI Shop Assistant!")
    print("Type your question or 'exit' to quit.")
    chatbot()
