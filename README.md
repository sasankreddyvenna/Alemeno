# Alemeno-Bot

## Overview

This project creates a robust Content Engine that analyzes and compares multiple PDF documents, specifically identifying and highlighting their differences. The system leverages Retrieval Augmented Generation (RAG) techniques to effectively retrieve, assess, and generate insights from the documents. Users interact with the system through a chatbot interface, querying information and comparing data across the documents.   

You can get text of the pdf by asking " show the text ".

**Note:** This chatbot is completely independent of any external APIs and works entirely locally, ensuring data privacy and security. This utilizes Ollama's llama3 model as a Local Language Model. 

## Key Components
- **Backend Framework: LangChain**
- **Frontend Framework: Streamlit**
- **Vector Store: FAISS**
- **Embedding Model: HuggingFace**
- **Local LLM: Ollama**

**Verify Installation**
Make sure U install all requirements given


## Usage

1. **Run the Application**

    ```bash
    streamlit run app.py
    ```

2. **Upload PDFs**

    - Use the Streamlit interface to upload multiple PDF files for analysis.



## Example Use Cases

- **Compare Risk Factors**: "What are the risk factors associated with Google and Tesla?"
- **Retrieve Financial Data**: "What is the total revenue for Google Search?"
- **Business Analysis**: "What are the differences in the business of Tesla and Uber?"

3. **Process PDFs**

    - The system extracts text, splits it into chunks, generates embeddings, and stores them in the FAISS vector store.

4. **Query the System**

    - Enter questions related to the content of the PDFs to retrieve relevant information and generate detailed responses.

5. **View Results**

    - Responses are displayed in the interface along with citations from the source documents.
    - Chat history and logs are accessible for review.
  
 ## Author
- V.V.S Sasank Reddy
- LinkedIn: www.linkedin.com/in/sasank-venna
  
