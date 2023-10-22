# Invoice data processing with Llama2 13B LLM RAG on Local CPU


**Youtube**: <a href="https://www.youtube.com/watch?v=XuvdgCuydsM" target="_blank">Invoice Data Processing with Llama2 13B LLM RAG on Local CPU</a>

___

## Quickstart

### RAG runs on: LlamaCPP, Haystack, Weaviate

1. Download the Llama2 13B model, check models/model_download.txt for the download link.
2. Install Weaviate local DB with Docker

`docker compose up -d`
   
3. Install the requirements: 

`pip install -r requirements.txt`

4. Copy text PDF files to the `data` folder.
5. Run the script, to convert text to vector embeddings and save in Weaviate vector storage: 

`python ingest.py`

6. Run the script, to process data with Llama2 13B LLM RAG and return the answer: 

`python main.py "What is the invoice number value?"`
