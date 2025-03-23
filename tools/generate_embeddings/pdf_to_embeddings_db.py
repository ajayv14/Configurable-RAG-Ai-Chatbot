import os
import json
from PyPDF2 import PdfReader
from langchain.embeddings import BedrockEmbeddings
from langchain.llms.bedrock import Bedrock
from langchain.vectorstores import FAISS
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct


#pip install boto3
#pip install PyPDF2
#pip install langchain-community
#pip install qdrant-client

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    reader = PdfReader(pdf_path)
    text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    return text

def get_aws_titan_embedding(text, model_id, region):
    """Generates embeddings using AWS Titan Embeddings model through LangChain."""
    embeddings = BedrockEmbeddings(model_id=model_id,region_name=region)
    return embeddings.embed_query(text)

def save_to_qdrant(file_name, embedding, qdrant_url, qdrant_port):
    """Saves embeddings to Qdrant database."""
    client = QdrantClient(qdrant_url, port=qdrant_port)
    collection_name = "pdf_embeddings"
    
    client.upsert(
        collection_name=collection_name,
        points=[PointStruct(id=hash(file_name), vector=embedding, payload={"file": file_name})]
    )

def process_pdfs(input_folder, output_folder, model_id, region, qdrant_url, qdrant_port):
    """Processes PDF files by extracting text, generating embeddings, and moving to output folder."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for file in os.listdir(input_folder):
        if file.endswith(".pdf"):
            pdf_path = os.path.join(input_folder, file)
            print(f"Processing {file}...")
            
            text = extract_text_from_pdf(pdf_path)
            embedding = get_aws_titan_embedding(text, model_id,region)
            
            # Save embedding to JSON file
            embedding_path = os.path.join(output_folder, file.replace(".pdf", ".json"))
            with open(embedding_path, "w") as f:
                json.dump({"file": file, "embedding": embedding}, f)
            
            # Save embedding to Qdrant
            save_to_qdrant(file, embedding, qdrant_url, qdrant_port)
            
            os.rename(pdf_path, os.path.join(output_folder, file))
            print(f"Processed {file} and moved to {output_folder}")

if __name__ == "__main__":
    INPUT_FOLDER = "pdf_input"
    OUTPUT_FOLDER = "pdf_dump"
    MODEL_ID = "amazon.titan-embed-text-v1"
    REGION = "us-east-1"
    QDRANT_URL = "localhost"
    QDRANT_PORT = 6333
    
    process_pdfs(INPUT_FOLDER, OUTPUT_FOLDER, MODEL_ID, REGION, QDRANT_URL, QDRANT_PORT)
