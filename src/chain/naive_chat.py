import time

from langchain_core.output_parsers import StrOutputParser

from src.model.lm.qwen_plus import qwen_plus


chain = qwen_plus | StrOutputParser()


def naive_chat(query: str, stream: bool = False):
    if stream:
        return chain.stream(query)
    return chain.invoke(query)


def shell_run():
    while True:
        _query = input('> ')
        answer: str = ''
        response = naive_chat(query=_query, stream=True)
        for token in response:
            answer += token
            for char in token:
                time.sleep(0.06)
                print(char, end='', flush=True)
        print("\n", flush=True)


if __name__ == '__main__':
    shell_run()