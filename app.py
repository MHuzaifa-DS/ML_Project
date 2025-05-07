# import os
# import streamlit as st
# from dotenv import load_dotenv

# from langchain_community.document_loaders import PyPDFLoader, TextLoader
# from langchain.text_splitter import CharacterTextSplitter
# from langchain_community.vectorstores import FAISS
# from langchain_openai import OpenAIEmbeddings, ChatOpenAI
# from langchain.chains.question_answering import load_qa_chain

# # Load environment variables
# load_dotenv()
# openai_api_key = os.getenv("OPENAI_API_KEY")

# st.set_page_config(page_title="Document Q&A", layout="wide")
# st.title("📄 Ask Questions From Your Documents")

# # File uploader
# uploaded_file = st.file_uploader("Upload a PDF or TXT file", type=["pdf", "txt"])

# if uploaded_file:
#     st.success("✅ File uploaded successfully.")

#     # Save the uploaded file
#     file_path = f"temp_docs/{uploaded_file.name}"
#     os.makedirs("temp_docs", exist_ok=True)
#     with open(file_path, "wb") as f:
#         f.write(uploaded_file.getvalue())

#     # Load the document
#     if uploaded_file.name.endswith(".pdf"):
#         loader = PyPDFLoader(file_path)
#     else:
#         loader = TextLoader(file_path)

#     documents = loader.load()

#     # Split text
#     text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
#     split_docs = text_splitter.split_documents(documents)

#     # Embeddings
#     embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

#     # Use FAISS instead of Chroma
#     vectordb = FAISS.from_documents(split_docs, embeddings)

#     # User query
#     query = st.text_input("Ask something about your document:")

#     if query:
#         docs = vectordb.similarity_search(query)
#         llm = ChatOpenAI(openai_api_key=openai_api_key)
#         chain = load_qa_chain(llm, chain_type="stuff")
#         response = chain.run(input_documents=docs, question=query)

#         st.subheader("Answer:")
#         st.write(response)


# import os
# import streamlit as st
# from dotenv import load_dotenv

# from langchain_community.document_loaders import PyPDFLoader, TextLoader
# from langchain.text_splitter import CharacterTextSplitter
# from langchain_community.vectorstores import FAISS
# from langchain_openai import OpenAIEmbeddings, ChatOpenAI
# from langchain.chains.question_answering import load_qa_chain

# # Load environment variables
# load_dotenv()
# openai_api_key = os.getenv("OPENAI_API_KEY")

# # Set page config and title
# st.set_page_config(page_title="Document Q&A Chat", layout="wide")

# # Custom CSS for dark theme and chat UI
# st.markdown("""
#     <style>
#         body {
#             background-color: #1e1e1e;
#             color: #f0f0f0;
#         }
#         .stChat {
#             background-color: #2c2c2c;
#             border-radius: 12px;
#             padding: 20px;
#             max-width: 900px;
#             margin-left: auto;
#             margin-right: auto;
#         }
#         .user-message {
#             background-color: #4d90fe;
#             color: white;
#             border-radius: 12px;
#             padding: 10px;
#             margin: 10px 0;
#             max-width: 75%;
#             margin-left: auto;
#         }
#         .assistant-message {
#             background-color: #444444;
#             color: white;
#             border-radius: 12px;
#             padding: 10px;
#             margin: 10px 0;
#             max-width: 75%;
#             margin-right: auto;
#         }
#         .stTextInput {
#             background-color: #333333;
#             color: white;
#             border-radius: 12px;
#             padding: 10px;
#         }
#     </style>
# """, unsafe_allow_html=True)

# # Set title
# st.title("📄 Ask Questions From Your Documents")

# # Sidebar for file upload
# st.sidebar.title("Upload Document")
# uploaded_file = st.sidebar.file_uploader("Upload a PDF or TXT file", type=["pdf", "txt"])

# # Session state to manage conversation history
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# # Function to load document and process it
# def load_document(uploaded_file):
#     file_path = f"temp_docs/{uploaded_file.name}"
#     os.makedirs("temp_docs", exist_ok=True)
#     with open(file_path, "wb") as f:
#         f.write(uploaded_file.getvalue())

#     if uploaded_file.name.endswith(".pdf"):
#         loader = PyPDFLoader(file_path)
#     else:
#         loader = TextLoader(file_path)

#     return loader.load()

# # If a document is uploaded
# if uploaded_file:
#     st.sidebar.success("✅ File uploaded successfully!")

#     # Load the document
#     documents = load_document(uploaded_file)

#     # Split the document into chunks
#     text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
#     split_docs = text_splitter.split_documents(documents)

#     # Create embeddings for the document chunks
#     embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

#     # Use FAISS to create vector store
#     vectordb = FAISS.from_documents(split_docs, embeddings)

# # Function to get answer from the LLM
# def get_answer(query):
#     docs = vectordb.similarity_search(query)
#     llm = ChatOpenAI(openai_api_key=openai_api_key, model="gpt-4")
#     chain = load_qa_chain(llm, chain_type="stuff")
#     return chain.run(input_documents=docs, question=query)

# # Chat interface
# user_input = st.text_input("Ask something about your document:", key="input", label_visibility="collapsed")

# if user_input:
#     # Add the user's message to the session state
#     st.session_state.messages.append({"role": "user", "content": user_input})

#     # Get the response from the assistant
#     with st.spinner("Processing..."):
#         response = get_answer(user_input)

#     # Add the assistant's response to the session state
#     st.session_state.messages.append({"role": "assistant", "content": response})

