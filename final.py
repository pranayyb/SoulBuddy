import os
import warnings
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_astradb.vectorstores import AstraDBVectorStore
from langchain_groq import ChatGroq
from astrapy import DataAPIClient

# Suppress warnings
warnings.filterwarnings("ignore")

# Load environment variables
load_dotenv()

# Initialize HuggingFace embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Initialize AstraDB client
client = DataAPIClient(os.getenv("ASTRA_DB_APPLICATION_TOKEN"))
db = client.get_database_by_api_endpoint(os.getenv("ASTRA_DB_API_ENDPOINT"))
collection = db["final_boss2"]

# Initialize Groq model
model = ChatGroq(
    model="mixtral-8x7b-32768",
    temperature=0.4,
    max_retries=2,
)

# Initialize AstraDB Vector Store
searcher = AstraDBVectorStore(
    embedding=embeddings,
    collection_name="final_boss2",
    api_endpoint=os.getenv("ASTRA_DB_API_ENDPOINT"),
    token=os.getenv("ASTRA_DB_APPLICATION_TOKEN"),
)


def get_relevant_documents(query):
    return searcher.similarity_search(query)


def gen(query):
    relevant_docs = get_relevant_documents(query)
    if relevant_docs:
        response = model.invoke(str(relevant_docs[0]))  # Use the most relevant document
        return response
    return "No relevant documents found."


# Example query and response generation
response = gen("what are gemstones?")
print(response.content)
