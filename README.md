# Configurable Chatbot AI

An easily customizable AI chatbot.

## Requirements

- Model access: `amazon.titan-embed-text-v1` for embeddings generation  
- Model foundation: `amazon.titan-embed-text-v1`  

## Getting Started

### Step 0: Create Environment

1. [Install Anaconda Platform](https://www.anaconda.com/download)  
2. Import environment YAML: `python_3_11_11_langchain_env.yaml`  

### Step 1: Setup Local DB and Optional PDF Data  

1. **Prerequisites:** Docker engine  
2. **Setup Qdrant Vector DB:**  
   ```sh
   cd /docker/qdrant
   docker-compose up -d
   ```
   Access Qdrant UI: [http://localhost:6333/dashboard](http://localhost:6333/dashboard)  

3. **Optional: PDF to Vector DB Embeddings Generator:**  
   - Directory: `/tools`  
   - Run:  
     ```sh
     python pdf_embeddings_generator.py
     ```
   - Default configs:  
     ```yaml
     db_url: "localhost:6333"
     db_collection_name: "pdf_embeddings"
     ```

### Step 2: Run Application Components  

1. **Server:** Flask server that calls the underlying Langchain module  
   ```sh
   python server/flask_server.py
   ```
2. **UI:** React and Node.js-based simple chat window  
3. **Langchain Module:** In progress  

## Additional Features  

### Search/Query Vector DB  

Run `search_query_embeddings.py` and provide search queries inside the file.  
