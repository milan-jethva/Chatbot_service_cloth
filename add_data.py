import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# ✅ Add Products
products = [
    {
        "name": "Classic Cotton T-Shirt - Black",
        "price": "₹499",
        "category": "T-Shirt",
        "description": "A classic black t-shirt made from 100% breathable cotton. Ideal for daily wear.",
        "link": "https://example.com/product/black-cotton",
        "image_url": "https://example.com/images/black-cotton.jpg"
    },
    {
        "name": "Slim Fit V-Neck T-Shirt - White",
        "price": "₹599",
        "category": "T-Shirt",
        "description": "White V-neck slim-fit t-shirt with a soft finish. Great for layering or wearing solo.",
        "link": "https://example.com/product/white-vneck",
        "image_url": "https://example.com/images/white-vneck.jpg"
    },
    {
        "name": "Oversized Graphic T-Shirt - Navy Blue",
        "price": "₹699",
        "category": "T-Shirt",
        "description": "Oversized t-shirt with abstract graphic print. 100% cotton, navy blue.",
        "link": "https://example.com/product/navy-graphic",
        "image_url": "https://example.com/images/navy-graphic.jpg"
    },
    {
        "name": "Round Neck Performance T-Shirt - Red",
        "price": "₹649",
        "category": "T-Shirt",
        "description": "Moisture-wicking red t-shirt for workouts and sports. Polyester blend.",
        "link": "https://example.com/product/red-performance",
        "image_url": "https://example.com/images/red-performance.jpg"
    },
    {
        "name": "Henley T-Shirt - Olive Green",
        "price": "₹749",
        "category": "T-Shirt",
        "description": "Stylish Henley t-shirt with 3-button placket. Olive green, soft cotton.",
        "link": "https://example.com/product/olive-henley",
        "image_url": "https://example.com/images/olive-henley.jpg"
    },
    {
        "name": "Striped Casual T-Shirt - Blue & White",
        "price": "₹599",
        "category": "T-Shirt",
        "description": "Casual striped t-shirt in blue and white. Lightweight and perfect for summer.",
        "link": "https://example.com/product/striped-bluewhite",
        "image_url": "https://example.com/images/striped-bluewhite.jpg"
    },
    {
        "name": "Solid Polo T-Shirt - Maroon",
        "price": "₹799",
        "category": "T-Shirt",
        "description": "Solid maroon polo t-shirt with a premium collar. Perfect for semi-casual outings.",
        "link": "https://example.com/product/maroon-polo",
        "image_url": "https://example.com/images/maroon-polo.jpg"
    },
    {
        "name": "Long Sleeve T-Shirt - Grey Melange",
        "price": "₹699",
        "category": "T-Shirt",
        "description": "Comfortable grey long-sleeve t-shirt made from soft blend fabric.",
        "link": "https://example.com/product/grey-long",
        "image_url": "https://example.com/images/grey-long.jpg"
    },
    {
        "name": "Printed T-Shirt - Yellow with Text",
        "price": "₹549",
        "category": "T-Shirt",
        "description": "Bright yellow t-shirt with bold 'Stay Humble' print. Cotton-rich fabric.",
        "link": "https://example.com/product/yellow-print",
        "image_url": "https://example.com/images/yellow-print.jpg"
    },
    {
        "name": "Eco-friendly Bamboo T-Shirt - Light Brown",
        "price": "₹899",
        "category": "T-Shirt",
        "description": "Sustainable bamboo fiber t-shirt in earthy light brown. Ultra-soft and breathable.",
        "link": "https://example.com/product/bamboo-brown",
        "image_url": "https://example.com/images/bamboo-brown.jpg"
    },
]


for product in products:
    db.collection("products").add(product)





