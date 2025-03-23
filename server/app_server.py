from flask import Flask, request, jsonify
from flask_cors import CORS
from test_similarity_search_vector_db import query_vector_db  # Import query function

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes



@app.route('/similarity_search_query', methods=['POST'])
def query():
    data = request.json
    query_text = data.get("query", "")

    results = query_vector_db(query_text)

    # Convert LangChain Document objects to JSON-serializable format
    response_data = []
    for doc in results:
        response_data.append({
            "content": doc.page_content,  # Extract text content
            "metadata": doc.metadata      # Extract metadata (if needed)
        })

    return jsonify({"response": response_data})



@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        prompt = data.get("prompt", "")
        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400
        
        #response = llm(prompt)
        return jsonify({"response": "under progress"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500





if __name__ == '__main__':
    app.run(debug=True)
