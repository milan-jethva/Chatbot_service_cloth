from llama_index.core import load_index_from_storage, StorageContext
from datetime import datetime
from firebase_admin import firestore

def save_chat_to_firebase(chat_history):
    db = firestore.client()
    timestamp = datetime.now().isoformat()

    chat_data = {
        "timestamp": timestamp,
        "history": chat_history  # list of {"role": ..., "content": ...}
    }

    db.collection("chats").add(chat_data)


def load_product_engines():
    product_ctx = StorageContext.from_defaults(persist_dir="./product_index")
    product_index = load_index_from_storage(product_ctx)
    product_engine = product_index.as_query_engine(similarity_top_k=3)
    return product_engine
def load_faq_engines():
    product_ctx = StorageContext.from_defaults(persist_dir="./faq_index")
    product_index = load_index_from_storage(product_ctx)
    faq_engine = product_index.as_query_engine(similarity_top_k=3)
    return faq_engine