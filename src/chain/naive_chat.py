import time

from langchain_core.output_parsers import StrOutputParser

from src.model.lm.gpt_3dot5_turbo import gpt_3dot5_turbo
from src.prompt.default_prompt import default_prompt

chain = default_prompt | gpt_3dot5_turbo | StrOutputParser()


def naive_chat(query: str, stream: bool = False):
    prompt_template = {
        'memory': '',
        'query': query
    }
    if stream:
        return chain.stream(prompt_template)
    return chain.invoke(prompt_template)


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
