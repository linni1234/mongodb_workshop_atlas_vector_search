import os
from pymongo import MongoClient
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_openai import AzureOpenAIEmbeddings
import json

# Load environment variables
MONGODB_URI = os.getenv("MONGODB_URI")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
first_last = os.getenv("first_last")

# initialize MongoDB python client using the environment variable for the URI
client = MongoClient(MONGODB_URI)
DB_NAME = first_last  
COLLECTION_NAME = f"movies_{first_last}"  
ATLAS_VECTOR_SEARCH_INDEX_NAME = f"langchain-test-index-vectorstores_{first_last}"  
MONGODB_COLLECTION = client[DB_NAME][COLLECTION_NAME]

# initialize Azure OpenAI using environment variables
embeddings = AzureOpenAIEmbeddings(
    openai_api_key=AZURE_OPENAI_API_KEY,
    model="text-embedding-ada-002",
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
)

# Prompt user for input text
input_text = input("Please enter the film you want to search for: ")

# Initialize MongoDBAtlasVectorSearch with the index
vectorstore = MongoDBAtlasVectorSearch(
    collection=MONGODB_COLLECTION,
    embedding_key="azure_openai_vector",
    index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
    relevance_score_fn="euclidean",
    embedding=AzureOpenAIEmbeddings,
    text_key="title",
)

# Create the query embeddings
query = embeddings.embed_query(input_text)

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