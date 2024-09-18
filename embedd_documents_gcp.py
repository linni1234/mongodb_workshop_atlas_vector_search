import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from langchain_google_vertexai.embeddings import VertexAIEmbeddings

# Get environment variables for configuration
first_last = os.getenv("first_last")
#gcp_project = os.getenv("GCP_PROJECT")  # Get GCP project from environment variables
#gcp_location = os.getenv("GCP_LOCATION")  # Get GCP location from environment variables

# LangChain's VertexAIEmbeddings class to generate embeddings
embedding_model = VertexAIEmbeddings(
    model_name="textembedding-gecko@003",  # Vertex AI text embedding model
    #project=gcp_project,                   # Pass the project from env variables
    #location=gcp_location                  # Pass the location from env variables
)

# MongoDB Initialization
client = AsyncIOMotorClient(os.getenv("MONGODB_URI"))
db = client[first_last]
collection = db[f"movies_{first_last}"]

# Function to generate embeddings using LangChain's Vertex AI in an async-safe way
async def generate_text_embedding(text):
    # The LangChain VertexAIEmbeddings object handles the embedding call.
    return embedding_model.embed_query(text)

# Process a single document to generate its embeddings and update MongoDB
async def process_document(doc):
    combined_text = f"{doc.get('title', '')} {doc.get('plot', '')} {doc.get('genres', [])}"
    print(f"Generating embeddings for {combined_text}")
    
    # Generate embeddings using LangChain Vertex AI
    doc_vector = await generate_text_embedding(combined_text)
    
    if doc_vector:
        await collection.update_one(
            {"_id": doc["_id"]}, {"$set": {"embedding": doc_vector}}
        )
        print(f"Document {doc['_id']} updated.")

# Process multiple documents from MongoDB
async def process_documents(batch_size=500,limit=100):
    cursor = collection.find({"embedding": {"$exists": False}}).batch_size(batch_size).limit(limit)
    
    async for doc in cursor:
        await process_document(doc)

# Run the processing
if __name__ == "__main__":
    asyncio.run(process_documents())