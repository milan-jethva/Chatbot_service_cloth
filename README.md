# Company Chatbot Service – Smart FAQ & Product Query Assistant

**Company Chatbot** is an AI-powered assistant designed to answer both FAQ and product-related queries from users. It’s built for businesses to provide instant, intelligent responses — whether it’s about **product pricing**, **availability**, or general **company information**.

## 🔍 What It Can Do

- Answer product-related queries like:
  - “What is the price of [Product X]?”
  - “Is [Product Y] in stock?”
- Handle common FAQs such as:
  - “What is your return policy?”
  - “Do you offer international shipping?”
- Supports natural, human-like language understanding

---

## 💡 Use Cases

- E-commerce platforms
- SaaS companies
- Retail stores
- Internal helpdesk automation

## Tech Stack

| Layer             | Technology                  |
|------------------|-----------------------------|
| 🔗 NLP Model      | Google Gemini API            |
| 🔎 Vector Search  | FAISS                        |
| 🧠 Embedding/Data | Google Gemini / LangChain     |
| 🗂️ Database       | Firestore (for products + FAQs) |
| 🧰 Backend        | FastAPI |

## How It Works

1. **User sends a question** in natural language.
2. Query is **vectorized** using Gemini embeddings.
3. **FAISS** searches for the closest match in the knowledge base (FAQs + product info).
4. The top result and context are sent to **Gemini API** for a conversational response.
5. Chatbot returns a clear, contextual answer to the user.

## 🧾 Example Queries

| User Question                              | Bot Response                             |
|-------------------------------------------|------------------------------------------|
| "How much does the iPhone 15 cost?"       | "The iPhone 15 is priced at ₹79,900."    |
| "Is the wireless charger in stock?"       | "Yes, the wireless charger is available."|
| "Can I return a product after 30 days?"   | "Our return policy allows returns within 15 days."|

---


