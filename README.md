<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Configurable Chatbot AI</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        h1 {
            color: #00698f;
        }
        h2 {
            margin-top: 40px;
        }
        ul {
            list-style: disc;
            margin-left: 20px;
        }
        li {
            margin-bottom: 10px;
        }
        a {
            text-decoration: none;
            color: #008000;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <h1>Configurable Chatbot AI</h1>
    <p>An easily customizable AI chatbot.</p>

    <h2>Requirements</h2>
    <ul>
        <li>Model access: amazon.titan-embed-text-v1 for embeddings generation</li>
        <li>Model foundation: amazon.titan-embed-text-v1</li>
    </ul>

    <h2>Getting Started</h2>

    <h3>Step 0: Create Environment</h3>
    <ol>
        <li><a href="https://www.anaconda.com/download">Install Anaconda Platform</a></li>
        <li>Import environment YAML: python_3_11_11_langchain_env.yaml</li>
    </ol>

    <h3>Step 1: Setup Local DB and Optional PDF Data</h3>
    <ol>
        <li>Prerequisites: Docker engine</li>
        <li>
            Setup Qdrant Vector DB:
            <ul>
                <li>cd /docker/qdrant</li>
                <li>docker-compose up -d</li>
                <li>Access Qdrant UI: <a href="http://localhost:6333/dashboard">http://localhost:6333/dashboard</a></li>
            </ul>
        </li>
        <li>
            Optional: PDF to Vector DB Embeddings Generator:
            <ul>
                <li>Directory: /tools</li>
                <li>Run: python pdf_embeddings_generator.py</li>
                <li>Default configs:
                    <ul>
                        <li>db_url: "localhost:6333"</li>
                        <li>db_collection_name: "pdf_embeddings"</li>
                    </ul>
                </li>
            </ul>
        </li>
    </ol>

    <h3>Step 2: Run Application Components</h3>
    <ol>
        <li>
            Server: Flask server that calls underneath Langchain module
            <ul>
                <li>Run: python server/flask_server.py</li>
            </ul>
        </li>
        <li>UI: React and Node.js-based simple chat window</li>
        <li>Langchain Module: In progress</li>
    </ol>

    <h2>Additional Features</h2>

    <h3>Search/Query Vector DB</h3>
    <p>search_query_embeddings.py: Provide search query inside the file</p>
</body>
</html>