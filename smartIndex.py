from sentence_transformers import SentenceTransformer
from firebase_admin import firestore
import numpy as np
import faiss
# Initialize the model

model = SentenceTransformer("all-MiniLM-L6-v2")
db = firestore.client()

products_ref = db.collection("products")
docs = list(products_ref.stream())  # Store docs as a list to re-iterate

for doc in docs:
    product_id = doc.id
    product_data = doc.to_dict()

    # Build the text to embed (title + description)
    text_to_embed = product_data.get("name", "") + " " + product_data.get("description", "")

    # Generate the embedding
    embedding = model.encode(text_to_embed).tolist()  # Convert NumPy array to list

    # Save embedding back to Firestore
    products_ref.document(product_id).update({
        "embedding": embedding
    })

    print(f"✅ Updated embedding for product: {product_data.get('name')}")


product_list = []
embeddings = []

for doc in docs:
    data = doc.to_dict()
    product_list.append(data)
    embeddings.append(data["embedding"])

    # Convert embeddings to numpy array (should be 2D)
embeddings = np.array(embeddings)

    # Step 3: Initialize FAISS Index with correct dimensions (embedding size)
embedding_dim = embeddings.shape[1]  # Size of the embedding vector (should match your model, e.g., 384 for MiniLM)
index = faiss.IndexFlatL2(embedding_dim)  # L2 distance-based index

    # Add embeddings to the FAISS index
index.add(embeddings)
def smartIndex(query):
    # Step 4: Query for similar products
    #query = "I want a black t-shirt"
    query_vector = model.encode([query])[0]  # Convert query to embedding (1D vector)

    # Search the FAISS index for the top 3 most similar products
    D, I = index.search(np.array([query_vector]), k=3)

    # Step 5: Format the response with top products
    top_products = [product_list[i] for i in I[0]]

    # Display the top products (with image, link, etc.)
    i=0
    m={}
    for product in top_products:
        message = f"""
    👕 *{product['name']}*
    💰 {product['price']}
    🔗 [View Product]({product['link']})
    🖼️ Image: {product['image_url']}
    """
        
        m[i] = message 
        i+=1
    return m
