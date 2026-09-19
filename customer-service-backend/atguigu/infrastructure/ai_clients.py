from langchain.chat_models import init_chat_model

from atguigu.conf.config import settings

llm_client = init_chat_model(
    model=settings.llm_model,
    base_url=settings.llm_base_url,
    api_key=settings.llm_api_key,
    model_provider='openai',
    temperature=0
)