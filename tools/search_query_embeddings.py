

from bedrock_titan_embeddings import BedrockTitanEmbeddings

# Initialize Titan embedding model
titan_embeddings = BedrockTitanEmbeddings()


# Generate embeddings from query string
query = "Explain gfs scalability"
query_vector = titan_embeddings.embed_query(query)



from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

# Connect to Qdrant
client = QdrantClient("localhost:6333")  # Use "localhost" if running Qdrant locally

# Search in Qdrant
search_results = client.search(
    collection_name="pdf_embeddings",
    query_vector=query_vector,
    limit=3
)

# Display matched results
for result in search_results:
    print("\n🔎 Relevant Text:")
    print(result.payload["text"])
