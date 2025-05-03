from Product_indexBuild import product_index,faq_index
from Load_proIndex import load_product_engines,save_chat_to_firebase,load_faq_engines
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
import os

os.environ["GOOGLE_API_KEY"] = "AIzaSyDP459yeAgZvP0wlqppLt5zSusBtux1sd0"
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.7,
    max_tokens=1024
    )
Settings.llm = llm
Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
    )
product_index()
faq_index()
product_query_engine = load_product_engines()
faq_query_engine= load_faq_engines()

def get_last_line(chat_history):
    for message in reversed(chat_history):
        if message.get("role") == "user":
            return message.get("content", "").strip()
    return ""

def chatbot():
    chat_h = []
    while True:
        query = input("\nYou: ")
        if query.lower() == "exit":
            break
        chat_query = "\n".join(f"{msg['role'].capitalize()}: {msg['content']}" for msg in chat_h)
        print(chat_query)
        #add_query = chat_query + user_input
        #print(add_query)
        
        chat_prompt = PromptTemplate(
            input_variables=["query"],
            template = '''Classify the query as Product (about items) or FAQ (about service/policy/track).
Answer in one word only.

Query: {query}''')
        intent_run = chat_prompt | llm
        results = intent_run.invoke({"query": query}).content.strip().lower()
        print(results)
        #print(type(results))
        if results=='faq':
            response = faq_query_engine.query(query)
            print("\nBot:", response.response)
        elif results=='product':
            chat_history = get_last_line(chat_h)
            chat_h.append({"role": "user", "content": query})
            print(chat_history)
            chat_prompt = PromptTemplate(
            input_variables=["query","chat_history"],
            template = '''Analyze the full conversation and extract all relevant product filters (such as category, color, gender, size, price, etc.) based on the latest user query and previous queries.
Return the combined filters in structured JSON.

Chat History:
{chat_history}

Latest Query:
{query}

Complete Product Filters (JSON):
''')
            intent_run = chat_prompt | llm
            results = intent_run.invoke({"query": query,"chat_history":chat_history}).content.strip().lower()
            print(results)
        else:
            print("ohh i can't handle it. ")
        
    save_chat_to_firebase(chat_history)



if __name__ == "__main__":
    print("Clothing Shop Chatbot 🤖 (type 'exit' to quit)")
    chatbot()