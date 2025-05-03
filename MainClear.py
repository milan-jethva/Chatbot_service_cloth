import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from llama_index.core import Document, VectorStoreIndex, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from langchain.prompts import PromptTemplate
from datetime import datetime

def save_chat_to_firebase(chat_history):
    db = firestore.client()
    timestamp = datetime.now().isoformat()

    chat_data = {
        "timestamp": timestamp,
        "history": chat_history  # list of {"role": ..., "content": ...}
    }

    db.collection("chats").add(chat_data)

#Firebase Setup 
cred = credentials.Certificate('serviceAccountKey.json')
app = firebase_admin.initialize_app(cred)
db= firestore.client()

#GeminiModel Setup
'''import os
os.environ["GOOGLE_API_KEY"] = ""
llm = GoogleGenAI(
    model="gemini-2.0-flash",
)'''
'''from langchain_google_genai import ChatGoogleGenerativeAI
import os
os.environ["GOOGLE_API_KEY"] = "AIzaSyDP459yeAgZvP0wlqppLt5zSusBtux1sd0"

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.7,
    max_tokens=1024
)'''





#Setup- Faqs
'''db_ref  = db.collection("faqs").stream()
faq_texts = [f"Q: {d.to_dict()['question']}\nA: {d.to_dict()['answer']}" for d in db_ref]'''
'''Settings.llm = llm
Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)'''
'''faq_doc = [Document(text=t) for t in faq_texts]
faq_vec = VectorStoreIndex.from_documents(faq_doc)
faq_query_engine = faq_vec.as_query_engine()
response = faq_query_engine.query("Do you offer COD?")
print(response)'''

#Setup - products

#faq_docs = db.collection("faqs").stream()
#faq_texts = [f"Q: {d.to_dict()['question']}\nA: {d.to_dict()['answer']}" for d in faq_docs]
'''product_doc = db.collection("products").stream()
product_data = [d.to_dict() for d in product_doc]
product_texts = [
    f"{p['name']} - ₹{p['price']}, Category: {p['category']}, Description: {p['description']}, Link: {p['link']}, Image: {p['image_url']}"
    for p in product_data
]
#all_texts = faq_texts + product_texts
product_documents = [Document(text=t) for t in product_texts]
product_index = VectorStoreIndex.from_documents(product_documents) '''
product_query_engine = product_index.as_query_engine()

#Creating Prompt Template


#Saving Chat in firestore
def chatbot():  
    chat_history=[]
    while True:     
        results=" "
        query = input("\n👤 You: ")
        query +=results
        if query.lower() in ["exit", "quit"]:
            break
        chat_history.append({"role": "user", "content": query})
        #context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in chat_history])
        # Use LlamaIndex to fetch relevant product info
        product_response = product_query_engine.query(query)
        product_context = str(product_response)

        # Include both chat history and product context
        chat_context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in chat_history])
        #context = f"{chat_context}\n\nRelevant Product Info:\n{product_context}"
        #intent = intent_chain.invoke({"query": query}).content.strip().lower()
        
        #results = product_query_engine.query(context)
        intent_temp = PromptTemplate(
            input_variables=["query", "product_context", "chat_context"],
            template="""
            You are a helpful shopping assistant.

            Previous conversation:
            {chat_context}

            Relevant product information:
            {product_context}
            If the current question refers to a product discussed earlier (e.g. "what's the price", "show image"), assume the user is asking about the most recent product.

            Question: {query}

            Answer:
            """
)

        intent_run = intent_temp | llm
        results = intent_run.invoke({"query": query,"product_context": product_context,"chat_context": chat_context}).content.strip().lower()
        print(type(results))
        print(f"🛍️ Product Result:\n{results}")
        chat_history.append({"role": "bot", "content": str(results)})

    save_chat_to_firebase(chat_history)
# ----------------------
# 7. Run the Bot
# ----------------------
if __name__ == "__main__":
    print("🧠 Welcome to the AI Shop Assistant!")
    print("Type your question or 'exit' to quit.")
    chatbot()