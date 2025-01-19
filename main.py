import os
import warnings
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # Import CORSMiddleware
from pydantic import BaseModel
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_astradb.vectorstores import AstraDBVectorStore
from langchain_groq import ChatGroq
from astrapy import DataAPIClient
import json  # Import JSON to handle user_data

# Suppress warnings
warnings.filterwarnings("ignore")

# Load environment variables
load_dotenv()

# FastAPI app instance
app = FastAPI()

# Add CORS middleware
origins = [
    "*",  # Allow all origins (be cautious with this in production)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

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


# Function to get relevant documents from AstraDB
def get_relevant_documents(query: str):
    return searcher.similarity_search(query)


# Function to generate response based on query and user_data
def gen(query: str, user_data: dict):
    # Convert user_data into a string representation
    user_data_str = json.dumps(
        user_data
    )  # You can modify how you serialize the user data

    # Combine the query with the user data to form a rich prompt
    full_prompt = f"Query: {query}\nUser Data: {user_data_str}"

    relevant_docs = get_relevant_documents(query)

    if relevant_docs:
        # Now use the full_prompt including user_data and the relevant document
        response = model.invoke(
            full_prompt + "\nRelevant Document: " + str(relevant_docs[0])
        )  # Add the document context
        return response
    return "No relevant documents found."


# Pydantic model for request validation
class QueryRequest(BaseModel):
    query: str
    user_data: dict


# Endpoint to handle queries
@app.post("/generate/")
async def generate_response(request: QueryRequest):
    try:
        # Pass both query and user_data to the gen function
        response = gen(request.query, request.user_data)
        return {"response": response.content}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating response: {str(e)}"
        )
