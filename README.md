# Configurable-Chatbot-Ai
An easliy customizable Ai chatbot.


server 
    flask server that calls underneath langchain module

UI - React and nodejs based simple chat window

Langchain Module

    - Need local sql db
    - access to titan text module on aws.



Setup : Use anaconda to setup this environment : python_3_11_11_langchain_env.yaml    




pdf to vector db embeddings :
    /tools

    Have local qdrant vector db running on docker
        
        cd /docker/qdrant
        run docker-compose up -d 