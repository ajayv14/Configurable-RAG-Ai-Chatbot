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


############
############

#Generate  embeddings

from bedrock_titan_embeddings import BedrockTitanEmbeddings

# Initialize Titan embedding model
titan_embeddings = BedrockTitanEmbeddings()

# Generate embeddings for document chunks
embeddings = titan_embeddings.embed_documents([doc.page_content for doc in docs])

##########
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