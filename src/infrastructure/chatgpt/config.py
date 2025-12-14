# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 重要情報: ChatGPT設定情報
# BaseSettingsを継承して、環境変数や.envファイルから設定値を読み込む

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from pydantic_settings import BaseSettings
from .model_enum import ChatgptModel

# ----------------------------------------------------------------------------------
# **********************************************************************************


class ChatgptConfig(BaseSettings):
    chatgpt_api_token: str
    base_url: str = "https://api.chatwork.com/v2"
    model: ChatgptModel = ChatgptModel.standard


    class Config:
        # envファイルの中から検索する
        env_file = ".env.chatgpt"
        env_file_encoding = "utf-8"