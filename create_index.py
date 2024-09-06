import os
from langchain_mongodb.vectorstores import MongoDBAtlasVectorSearch
from pymongo import MongoClient

# Load the first_last environment variable
first_last = os.getenv("first_last")

# Initialize MongoDB python client using the environment variable for MongoDB URI
MONGODB_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGODB_URI)

DB_NAME = first_last  
COLLECTION_NAME = f"movies_{first_last}"  
ATLAS_VECTOR_SEARCH_INDEX_NAME = f"langchain-test-index-vectorstores_{first_last}"  
MONGODB_COLLECTION = client[DB_NAME][COLLECTION_NAME]

# Initialize the MongoDBAtlasVectorSearch object
vectorstore = MongoDBAtlasVectorSearch(
    collection=MONGODB_COLLECTION,
    embedding_key="azure_openai_vector",
    index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
    relevance_score_fn="euclidean",
    embedding="azure_openai_vector",
)

# Create the vector search index with dimensions and filters
vectorstore.create_vector_search_index(
    dimensions=1536,
    filters=["genres", "year"],
    # update=True  # Uncomment if you want to update the index
)