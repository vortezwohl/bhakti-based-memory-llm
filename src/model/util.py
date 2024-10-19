import re
import time

from bhakti.database import Metric
from bhakti.exception import BhaktiRemoteError
from numpy import ndarray, asarray

from src.model.embedding.m3e_small import m3e_small
from src.bhakti_client import bhakti_client
from src.logger import logger

DEFAULT_USER_ID = 'None'
DEFAULT_BOT_ID = 'None'


def text_encode(text: str) -> ndarray:
    return asarray(m3e_small.encode(text).tolist())


async def recall_memories(
        query: str,
        top_k: int,
        metric: Metric = Metric.DEFAULT_METRIC,
        user_id: str = DEFAULT_USER_ID,
        bot_id: str = DEFAULT_BOT_ID
) -> list[tuple]:
    query_vector = text_encode(query)
    try:
        return await bhakti_client.find_documents_by_vector_indexed(
            query=f'user_id == "{user_id}" && bot_id == "{bot_id}"',
            vector=query_vector,
            metric=metric,
            top_k=top_k
        )
    except BhaktiRemoteError:
        return []


async def recall_memories_templated(
        query: str,
        top_k: int,
        metric: Metric = Metric.DEFAULT_METRIC,
        user_id: str = DEFAULT_USER_ID,
        bot_id: str = DEFAULT_BOT_ID
) -> list[str]:
    memories = await recall_memories(
        query=query,
        top_k=top_k,
        metric=metric,
        user_id=user_id,
        bot_id=bot_id
    )
    logger.debug(f'Recalls: {len(memories)}')
    for i, memory in enumerate(memories):
        logger.debug(f'{i}: {memory}')
    template = list()
    for document, _ in memories:
        query = document['query']
        answer = document['answer']
        timestamp = document['timestamp']
        template.append(f'Query: "{query}" Answer: "{answer}" UnixTimestamp(seconds): {timestamp}')
    return template


async def memorize_conversation(
        query: str,
        answer: str,
        user_id: str = DEFAULT_USER_ID,
        bot_id: str = DEFAULT_BOT_ID,
        query_weight: int = 1,
        answer_weight: int = 1,
        cached: bool = False
) -> bool:
    answer = re.sub(pattern=r'\n+', repl='\n', string=answer)
    query_vector = text_encode(query)
    answer_vector = text_encode(answer)
    vector = query_weight * query_vector + answer_weight * answer_vector
    mem_data = {
        'query': query,
        'answer': answer,
        'user_id': user_id,
        'bot_id': bot_id,
        'timestamp': time.time()
    }
    inv_indices = list(mem_data.keys())
    await bhakti_client.remove_by_vector(vector)
    return await bhakti_client.create(
        vector=vector,
        document=mem_data,
        indices=inv_indices,
        cached=cached
    )

