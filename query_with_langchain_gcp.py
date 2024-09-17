import os
from pymongo import MongoClient
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_google_vertexai.embeddings import VertexAIEmbeddings
import json

# Load environment variables
MONGODB_URI = os.getenv("MONGODB_URI")
first_last = os.getenv("first_last")
gcp_project = os.getenv("GCP_PROJECT")  # Get GCP project from environment variables
gcp_location = os.getenv("GCP_LOCATION")  # Get GCP location from environment variables

# Initialize Vertex AI embeddings using LangChain's VertexAIEmbeddings class
embedding_model = VertexAIEmbeddings(
    model_name="textembedding-gecko@003",  # The model to use for text embeddings
    project=gcp_project,                   # Use the project from environment variables
    location=gcp_location                  # Use the location from environment variables
)

# Initialize MongoDB python client using the environment variable for the URI
client = MongoClient(MONGODB_URI)
DB_NAME = first_last  
COLLECTION_NAME = f"movies_{first_last}"  
ATLAS_VECTOR_SEARCH_INDEX_NAME = f"langchain-test-index-vectorstores_{first_last}"  
MONGODB_COLLECTION = client[DB_NAME][COLLECTION_NAME]

# Prompt user for input text
input_text = input("Please enter the film you want to search for: ")

# Initialize MongoDBAtlasVectorSearch with the index and Vertex AI embeddings
vectorstore = MongoDBAtlasVectorSearch(
    collection=MONGODB_COLLECTION,
    embedding_key="embedding",
    index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
    relevance_score_fn="euclidean",
    embedding=embedding_model,  # Use VertexAIEmbeddings here
    text_key="title",
)

# Create the query embeddings using Vertex AI
query = embedding_model.embed_query(input_text)

# Define the post-filter pipeline
post_filter_pipeline = [{"$project": {"title": 1, "score": 1, "plot": 1, "genres": 1, "_id": 0}}]

# Define the query filter
pre_filter_query = {"genres": {"$in": ["Drama", "Comedy"]}}

# Perform vector search using the query vector
results = vectorstore._similarity_search_with_score(
    query_vector=query,
    k=10,  
    post_filter_pipeline=post_filter_pipeline,
    pre_filter=pre_filter_query
)

# Display results
for doc, score in results:
    # Convert the Document object to a dictionary
    doc_dict = doc.to_dict() if hasattr(doc, "to_dict") else dict(doc)
    
    # Print the document in pretty-printed JSON format
    print(json.dumps(doc_dict, indent=4))
    print(f"Score: {score}")