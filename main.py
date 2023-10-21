import timeit
import argparse
from llm.wrapper import setup_rag_pipeline
import re


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('input',
                        type=str,
                        default='What is the invoice number value?',
                        help='Enter the query to pass into the LLM')
    args = parser.parse_args()

    start = timeit.default_timer()
    rag_pipeline = setup_rag_pipeline()

    json_response = rag_pipeline.run(query=args.input, params={"Retriever": {"top_k": 5}})

    answers = json_response['answers']
    answer = 'No answer found'
    for ans in answers:
        answer = ans.answer
        break

    end = timeit.default_timer()

    print(f'\nAnswer: {answer}')
    print('='*50)

    print(f"Time to retrieve answer: {end - start}")