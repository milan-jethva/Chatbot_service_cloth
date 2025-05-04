#Importing Library
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from llama_index.core import Document, VectorStoreIndex
from llama_index.core import load_index_from_storage, StorageContext
from datetime import datetime

#setup PRoduct indexes
cred = credentials.Certificate('serviceAccountKey.json')
app = firebase_admin.initialize_app(cred)
db= firestore.client()

def faq_index():
    db_ref  = db.collection("faqs").stream()
    faq_texts = [f"Q: {d.to_dict()['question']}\nA: {d.to_dict()['answer']}" for d in db_ref]
    faq_doc = [Document(text=t) for t in faq_texts]
    faq_vec = VectorStoreIndex.from_documents(faq_doc)
    faq_vec.storage_context.persist(persist_dir="./faq_index")
    return faq_vec

def save_chat_to_firebase(chat_history):
    db = firestore.client()
    timestamp = datetime.now().isoformat()
    chat_data = {
        "timestamp": timestamp,
        "history": chat_history  # list of {"role": ..., "content": ...}
    }
    db.collection("chats").add(chat_data)

def load_faq_engines():
    product_ctx = StorageContext.from_defaults(persist_dir="./faq_index")
    product_index = load_index_from_storage(product_ctx)
    faq_engine = product_index.as_query_engine(similarity_top_k=3)
    return faq_engine