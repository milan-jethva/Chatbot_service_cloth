from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import pickle

#NEED DATASET TO CREATE MODEL
import pandas as pd

# Load product queries
with open("D:/ChatbotEcom/DatasetForfaqorpro/ecommerce_product.txt", "r", encoding="utf-8") as f:
    product_data = f.read().split(",")

# Load FAQ queries
with open("D:/ChatbotEcom/DatasetForfaqorpro/ecommerce_faqs.txt", "r", encoding="utf-8") as f:
    faq_data = f.read().split(",")

# Create DataFrame
df = pd.DataFrame({
    "text": product_data + faq_data,
    "label": [0]*len(product_data) + [1]*len(faq_data)  # 0 = product, 1 = FAQ
})

# Optional: Remove extra whitespace
df["text"] = df["text"].str.strip()
vectorizer = TfidfVectorizer(max_features=5000)
X = vectorizer.fit_transform(df["text"])
y = df["label"]

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = LogisticRegression()
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))
with open('query_classifier.pkl', 'wb') as f:
    pickle.dump((model, vectorizer), f)
def classify_query(query):
    with open('query_classifier.pkl', 'rb') as f:
        classifier, vectorizer = pickle.load(f)
    query_vector = vectorizer.transform([query])
    prediction = classifier.predict(query_vector)
    return prediction[0]
query = "do you have men black t shirt"
category = classify_query(query)
print(f"The query is categorized as: {category}")