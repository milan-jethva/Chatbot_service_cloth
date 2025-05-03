import os
os.environ["TORCH_USE_RTLD_GLOBAL"] = "1"
import streamlit as st
st.set_page_config(page_title="AI Shop Assistant", page_icon="🛍️")
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
from llama_index.core import Document, VectorStoreIndex, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
import os

# --- Initialize Firebase ---
cred = credentials.Certificate("serviceAccountKey.json")
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
db = firestore.client()

# --- Setup Gemini LLM ---
os.environ["GOOGLE_API_KEY"] = "AIzaSyDP459yeAgZvP0wlqppLt5zSusBtux1sd0"
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.7, max_tokens=1024)
Settings.llm = llm
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

# --- Load and Index Product Data ---
@st.cache_resource
def load_product_index():
    product_docs = db.collection("products").stream()
    product_data = [doc.to_dict() for doc in product_docs]
    product_texts = [
        f"{p['name']} - ₹{p['price']}, Category: {p['category']}, Description: {p['description']}, Link: {p['link']}, Image: {p['image_url']}"
        for p in product_data
    ]
    documents = [Document(text=text) for text in product_texts]
    index = VectorStoreIndex.from_documents(documents)
    return index.as_query_engine()

product_query_engine = load_product_index()

# --- Prompt Template ---
prompt_template = PromptTemplate(
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
intent_chain = prompt_template | llm

# --- Save Chat to Firebase ---
def save_chat_to_firebase(chat_history):
    timestamp = datetime.now().isoformat()
    db.collection("chats").add({
        "timestamp": timestamp,
        "history": chat_history
    })

# --- Streamlit UI ---
st.set_page_config(page_title="AI Shop Assistant", page_icon="🛍️")
st.title("🛍️ AI Shop Assistant")
st.markdown("Ask me anything about our clothing products!")

# --- Session State ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

query = st.chat_input("Type your message...")

if query:
    st.session_state.chat_history.append({"role": "user", "content": query})

    # Context for the LLM
    chat_context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.chat_history])
    product_context = str(product_query_engine.query(query))

    # Get Response
    response = intent_chain.invoke({
        "query": query,
        "chat_context": chat_context,
        "product_context": product_context
    }).content.strip()

    st.session_state.chat_history.append({"role": "bot", "content": response})

# --- Display Chat Messages ---
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Option to Save Chat ---
if st.button("💾 Save Chat"):
    save_chat_to_firebase(st.session_state.chat_history)
    st.success("Chat saved to Firebase!")

