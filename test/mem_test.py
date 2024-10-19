import logging

from src.chain.conversational_retrieval_chat import shell_run
from src.logger import logger

logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    shell_run(2, 1)
