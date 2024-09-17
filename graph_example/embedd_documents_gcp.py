import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from langchain_google_vertexai.embeddings import VertexAIEmbeddings

# Get environment variables for configuration
first_last = os.getenv("first_last")
gcp_project = os.getenv("GCP_PROJECT")
gcp_location = os.getenv("GCP_LOCATION")

# Initialize Vertex AI Embeddings
embedding_model = VertexAIEmbeddings(
    model_name="textembedding-gecko@003",
    project=gcp_project,
    location=gcp_location
)

# MongoDB Initialization
client = AsyncIOMotorClient(os.getenv("MONGODB_URI"))
db = client[first_last]
collection = db[f"routes_{first_last}"]

# Function to generate embeddings using LangChain's Vertex AI
async def generate_text_embedding(text):
    return embedding_model.embed_query(text)

# Process a single document to generate its embeddings and update MongoDB
async def process_document(doc):
    combined_text = f"Flight from {doc.get('src_airport', '')} to {doc.get('dst_airport', '')} with {doc['airline']['name']}"
    print(f"Generating embeddings for {combined_text}")
    
    # Generate embeddings
    doc_vector = await generate_text_embedding(combined_text)
    
    if doc_vector:
        await collection.update_one(
            {"_id": doc["_id"]}, {"$set": {"embedding": doc_vector}}
        )
        print(f"Document {doc['_id']} updated.")

# Process multiple documents
async def process_documents(batch_size=500):
    cursor = collection.find({"embedding": {"$exists": False}}).batch_size(batch_size)
    
    async for doc in cursor:
        await process_document(doc)

# Run the processing
if __name__ == "__main__":
    asyncio.run(process_documents())