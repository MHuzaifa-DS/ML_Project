
# from flask import Flask, render_template, request, jsonify
# from werkzeug.utils import secure_filename
# import os
# from dotenv import load_dotenv
# from langchain_community.document_loaders import PyPDFLoader, TextLoader
# from langchain.text_splitter import CharacterTextSplitter
# from langchain_community.vectorstores import FAISS
# from langchain_openai import OpenAIEmbeddings, ChatOpenAI
# from langchain.chains import RetrievalQA

# load_dotenv()
# openai_api_key = os.getenv("OPENAI_API_KEY")

# app = Flask(__name__)
# UPLOAD_FOLDER = "temp_docs"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# vectordb = None
# qa_chain = None

# def prepare_vectorstore(file_path):
#     loader = PyPDFLoader(file_path) if file_path.endswith(".pdf") else TextLoader(file_path)
#     documents = loader.load()

#     splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
#     split_docs = splitter.split_documents(documents)

#     embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
#     vectorstore = FAISS.from_documents(split_docs, embeddings)
#     return vectorstore

# @app.route("/")
# def index():
#     return render_template("index.html")


# @app.route("/upload", methods=["POST"])
# def upload_file():
#     global vectordb, qa_chain
#     file = request.files['file']
#     if not file:
#         return "No file uploaded", 400

#     filename = secure_filename(file.filename)
#     filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#     file.save(filepath)

#     vectordb = prepare_vectorstore(filepath)
#     retriever = vectordb.as_retriever(search_kwargs={"k": 3})
#     llm = ChatOpenAI(model="gpt-4", openai_api_key=openai_api_key)
#     qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=True)

#     return "File uploaded and processed", 200

# @app.route("/chat", methods=["POST"])
# def chat():
#     global qa_chain
#     data = request.get_json()
#     question = data.get("question", "")

#     if not question.strip():
#         return jsonify({"answer": "Please enter a valid question."})
#     if not qa_chain:
#         return jsonify({"answer": "Please upload a document first."})

#     result = qa_chain(question)
#     answer = result["result"].strip() or "Sorry, I couldn't find anything related to that."
#     return jsonify({"answer": answer})

# if __name__ == "__main__":
#     app.run(debug=True)


# from flask import Flask, render_template, request, jsonify, session
# from werkzeug.utils import secure_filename
# import os
# from dotenv import load_dotenv
# from langchain_community.document_loaders import PyPDFLoader, TextLoader
# from langchain.text_splitter import CharacterTextSplitter
# from langchain_community.vectorstores import FAISS
# from langchain_openai import OpenAIEmbeddings, ChatOpenAI
# from langchain.chains import RetrievalQA
# from uuid import uuid4

# load_dotenv()
# openai_api_key = os.getenv("OPENAI_API_KEY")

# app = Flask(__name__)
# app.secret_key = os.getenv("SECRET_KEY", str(uuid4()))  # Needed for session
# UPLOAD_FOLDER = "temp_docs"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# user_data = {}  # Store vector DB and chats per session


# def get_user_session():
#     if 'user_id' not in session:
#         session['user_id'] = str(uuid4())
#     return session['user_id']


# def prepare_vectorstore(file_path):
#     loader = PyPDFLoader(file_path) if file_path.endswith(".pdf") else TextLoader(file_path)
#     documents = loader.load()

#     splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
#     split_docs = splitter.split_documents(documents)

#     embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
#     vectorstore = FAISS.from_documents(split_docs, embeddings)
#     return vectorstore


# @app.route("/")
# def index():
#     return render_template("index.html")


# @app.route("/upload", methods=["POST"])
# def upload_file():
#     user_id = get_user_session()
#     file = request.files['file']
#     if not file:
#         return "No file uploaded", 400

#     filename = secure_filename(file.filename)
#     filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{user_id}_{filename}")
#     file.save(filepath)

#     vectorstore = prepare_vectorstore(filepath)

#     if user_id not in user_data:
#         user_data[user_id] = {'vectorstores': [], 'chat_history': []}
#     user_data[user_id]['vectorstores'].append(vectorstore)

#     return "File uploaded and processed", 200


# @app.route("/chat", methods=["POST"])
# def chat():
#     user_id = get_user_session()
#     data = request.get_json()
#     question = data.get("question", "").strip()

#     if not question:
#         return jsonify({"answer": "Please enter a valid question."})

#     if user_id not in user_data or not user_data[user_id]['vectorstores']:
#         return jsonify({"answer": "Please upload at least one document first."})

#     # Combine all vectorstores into a single retriever
#     all_docs = []
#     for vs in user_data[user_id]['vectorstores']:
#         all_docs.extend(vs.docstore._dict.values())

#     embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
#     merged_vectorstore = FAISS.from_documents(all_docs, embeddings)
#     retriever = merged_vectorstore.as_retriever(search_kwargs={"k": 3})
#     llm = ChatOpenAI(model="gpt-4", openai_api_key=openai_api_key)
#     qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=True)

#     result = qa_chain(question)
#     answer = result["result"].strip() or "Sorry, I couldn't find anything related to that."

#     # Save recent chat
#     user_data[user_id]['chat_history'].append({"question": question, "answer": answer})

#     return jsonify({"answer": answer})


# @app.route("/recent_chats", methods=["GET"])
# def recent_chats():
#     user_id = get_user_session()
#     chats = user_data.get(user_id, {}).get("chat_history", [])[-10:]  # last 10 chats
#     return jsonify({"chats": chats})


# if __name__ == "__main__":
#     app.run(debug=True)

