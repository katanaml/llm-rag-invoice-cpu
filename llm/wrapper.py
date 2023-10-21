from haystack.document_stores import WeaviateDocumentStore
from haystack.nodes import (AnswerParser,
                            PromptTemplate,
                            EmbeddingRetriever,
                            PromptNode)
from llm.prompts import prompt_template
from llm.llm import setup_llm
from haystack import Pipeline

import box
import yaml


# Import config vars
with open('config.yml', 'r', encoding='utf8') as ymlfile:
    cfg = box.Box(yaml.safe_load(ymlfile))


def setup_prompt():
    return PromptTemplate(prompt=prompt_template,
                          output_parser=AnswerParser())


def setup_retriever(model, prompt, document_store):
    # max_length: The maximum number of tokens the generated text output can have.
    prompt_node = PromptNode(model_name_or_path=model,
                             max_length=cfg.PROMPT_ANSWER_MAX_LENGTH_TOKENS,
                             use_gpu=cfg.USE_GPU,
                             default_prompt_template=prompt)

    retriever = EmbeddingRetriever(
        document_store=document_store,
        embedding_model=cfg.EMBEDDINGS
    )

    return prompt_node, retriever


def setup_rag_pipeline():
    document_store = WeaviateDocumentStore(
        host=cfg.WEAVIATE_HOST,
        port=cfg.WEAVIATE_PORT,
        embedding_dim=cfg.WEAVIATE_EMBEDDING_DIM
    )

    prompt = setup_prompt()
    model = setup_llm()
    prompt_node, retriever = setup_retriever(model, prompt, document_store)

    rag_pipeline = Pipeline()
    rag_pipeline.add_node(component=retriever, name="Retriever", inputs=["Query"])
    rag_pipeline.add_node(component=prompt_node, name="PromptNode", inputs=["Retriever"])

    return rag_pipeline
