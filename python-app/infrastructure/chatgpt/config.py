# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# リクエストする際のDTOを定義
#! ここではEnumは定義NG

#! 下記の定義以外は記述しない
# 例）
# class CreateMessageDTO(BaseModel):
#     text: str

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from pydantic_settings import BaseSettings

# ----------------------------------------------------------------------------------

from .model_enum import ChatgptModel


# ----------------------------------------------------------------------------------
# **********************************************************************************


class ChatgptConfig(BaseSettings):
    chatgpt_api_token: str
    base_url: str = "https://api.chatwork.com/v2"

    class Config:
        # envファイルの中から検索する
        env_file = ".env.chatgpt"
        env_file_encoding = "utf-8"