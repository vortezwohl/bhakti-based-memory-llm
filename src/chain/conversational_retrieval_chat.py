import time

from langchain_core.output_parsers import StrOutputParser
from bhakti.database import Metric
from bhakti.util import sync

from src.prompt.default_prompt import default_prompt
from src.model.lm.gpt_3dot5_turbo import gpt_3dot5_turbo
from src.model.util import (
    memorize_conversation,
    recall_memories_templated,
    DEFAULT_BOT_ID,
    DEFAULT_USER_ID
)

chain = default_prompt | gpt_3dot5_turbo | StrOutputParser()


async def memo_chat(
        query: str,
        top_k: int,
        user_id: str = DEFAULT_USER_ID,
        bot_id: str = DEFAULT_BOT_ID,
        metric: Metric = Metric.DEFAULT_METRIC,
        stream: bool = False
):
    memories = await recall_memories_templated(
        query=query,
        top_k=top_k,
        metric=metric,
        user_id=user_id,
        bot_id=bot_id
    )
    prompt_template = {
        'memory': memories.__repr__(),
        'query': query
    }
    if stream:
        return chain.stream(prompt_template)
    return chain.invoke(prompt_template)


@sync
async def shell_run(query_weight: int, answer_weight: int):
    while True:
        _query = input('> ')
        answer: str = ''
        response = await memo_chat(
            query=_query,
            top_k=5,
            stream=True
        )
        for token in response:
            answer += token
            for char in token:
                time.sleep(0.06)
                print(char, end='', flush=True)
        print("\n", flush=True)
        # update memory
        await memorize_conversation(
            query=_query,
            answer=answer,
            cached=True,
            query_weight=query_weight,
            answer_weight=answer_weight
        )


if __name__ == '__main__':
    shell_run(2, 1)
