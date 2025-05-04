from faq_index_build import product_index,faq_index,search_products
from faq_index_build import load_product_engines,save_chat_to_firebase,load_faq_engines
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
from smartIndex import smartIndex
import os
import re
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
#product_index()
faq_index()
#product_query_engine = load_product_engines()
faq_query_engine= load_faq_engines()

def get_last_line(chat_history):
    for message in reversed(chat_history):
        if message.get("role") == "user":
            return message.get("content", "").strip()
    return ""
def normalize_category(text):
    # Convert to lowercase and remove non-alphanumeric characters
    return re.sub(r'[^a-z0-9]', '', text.lower())

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
            smartIndex(query)
            #chat_prompt = PromptTemplate(
            #input_variables=["query"],
            #'''template = '''Extract relevant product filters (category, color, size) based on the user query.
#Return the filters as a structured JSON object, listing the extracted values under each filter.

#Query:
#{query}

#Extracted Product Filters (JSON):
#{{
#  "category": [],  # List of extracted categories (e.g., ["tshirt", "dress"])
#  "color": [],     # List of extracted colors (e.g., ["black", "blue"])
#  "size": []       # List of extracted sizes (e.g., ["M", "L", "XL"])
#}}
#''')
            '''intent_run = chat_prompt | llm
            results = intent_run.invoke({"query": query}).content.strip().lower()
            print(results)
            # Define regex patterns to extract category and color lists
            category_pattern = r'"category":\s*\[(.*?)\]'
            color_pattern = r'"color":\s*\[(.*?)\]'
            size_pattern = r'"size":\s*\[(.*?)\]'
            # Extract category and color lists using regex
            category_match = re.search(category_pattern, results)
            color_match = re.search(color_pattern, results)
            size_match = re.search(size_pattern, results)
            # Parse the matched strings into actual lists
            category = category_match.group(1).replace('"', '').split(',') if category_match else []
            color = color_match.group(1).replace('"', '').split(',') if color_match else []
            size = size_match.group(1).replace('"', '').split(',') if size_match else []
            # Print the extracted data
            print("Category:", category)
            print("Color:", color)
            #category_str = ', '.join(category)
            #color_str = ', '.join(color)
            #size_str = ', '.join(size)
            #category_norm = normalize_category(category_str)
            #print(category_norm,color_str,size_str)
            #search_products(category_norm, color_str,size_str)'''
        else:
            print("ohh i can't handle it. ")
        
    save_chat_to_firebase(chat_history)



if __name__ == "__main__":
    print("Clothing Shop Chatbot 🤖 (type 'exit' to quit)")
    chatbot()