# from flask import Flask, render_template, request, jsonify, session
# from werkzeug.utils import secure_filename
# import os
# from dotenv import load_dotenv
# from langchain_community.document_loaders import PyPDFLoader, TextLoader
# from langchain.text_splitter import CharacterTextSplitter
# from langchain_community.vectorstores import FAISS
# from langchain_openai import OpenAIEmbeddings, ChatOpenAI
# from langchain.chains import RetrievalQA
# from uuid import uuid4

# load_dotenv()
# openai_api_key = os.getenv("OPENAI_API_KEY")

# app = Flask(__name__)
# app.secret_key = os.getenv("SECRET_KEY", str(uuid4()))
# UPLOAD_FOLDER = "temp_docs"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# user_data = {}


# def get_user_session():
#     if 'user_id' not in session:
#         session['user_id'] = str(uuid4())
#     return session['user_id']


# def prepare_vectorstore(file_path):
#     loader = PyPDFLoader(file_path) if file_path.endswith(".pdf") else TextLoader(file_path)
#     documents = loader.load()
#     splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
#     split_docs = splitter.split_documents(documents)
#     embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
#     vectorstore = FAISS.from_documents(split_docs, embeddings)
#     return vectorstore


# @app.route("/")
# def index():
#     return render_template("index.html")


# @app.route("/upload", methods=["POST"])
# def upload_file():
#     user_id = get_user_session()
#     files = request.files.getlist("files")
#     if not files:
#         return "No files uploaded", 400

#     if user_id not in user_data:
#         user_data[user_id] = {'vectorstores': [], 'chat_history': []}

#     for file in files:
#         if not file:
#             continue
#         filename = secure_filename(file.filename)
#         filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{user_id}_{filename}")
#         file.save(filepath)
#         vectorstore = prepare_vectorstore(filepath)
#         user_data[user_id]['vectorstores'].append(vectorstore)

#     return "Files uploaded and processed", 200


# @app.route("/chat", methods=["POST"])
# def chat():
#     user_id = get_user_session()
#     data = request.get_json()
#     question = data.get("question", "").strip()

#     if not question:
#         return jsonify({"answer": "Please enter a valid question."})

#     if user_id not in user_data or not user_data[user_id]['vectorstores']:
#         return jsonify({"answer": "Please upload at least one document first."})

#     all_docs = []
#     for vs in user_data[user_id]['vectorstores']:
#         all_docs.extend(vs.docstore._dict.values())

#     embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
#     merged_vectorstore = FAISS.from_documents(all_docs, embeddings)
#     retriever = merged_vectorstore.as_retriever(search_kwargs={"k": 3})
#     llm = ChatOpenAI(model="gpt-4", openai_api_key=openai_api_key)
#     qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=True)

#     result = qa_chain(question)
#     answer = result["result"].strip() or "Sorry, I couldn't find anything related to that."

#     user_data[user_id]['chat_history'].append({"question": question, "answer": answer})

#     return jsonify({"answer": answer})


# @app.route("/recent_chats", methods=["GET"])
# def recent_chats():
#     user_id = get_user_session()
#     chats = user_data.get(user_id, {}).get("chat_history", [])[-10:]
#     return jsonify({"chats": chats})


# if __name__ == "__main__":
#     app.run(debug=True)




# from flask import Flask, request, jsonify, render_template
# from flask_cors import CORS
# import os

# app = Flask(__name__)
# CORS(app)

# UPLOAD_FOLDER = 'uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024  # 200MB

# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# messages = []

# @app.route('/')
# def index():
#     return render_template('index.html')  # load from templates folder

# @app.route('/chat', methods=['POST'])
# def chat():
#     data = request.get_json()
#     question = data.get('question', '')
#     if not question:
#         return jsonify({'answer': 'No question provided.'}), 400

#     messages.append({'sender': 'user', 'text': question})
#     answer = f"👨‍🎓 Bot: You asked - \"{question}\""
#     messages.append({'sender': 'bot', 'text': answer})
#     return jsonify({'answer': answer})

# @app.route('/messages', methods=['GET'])
# def get_messages():
#     return jsonify(messages)

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if 'file' not in request.files:
#         return "No file part", 400
#     file = request.files['file']
#     if file.filename == '':
#         return "No selected file", 400

#     filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
#     file.save(filepath)
#     return f"File '{file.filename}' uploaded successfully."

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

from langchain_community.chat_models import ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.question_answering import load_qa_chain

load_dotenv()

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = Flask(__name__, static_folder='static')
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

vector_store = None
messages = []

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_file(filepath):
    global vector_store
    loader = PyPDFLoader(filepath)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    vector_store = FAISS.from_documents(docs, embeddings)

@app.route('/')
def serve_ui():
    return send_from_directory('static', 'index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        try:
            process_file(filepath)
            return "File uploaded and processed successfully"
        except Exception as e:
            return f"Error processing file: {e}", 500
    return "Invalid file type", 400

@app.route('/chat', methods=['POST'])
def chat():
    global vector_store
    data = request.get_json()
    question = data.get("question", "")

    if not vector_store:
        return jsonify({"answer": "Please upload a document first."})

    try:
        docs = vector_store.similarity_search(question)
        llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=0)
        chain = load_qa_chain(llm, chain_type="stuff")
        answer = chain.run(input_documents=docs, question=question)
        messages.append({"sender": "user", "text": question})
        messages.append({"sender": "bot", "text": answer})
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"answer": f"Error: {e}"}), 500

@app.route('/messages', methods=['GET'])
def get_messages():
    return jsonify(messages)

if __name__ == '__main__':
    app.run(debug=True)
