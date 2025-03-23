import os
from qdrant_client import QdrantClient
from langchain.vectorstores import Qdrant
from langchain.embeddings import BedrockEmbeddings

# Constants
QDRANT_URL = "localhost"
QDRANT_PORT = 6333
COLLECTION_NAME = "pdf_embeddings"
REGION = "us-east-1"  # AWS region
MODEL_ID = "amazon.titan-embed-text-v1"

# Initialize the Qdrant client
qdrant_client = QdrantClient(QDRANT_URL, port=QDRANT_PORT)

# Setup LangChain embedding model (AWS Titan)
embeddings = BedrockEmbeddings(model_id=MODEL_ID, region_name=REGION)

# Create the Qdrant vector store, but this time we explicitly set `embedding_function` to generate embeddings
vector_store = Qdrant(
    client=qdrant_client,
    collection_name=COLLECTION_NAME,
    embeddings=embeddings  # Use embed_query to generate query embeddings
)

# Define a function to query the vector database and get responses
def query_vector_db(query: str, top_k: int = 3):
    """Queries the Qdrant vector database and gets the most relevant documents based on the query."""
    
    # Perform a similarity search (embeddings will be generated internally)
    search_results = vector_store.similarity_search(query, k=top_k)
    
    return search_results

# Main function to query and get the response
if __name__ == "__main__":
    query = input("Enter your query: ")  # Prompt the user for input query
    search_results = query_vector_db(query)
    
   
     # Print the relevant documents with headings and spacing
    print("\n## Relevant Documents:")
    for i, result in enumerate(search_results, start=1):
        print(f"\n### Document {i}")
        print("#### Metadata")
        for key, value in result.metadata.items():
            print(f"{key}: {value}")
        print("\n#### Page Content")
        print(result.page_content)