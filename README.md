# Chatbot Verba

## Overview

Welcome to Verba: The Golden RAGtriever, an open-source application designed to offer an end-to-end, streamlined, and user-friendly interface for Retrieval-Augmented Generation (RAG) out of the box. In just a few easy steps, explore your datasets and extract insights with ease, either locally with Ollama and Huggingface or through LLM providers such as Anthrophic, Cohere, and OpenAI.


## Setup
1. Clone the Repository
    ```bash
    git clone longdinh-theinfitech/chatbot-verba
    ```

2. Running the Application
    
    Navigate to the root directory of the project:
    ```bash
    cd chatbot-verba
    ```

    Build and start the application using Docker Compose:
    ```bash
    docker compose up --build
    ```

    This command will:

    - Build the Docker images for both the backend and frontend.
    - The database will be installed and stored in a Docker volume.

    Access the application:

    - Open your web browser and navigate to http://localhost:8000


