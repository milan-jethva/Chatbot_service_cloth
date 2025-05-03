import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# ✅ Add Products
products = [
    {
        "name": "Do you offer Cash on Delivery?",
        "price": "",
        "category": "",
        "description": "Yes, we offer COD on orders above ₹300.",
        "link": "",
        "image_url": ""
    },
    
]

for product in products:
    db.collection("products").add(product)





