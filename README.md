# Invoice data processing with Llama2 13B LLM RAG on Local CPU


**Youtube**: <a href="https://youtu.be/5Q4Q1Q4Q1Q4" target="_blank">Invoice Data Processing with Llama2 13B LLM RAG on Local CPU</a>

___

## Quickstart

### RAG runs on: LlamaCPP, Haystack, Weaviate

1. Download the Llama2 13B model, check models/model_download.txt for the download link.
2. Install the requirements: 

`pip install -r requirements.txt`

3. Copy text PDF files to the `data` folder.
4. Run the script, to convert text to vector embeddings and save in Weaviate vector storage: 

`python ingest.py`

5. Run the script, to process data with Llama2 13B LLL RAG and return the answer: 

`python main.py "retrieve invoice number value"`
