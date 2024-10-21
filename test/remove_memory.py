from bhakti.util.async_run import sync

from src.bhakti_client.client import bhakti_client

@sync
async def remove_memory(query: str):
    return await bhakti_client.indexed_remove(f'query == %{query}%')


if __name__ == '__main__':
    print(remove_memory('What do you know about cars i love'))