# # Display chat history
# for message in st.session_state.messages:
#     if message["role"] == "user":
#         st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
#     else:
#         st.markdown(f'<div class="assistant-message">{message["content"]}</div>', unsafe_allow_html=True)
# import os
# import streamlit as st
# from dotenv import load_dotenv
# from langchain_community.document_loaders import PyPDFLoader, TextLoader
# from langchain.text_splitter import CharacterTextSplitter
# from langchain_community.vectorstores import FAISS
# from langchain_openai import OpenAIEmbeddings, ChatOpenAI
# from langchain.chains import RetrievalQA

# # Load API key
# load_dotenv()
# openai_api_key = os.getenv("OPENAI_API_KEY")

# st.set_page_config(page_title="Chat with Documents", layout="wide")

# # Custom Dark UI like ChatGPT
# st.markdown("""
#     <style>
#     body {
#         background-color: #121212;
#         color: white;
#     }
#     .message {
#         border-radius: 12px;
#         padding: 12px;
#         margin: 10px 0;
#         max-width: 80%;
#     }
#     .user {
#         background-color: #4e8cff;
#         color: white;
#         margin-left: auto;
#         text-align: right;
#     }
#     .bot {
#         background-color: #2a2a2a;
#         color: white;
#         margin-right: auto;
#         text-align: left;
#     }
#     </style>
# """, unsafe_allow_html=True)

# st.title("📄 Chat with Your Documents")

# # Sidebar Upload
# st.sidebar.header("Upload Document")
# uploaded_file = st.sidebar.file_uploader("Upload PDF or TXT", type=["pdf", "txt"])

# # Initialize chat history
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []

# # Prepare Vector Store
# def prepare_vectorstore(file):
#     os.makedirs("temp_docs", exist_ok=True)
#     file_path = os.path.join("temp_docs", file.name)
#     with open(file_path, "wb") as f:
#         f.write(file.getvalue())

#     loader = PyPDFLoader(file_path) if file.name.endswith(".pdf") else TextLoader(file_path)
#     documents = loader.load()

#     splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
#     split_docs = splitter.split_documents(documents)

#     embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
#     vectorstore = FAISS.from_documents(split_docs, embeddings)
#     return vectorstore

# if uploaded_file:
#     st.sidebar.success("✅ File uploaded")
#     vectordb = prepare_vectorstore(uploaded_file)

#     retriever = vectordb.as_retriever(search_kwargs={"k": 3})
#     llm = ChatOpenAI(model="gpt-4", openai_api_key=openai_api_key)
#     qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=True)

#     # Chat input
#     user_query = st.chat_input("Ask a question from your document...")
#     if user_query:
#         st.session_state.chat_history.append({"role": "user", "content": user_query})

#         # Get answer
#         with st.spinner("Thinking..."):
#             result = qa_chain(user_query)

#             if not result["result"].strip():
#                 bot_response = "🤖 Sorry, I couldn't find anything related to that in the document."
#             else:
#                 bot_response = result["result"].strip()

#             st.session_state.chat_history.append({"role": "bot", "content": bot_response})

# # Display conversation
# for msg in st.session_state.chat_history:
#     css_class = "user" if msg["role"] == "user" else "bot"
#     st.markdown(f'<div class="message {css_class}">{msg["content"]}</div>', unsafe_allow_html=True)


import os
import streamlit as st
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA

# Load API Key
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="🎓 🏛️ Superior Admission Chatbot", layout="wide")

# 🌈 Enhanced UI Styling
st.markdown("""
    <style>
    body {
        background-color: #f5f5f5;
        font-family: 'Segoe UI', sans-serif;
        color: #000000;
    }
    .message {
        border-radius: 12px;
        padding: 14px 18px;
        margin: 12px 0;
        max-width: 80%;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    }
    .user {
        background-color: #d0e7ff;
        color: #000;
        margin-left: auto;
        text-align: right;
    }
    .bot {
        background-color: #ffffff;
        color: #000;
        margin-right: auto;
        text-align: left;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎓 🏛️ Superior Admission Chatbot")

# Sidebar Upload
st.sidebar.header("Upload Document")
uploaded_file = st.sidebar.file_uploader("Upload PDF or TXT", type=["pdf", "txt"])

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Prepare Vector Store
def prepare_vectorstore(file):
    os.makedirs("temp_docs", exist_ok=True)
    file_path = os.path.join("temp_docs", file.name)
    with open(file_path, "wb") as f:
        f.write(file.getvalue())

    loader = PyPDFLoader(file_path) if file.name.endswith(".pdf") else TextLoader(file_path)
    documents = loader.load()

    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
    split_docs = splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vectorstore = FAISS.from_documents(split_docs, embeddings)
    return vectorstore

if uploaded_file:
    st.sidebar.success("✅ File uploaded")
    vectordb = prepare_vectorstore(uploaded_file)

    retriever = vectordb.as_retriever(search_kwargs={"k": 3})
    llm = ChatOpenAI(model="gpt-4", openai_api_key=openai_api_key)
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=True)

    # Chat input
    user_query = st.chat_input("Ask a question from your document...")
    if user_query:
        st.session_state.chat_history.append({"role": "user", "content": user_query})

        with st.spinner("Thinking..."):
            result = qa_chain(user_query)

            if not result["result"].strip():
                bot_response = "🤖 Sorry, I couldn't find anything related to that in the document."
            else:
                bot_response = result["result"].strip()

            st.session_state.chat_history.append({"role": "bot", "content": bot_response})

# Display chat
for msg in st.session_state.chat_history:
    css_class = "user" if msg["role"] == "user" else "bot"
    avatar = "🧑‍💬" if msg["role"] == "user" else "🤖"
    st.markdown(f'<div class="message {css_class}"><strong>{avatar}</strong><br>{msg["content"]}</div>', unsafe_allow_html=True)
