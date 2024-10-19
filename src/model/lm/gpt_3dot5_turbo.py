from langchain_openai import ChatOpenAI

OPENAI_API_KEY = ''
MODEL_NAME = "gpt-3.5-turbo"
TOP_P = 0.7
TEMP = 0.7
STREAMING = True

gpt_3dot5_turbo = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    model=MODEL_NAME,
    top_p=TOP_P,
    temperature=TEMP,
    streaming=STREAMING
)
