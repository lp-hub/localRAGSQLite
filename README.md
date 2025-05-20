# localRAGSQLite

## Free, local, open-source RAG with SQLite, LLaMA-3-8B GGUF & FAISS

Created & tested with Python 3.12, llama-cpp-python, LangChain, FAISS, and Gradio. Works entirely offline on Ubuntu-based system with NVIDIA GPU (for CUDA acceleration) and GGUF model (e.g. LLaMA-3-8B-Uncensored.Q8_0.gguf).

#### Set up:

1. Download or clone this repository.

git clone https://github.com/lp-hub/localRAGSQLite.git && cd localRAGSQLite

2. Install GCC / build tools

sudo apt update
sudo apt install python3 python3.12-venv build-essential cmake

https://visualstudio.microsoft.com/visual-cpp-build-tools/ for Windows, whatever...

3. Create and activate virtual environment

cd /../localRAG && python3.12 -m venv venv # to create venv dir

source venv/bin/activate # (venv) USER@PC:/../localRAG$

deactivate # after usig RAG

4. Install Python dependencies

pip install --upgrade pip

pip install gradio langchain pypdf tiktoken faiss-cpu sentence-transformers sqlite-utils

5. Install llama-cpp-python with CUDA support

pip uninstall -y llama-cpp-python
CMAKE_ARGS="-DGGML_CUDA=on" FORCE_CMAKE=1 pip install --no-cache-dir --force-reinstall llama-cpp-python

6. Download the GGUF model

mkdir -p models && wget https://huggingface.co/mradermacher/LLama-3-8b-Uncensored-GGUF/resolve/main/LLama-3-8b-Uncensored.Q8_0.gguf -O models/Llama-3-8B-Uncensored.Q8_0.gguf

7. Add your documents

Place .pdf, .txt, .md, .epub, etc., into your data/ folder.
Supported file types are automatically handled by the loader.

8. Rename config.template.py to config.py and configure

DATA_DIR = '/directory_with_files'
DB_DIR = "/faiss_db/"
MODEL_PATH = "/AI_model.gguf"

#### Usage

1. Run the CLI interface

python3 main.py --rebuild-db # use --rebuild-db first time or to make new db from new files

First run will embed and index documents.
You'll get an interactive prompt (You:) for local Q&A with sources.
Type in your question and wait for the model response.

2. (Optional) Start the Gradio Web UI

python webui.py

You will see something like:
Web UI running at http://192.168.X.X:7860
Open the IP in your browser for a simple web-based interface.

#### Notes

Your computer may not be powerful enough to run some models.

#### Acknowledgements

localRAG reworked by ChatGPT4 and me.
