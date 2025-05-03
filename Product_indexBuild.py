#Importing Library
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Document, VectorStoreIndex, Settings


#setup PRoduct indexes
cred = credentials.Certificate('serviceAccountKey.json')
app = firebase_admin.initialize_app(cred)
db= firestore.client()

from google.cloud.firestore_v1 import FieldFilter

def search_products(category, color, size):
    query_ref = db.collection("products")

    if category:
        query_ref = query_ref.where(filter=FieldFilter("index", "array_contains", category))
    if color:
        query_ref = query_ref.where(filter=FieldFilter("color", "==", color))
    if size:
        query_ref = query_ref.where(filter=FieldFilter("size", "==", size))

    results = query_ref.stream()
    if not results:
        print("No matching products found.")
    else:
        print("Matching products:")
        for doc in results:
            print(doc.id, doc.to_dict())


def product_index():
    product_doc = db.collection("products").stream()
    product_data = [d.to_dict() for d in product_doc]
    product_texts = [
        f"{p['name']} - ₹{p['price']}, Category: {p['category']}, Description: {p['description']}, Link: {p['link']}, Image: {p['image_url']}"
        for p in product_data
    ]
    product_documents = [Document(text=t) for t in product_texts]
    index = VectorStoreIndex.from_documents(product_documents)
    index.storage_context.persist(persist_dir="./product_index")
    return index 
def faq_index():
    db_ref  = db.collection("faqs").stream()
    faq_texts = [f"Q: {d.to_dict()['question']}\nA: {d.to_dict()['answer']}" for d in db_ref]
    faq_doc = [Document(text=t) for t in faq_texts]
    faq_vec = VectorStoreIndex.from_documents(faq_doc)
    faq_vec.storage_context.persist(persist_dir="./faq_index")
    return faq_vec