import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from langchain_google_vertexai.embeddings import VertexAIEmbeddings
from pymongo import UpdateOne

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
collection = db[f"routes_{first_last}"]

# Function to generate embeddings using LangChain's Vertex AI
async def generate_text_embedding(text):
    return embedding_model.embed_query(text)

# Process a batch of documents concurrently
async def process_batch(documents):
    requests = []
    for doc in documents:
        combined_text = f"Flight from {doc.get('src_airport', '')} to {doc.get('dst_airport', '')} with {doc['airline']['name']}"
        print(f"Generating embeddings for {combined_text}")
        
        # Generate embeddings asynchronously
        doc_vector = await generate_text_embedding(combined_text)
        
        if doc_vector:
            # Prepare batch update request
            requests.append(
                UpdateOne(
                    {"_id": doc["_id"]}, 
                    {"$set": {"embedding": doc_vector}}
                )
            )
    
    # Perform batch update
    if requests:
        await collection.bulk_write(requests)
        print(f"Batch updated {len(requests)} documents.")

# Process multiple documents in batches
async def process_documents(batch_size=100,limit=100):
    cursor = collection.find({"embedding": {"$exists": False}}).batch_size(batch_size).limit(limit)
    
    while await cursor.fetch_next:
        batch = [cursor.next_object() for _ in range(batch_size) if cursor.alive]
        await asyncio.gather(process_batch(batch))

# Run the processing
if __name__ == "__main__":
    asyncio.run(process_documents(batch_size=100))