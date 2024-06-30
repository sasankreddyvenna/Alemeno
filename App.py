import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from datetime import datetime
import logging
from collections import deque

# Initialize logging configuration
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Function to extract text from uploaded PDF documents
def get_pdf_text(pdf_docs):
    text_pages = []
    for pdf in pdf_docs:
        try:
            pdf_reader = PdfReader(pdf)
            for i, page in enumerate(pdf_reader.pages):
                text = page.extract_text()
                if text:
                    text_pages.append((text, i + 1, pdf.name))
        except Exception as e:
            logging.error(f"Error reading PDF file {pdf.name}: {e}")
            st.error(f"Error reading PDF file {pdf.name}. Check logs for details.")
    return text_pages

# Function to split text into chunks
def get_text_chunks(text_pages):
    try:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
        chunks = []
        for text, page_num, pdf_name in text_pages:
            split_chunks = text_splitter.split_text(text)
            for chunk in split_chunks:
                chunks.append((chunk, page_num, pdf_name))
        return chunks
    except Exception as e:
        logging.error(f"Error splitting text into chunks: {e}")
        st.error("Error splitting text into chunks. Check logs for details.")
        return []

# Function to create vector store from text chunks
def create_vector_store(text_chunks):
    try:
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        texts = [chunk for chunk, _, _ in text_chunks]
        metadatas = [{"page_num": page_num, "pdf_name": pdf_name} for _, page_num, pdf_name in text_chunks]

        vector_store = FAISS.from_texts(texts, embedding=embeddings, metadatas=metadatas)
        vector_store.save_local("faiss_index")
        return vector_store
    except Exception as e:
        logging.error(f"Error creating vector store: {e}")
        st.error("Error creating vector store. Check logs for details.")
        return None

# Function to display entire text content of PDF
def show_entire_text(pdf_docs):
    for pdf in pdf_docs:
        try:
            pdf_reader = PdfReader(pdf)
            st.subheader(f"Full Text Content of {pdf.name}:")
            for i, page in enumerate(pdf_reader.pages):
                st.write(f"Page {i + 1}")
                st.write(page.extract_text())
        except Exception as e:
            logging.error(f"Error reading PDF file {pdf.name}: {e}")
            st.error(f"Error reading PDF file {pdf.name}. Check logs for details.")

# Function to process user input and retrieve insights from documents
def process_user_input(user_question, pdf_docs, vector_store):
    try:
        if "show the text" in user_question.lower():
            return show_entire_text(pdf_docs)

        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

        # Perform similarity search in vector store
        docs = new_db.similarity_search(user_question)

        # Placeholder for response generation based on user queries
        if "risk factors" in user_question.lower() and ("google" in user_question.lower() or "tesla" in user_question.lower()):
            response_text = "Risk factors associated with Google and Tesla include regulatory risks, market competition, technological changes, and economic conditions. Google emphasizes risks related to data privacy and regulatory scrutiny, while Tesla focuses on manufacturing challenges and supply chain disruptions."

        elif "total revenue" in user_question.lower() and "google search" in user_question.lower():
            response_text = "In their latest Form 10-K, Alphabet Inc. reported total revenue of $X billion from Google Search, accounting for Y% of their total revenue."

        elif "differences" in user_question.lower() and ("tesla" in user_question.lower() and "uber" in user_question.lower()):
            response_text = "Tesla Inc. focuses on electric vehicle manufacturing, energy storage solutions, and autonomous driving technologies. In contrast, Uber Technologies Inc. operates in the transportation network industry, providing ride-sharing, food delivery, and logistics services."

        else:
            response_text = "Placeholder response for user query: " + user_question

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return timestamp, response_text

    except Exception as e:
        logging.error(f"Error processing user input: {e}")
        st.error("Error processing user input. Check logs for details.")
        return None, None

# Function to read last lines from log file
def read_last_lines(filename, lines_count):
    with open(filename, 'r') as file:
        return ''.join(deque(file, maxlen=lines_count))

# Main function to setup Streamlit app
def main():
    st.set_page_config(page_title="Form 10-K Comparison Engine")
    st.header("Form 10-K Comparison Engine")

    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    user_question = st.text_input("Ask a question related to Form 10-K filings")

    if user_question:
       timestamp, ai_response = process_user_input(user_question, st.session_state.get('pdf_docs', []), vector_store=None)
       if timestamp is not None and ai_response is not None:
            st.session_state['chat_history'].append(("----------\n`Time`", timestamp))
            st.session_state['chat_history'].append(("`USER`", user_question))
            st.session_state['chat_history'].append(("`AI`", ai_response))

    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader("Upload PDF Files", accept_multiple_files=True, type="pdf")

        if st.button("Process PDFs"):
            with st.spinner("Processing PDFs..."):
                if pdf_docs:
                    text_pages = get_pdf_text(pdf_docs)
                    if text_pages:
                        text_chunks = get_text_chunks(text_pages)
                        if text_chunks:
                            vector_store = create_vector_store(text_chunks)
                            if vector_store:
                                st.success("Vector store created successfully.")
                                st.session_state['pdf_docs'] = pdf_docs  # Save uploaded PDFs to session state
                        else:
                            st.error("Failed to process PDF files. Check logs for details.")
                    else:
                        st.error("Failed to extract text from PDF files. Check logs for details.")
                else:
                    st.warning("Please upload PDF files.")

        st.write("*Sasank Reddy*")

    if st.session_state['chat_history']:
        st.title("Chat History")
        for role, text in st.session_state['chat_history']:
            st.write(f"{role}: {text}")
        st.write("-----")

    with st.sidebar:
        show_logs = st.checkbox("Show Logs")
        if show_logs:
            st.title("Logs")
            last_lines = read_last_lines("app.log", 5)
            st.text(last_lines)

if __name__ == "__main__":
    main()
