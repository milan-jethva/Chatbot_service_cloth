from faq_index_build import faq_index,load_faq_engines
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

def get_last_two_user_queries(chat_history):
    user_queries = []
    for message in reversed(chat_history):
        if message.get("role") == "user":
            user_queries.append(message.get("content", "").strip())
        if len(user_queries) == 2:
            break
    return list(reversed(user_queries))
def normalize_category(text):
    # Convert to lowercase and remove non-alphanumeric characters
    return re.sub(r'[^a-z0-9]', '', text.lower())
import re

def extract_query(response_text):
    match = re.search(r"^query:\s*(.+)$", response_text, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return None
def chatbot():
    chat_product_history = []
    chat_faq_history=[]
    while True:
        query = input("\nYou: ")
        if query.lower() == "exit":
            break     
        chat_query = "\n".join(f"{msg['role'].capitalize()}: {msg['content']}" for msg in chat_product_history)
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
            chat_faq_history.append({"role": "user", "content": query}) #adding user query to list - faq
            response = faq_query_engine.query(query)
            print("\nBot:", response.response)
            chat_faq_history.append({"role": "bot", "content": response.response})
        elif results=='product':
            chat_history = get_last_two_user_queries(chat_product_history)
            chat_product_history.append({"role": "user", "content": query})
            chat_prompt = PromptTemplate(
            input_variables=["query","chat_history"],
            template = '''You are a smart AI assistant that helps users shop for clothes.
Given the previous conversation ({chat_history}) and the new user input ({query}), respond with:

1. A dynamic sentence that sounds like a natural follow-up from a smart shopping assistant. It should show you're engaging, e.g., asking a clarifying question or confirming a detail (like size, sleeve type, etc.).

2. A line starting with "Query:" followed by a short, clean product-related query to use in search.

Format:

<Dynamic assistant message>

query: <short product query>
''')
            intent_run = chat_prompt | llm
            results = intent_run.invoke({"query": query,"chat_history":chat_history}).content.strip().lower()
            print("Bot answer/smart index query :" ,results)
            new_ext_query = extract_query(results)
            print(new_ext_query)
            product_result = smartIndex(new_ext_query)
            print(product_result)
            chat_product_history.append({"role": "bot", "content": product_result})

            
            # Define regex patterns to extract category and color lists
            '''category_pattern = r'"category":\s*\[(.*?)\]'
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
        



if __name__ == "__main__":
    print("Clothing Shop Chatbot 🤖 (type 'exit' to quit)")
    chatbot()