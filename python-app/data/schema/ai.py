# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from typing import Union, List
from enum import Enum
from pydantic import BaseModel
from pydantic_settings import BaseSettings

# ----------------------------------------------------------------------------------
# **********************************************************************************
# モデル

class ChatgptModel(str, Enum):
    lowcost = "gpt-5-nano-2025-08-07"      # 安くて実用レベル
    standard = "gpt-5-mini-2025-08-07"          # ビジネス用途の最適解
    high_spec = "gpt-5.1-2025-11-13"       # 最高性能（高い）

# ----------------------------------------------------------------------------------
# リクエストの値

class ChatgptRequestValue(BaseModel):
    model : ChatgptModel = ChatgptModel.standard  # デフォルトモデル
    success_attribute : str = "choices"
    is_error: bool = False

    retry_prompt: str = "ただしくレスポンスが取得できませんでした。下記の再度回答をお願いします。"

    max_retries: int = 3  # 最大リトライ回数
    retry_delay: float = 1.0  # 初期リトライ遅延（秒）
    backoff_factor: float = 2.0  # バックオフ係数


# ----------------------------------------------------------------------------------
# レスポンスがあった際の値

class ChatgptResponseValue(BaseModel):
    chatwork_message: str
    is_error: bool = False

# ----------------------------------------------------------------------------------
# 重要情報

class ChatgptConfig(BaseSettings):
    chatgpt_api_token: str
    base_url: str = "https://api.chatwork.com/v2"

    class Config:
        # envファイルの中から検索する
        env_file = ".env.chatgpt"
        env_file_encoding = "utf-8"
    
#! 呼び出し方法
# chatgpt_config = ChatgptConfig()
# chatwork_config.chatwork_api_token

# **********************************************************************************


if __name__ == "__main__":
    pass

# ----------------------------------------------------------------------------------
