import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from openai import AzureOpenAI
import aiohttp
import os

first_last = os.getenv("first_last")

azure = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-01",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    azure_deployment="text-embedding-ada-002",
)

# MongoDB Initialization
client = AsyncIOMotorClient(os.getenv("MONGODB_URI"))
db = client[first_last]
collection = db[f"movies_{first_last}"]


def generate_text_embedding(session, text):
    response = azure.embeddings.create(input=[text], model="text-embedding-ada-002")
    return response.data[0].embedding


async def process_document(doc):
    combined_text = (
        f"{doc.get('title', '')} {doc.get('plot', '')} {doc.get('genres', [])}"
    )
    async with aiohttp.ClientSession() as session:
        print(f"Generating embeddings for {combined_text}")

        doc_vector = generate_text_embedding(session, combined_text)
        if doc_vector:
            await collection.update_one(
                {"_id": doc["_id"]}, {"$set": {"azure_openai_vector": doc_vector}}
            )
            print(f"Document {doc['_id']} updated.")


async def process_documents(batch_size=500):
    cursor = collection.find({"azure_openai_vector": {"$exists": False}}).batch_size(
        batch_size
    )
    async for doc in cursor:
        await process_document(doc)


if __name__ == "__main__":
    asyncio.run(process_documents())
