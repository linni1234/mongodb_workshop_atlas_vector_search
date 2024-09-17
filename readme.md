# Movie Embedding and Query System

This project provides a system for embedding movie documents using **Azure OpenAI** and querying them using **MongoDB Atlas Vector Search**. The system processes movie documents, generates embeddings, and stores them in a MongoDB collection. It also supports querying the embedded documents using MongoDB Atlas Vector Search.

## Project Structure

```bash
.
├── create_index.py                  # Script to create a vector search index in MongoDB Atlas
├── embedd_documents_azure.py        # Script to process and embed movie documents using Azure OpenAI
├── embedd_documents_gcp.py          # Script to process and embed movie documents using Google Cloud Platform
├── query_with_langchain_azure.py    # Script to query embedded documents using LangChain with Azure
├── query_with_langchain_gcp.py      # Script to query embedded documents using LangChain with GCP
├── query.txt                        # Contains sample query vectors
├── requirements.txt                 # Lists Python dependencies for the project
├── restore.sh                       # Shell script to restore MongoDB dumps
└── README.md                        # README file for the project
```

## Setup

### 1. Clone the repository

```sh
git clone <repository-url>
cd <repository-directory>
```

### 2. Install dependencies

Make sure you have Python installed, then install the required dependencies:

```sh
pip3 install -r requirements.txt
```

### 3. Set environment variables

Create a `.env` file in the root directory and add the following variables:

```sh
export MONGODB_URI="<your-mongodb-uri>"
export first_last="<your-first-last>"

#For Azure OpanAI:
export AZURE_OPENAI_API_KEY="<your-azure-openai-api-key>"
export AZURE_OPENAI_ENDPOINT="<your-azure-openai-endpoint>"

#For GCP VertexAI:
export GCP_PROJECT="your_project_name"
export GCP_LOCATION="your_location_name"
```

## Usage

### 1. Restore MongoDB Dumps (Run `restore.sh` first)

Before embedding documents or querying the system, **run the restore script** to restore the MongoDB dumps. Make sure to set the environment variables mentioned above.

```sh
./restore.sh
```

This script will restore the movie data either with or without vector embeddings into MongoDB, depending on the configured path.

### 2. Embedding Documents

After restoring the data, you can embed movie documents and store the embeddings in MongoDB by running:

```sh
#For Azure OpenAI:
python3 embedd_documents_azure.py

#For GCP VertexAI:
python3 embedd_documents_gcp.py
```

This script processes documents, generates embeddings using **Azure OpenAI**, and updates the MongoDB collection with the embeddings.

### 3. Creating Vector Search Index

To create a vector search index in MongoDB Atlas, run:

```sh
python3 create_index.py
```

This script initializes the **MongoDB Atlas Vector Search** and creates an index with specified dimensions and filters.

### 4. Querying with LangChain

To query the embedded documents using **LangChain**, run:

```sh
#For Azure OpenAI:
python3 query_with_langchain_azure.py

#For GCP VertexAI:
python3 query_with_langchain_gcp.py
```

This script performs vector search queries on the embedded documents stored in MongoDB.

## Files Overview

- **create_index.py**: Script to create a vector search index in MongoDB Atlas.
- **embedd_documents.py**: Script to process and embed movie documents using Azure OpenAI.
- **query_with_langchain.py**: Script to query embedded documents using LangChain.
- **query.txt**: Contains sample query vectors.
- **requirements.txt**: Lists the Python dependencies for the project.
- **restore.sh**: Shell script to restore MongoDB dumps.

## Dependencies

The project requires the following Python libraries:

motor
aiohttp
langchain
langchain_mongodb
langchain_openai
langchain-google-vertexai
pymongo
openai

Install them by running:

```sh
pip3 install -r requirements.txt
```

## License

This project is licensed under the MIT License.