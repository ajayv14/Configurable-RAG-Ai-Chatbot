#pip install langchain pypdf openai qdrant-client
# pip install -U langchain-community


# Load PDF

from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("gfs-sosp2003.pdf")
documents = loader.load()


# Text splitter
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = text_splitter.split_documents(documents)


# Generate embeddings


#############
############

# Custom class for titan based embedding client 

import boto3
import json
from langchain.embeddings.base import Embeddings

class BedrockTitanEmbeddings(Embeddings):
    def __init__(self, model_id="amazon.titan-embed-text-v1", region_name="us-east-1"):
        self.client = boto3.client("bedrock-runtime", region_name=region_name)
        self.model_id = model_id

    def embed_query(self, text: str):
        """Generate an embedding for a single text query."""
        response = self.client.invoke_model(
            modelId=self.model_id,
            body=json.dumps({"inputText": text}),
        )
        response_body = json.loads(response["body"].read())
        return response_body["embedding"]

    def embed_documents(self, texts):
        """Generate embeddings for multiple documents."""
        return [self.embed_query(text) for text in texts]




#########
#########

#Generate  embeddings

# Initialize Titan embedding model
titan_embeddings = BedrockTitanEmbeddings()

# Generate embeddings for document chunks
embeddings = titan_embeddings.embed_documents([doc.page_content for doc in docs])

########
######


# Save embeddings to db

from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

# Connect to Qdrant
client = QdrantClient("localhost:6333")  # Use "localhost" if running Qdrant locally

# Create collection
client.create_collection(
    collection_name="pdf_embeddings",
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
)

# Insert embeddings into Qdrant
for i, (doc, emb) in enumerate(zip(docs, embeddings)):
    client.upsert(
        collection_name="pdf_embeddings",
        points=[{"id": i, "vector": emb, "payload": {"text": doc.page_content}}],
    )