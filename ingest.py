from haystack.nodes import EmbeddingRetriever, PreProcessor
from haystack.document_stores import WeaviateDocumentStore
from haystack.preview.components.file_converters.pypdf import PyPDFToDocument
import box
import yaml
import timeit
import os


# Import config vars
with open('config.yml', 'r', encoding='utf8') as ymlfile:
    cfg = box.Box(yaml.safe_load(ymlfile))


def run_ingest():
    file_list = [os.path.join(cfg.DATA_PATH, f) for f in os.listdir(cfg.DATA_PATH) if
                 os.path.isfile(os.path.join(cfg.DATA_PATH, f)) and not f.startswith('.')]

    start = timeit.default_timer()

    vector_store = WeaviateDocumentStore(host=cfg.WEAVIATE_HOST,
                                         port=cfg.WEAVIATE_PORT,
                                         embedding_dim=cfg.WEAVIATE_EMBEDDING_DIM)

    converter = PyPDFToDocument()
    output = converter.run(paths=file_list)
    docs = output["documents"]

    final_doc = []
    for doc in docs:
        new_doc = {
            'content': doc.text,
            'meta': doc.metadata
        }
        final_doc.append(new_doc)

    preprocessor = PreProcessor(
        clean_empty_lines=True,
        clean_whitespace=False,
        clean_header_footer=False,
        split_by="word",
        language="en",
        split_length=cfg.PRE_PROCESSOR_SPLIT_LENGTH,
        split_overlap=cfg.PRE_PROCESSOR_SPLIT_OVERLAP,
        split_respect_sentence_boundary=True,
    )

    preprocessed_docs = preprocessor.process(final_doc)
    vector_store.write_documents(preprocessed_docs)

    retriever = EmbeddingRetriever(
        document_store=vector_store,
        embedding_model=cfg.EMBEDDINGS
    )
    vector_store.update_embeddings(retriever)

    end = timeit.default_timer()
    print(f"Time to prepare embeddings: {end - start}")


if __name__ == "__main__":
    run_ingest()