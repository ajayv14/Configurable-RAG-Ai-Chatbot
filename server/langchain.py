from langchain.llms import Bedrock
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import uuid
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Distance, VectorParams, Filter, FieldCondition, MatchValue
import numpy as np
import os

# Configurations
AWS_MODEL_ID = os.getenv("AWS_MODEL_ID", "amazon.titan-text-v1")
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "chat_responses")
VECTOR_SIZE = int(os.getenv("VECTOR_SIZE", 768))
SESSION_ID = os.getenv("SESSION_ID", str(uuid.uuid4()))  # Allow session ID to be configurable

# Initialize Amazon Bedrock LLM (Titan model)
llm = Bedrock(model_id=AWS_MODEL_ID)

# Initialize memory for session tracking
memory = ConversationBufferMemory(memory_key="chat_history")

# Connect to Qdrant (local or cloud instance)
qdrant_client = QdrantClient(QDRANT_URL)

# Ensure collection exists
if COLLECTION_NAME not in [col.name for col in qdrant_client.get_collections().collections]:
    qdrant_client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE)  # Adjust vector size based on embedding model
    )

def save_response(session_id, prompt, response):
    """Save chat response to Qdrant."""
    vector = np.random.rand(VECTOR_SIZE).tolist()  # Replace with actual embeddings
    point = PointStruct(id=int(uuid.uuid4().int % 1e6), vector=vector, payload={
        "session_id": session_id,
        "prompt": prompt,
        "response": response
    })
    qdrant_client.upsert(collection_name=COLLECTION_NAME, points=[point])

def get_session_responses(session_id):
    """Retrieve chat history for the given session ID."""
    search_filter = Filter(must=[
        FieldCondition(key="session_id", match=MatchValue(value=session_id))
    ])
    results = qdrant_client.scroll(collection_name=COLLECTION_NAME, scroll_filter=search_filter, limit=100)
    return [(hit.payload["prompt"], hit.payload["response"]) for hit in results[0]]

# Define prompt template
prompt_template = PromptTemplate(
    input_variables=["question"],
    template="{question}"
)

# Create chain
chain = LLMChain(llm=llm, prompt=prompt_template, memory=memory)

def chat(question):
    """Chat with Titan model and store responses."""
    response = chain.run(question)
    save_response(SESSION_ID, question, response)
    return response

# Example usage
if __name__ == "__main__":
    print(f"Using session ID: {SESSION_ID}")
    user_input = "Tell me about LangChain."
    print("User:", user_input)
    bot_response = chat(user_input)
    print("Bot:", bot_response)
    
    print("\nChat history:")
    history = get_session_responses(SESSION_ID)
    for prompt, response in history:
        print(f"Q: {prompt}\nA: {response}\n")
