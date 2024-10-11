from langchain_community.llms.tongyi import Tongyi

TONGYI_API_KEY = "sk-89b79de3a1ae4b4fb26a7b023e06699f"
TOP_P = 0.7
TEMP = 0.7
QWEN_PLUS = "qwen-plus"
STREAMING = True

qwen_plus = Tongyi(
    dashscope_api_key=TONGYI_API_KEY,
    model=QWEN_PLUS,
    top_p=TOP_P,
    temperature=TEMP,
    streaming=STREAMING
)