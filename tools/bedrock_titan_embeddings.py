

# Custom bedrock titan embeddings class 

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

