from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import pickle

#NEED DATASET TO CREATE MODEL

vector = TfidfVectorizer()
X = vector.fit_transform(queries)

classifier = LogisticRegression()
classifier.fit(X,labels)
with open('query_classifier.pkl', 'wb') as f:
    pickle.dump((classifier, vector), f)
def classify_query(query):
    with open('query_classifier.pkl', 'rb') as f:
        classifier, vectorizer = pickle.load(f)
    query_vector = vectorizer.transform([query])
    prediction = classifier.predict(query_vector)
    return prediction[0]
query = "I want to know about the shipping time"
category = classify_query(query)
print(f"The query is categorized as: {category}")