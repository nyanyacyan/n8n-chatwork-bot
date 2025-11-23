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
# 通常プロンプト

class ChatgptStartPrompt(str, Enum):
    prompt_1: str = "あなたは優秀なアシスタントです。以下のユーザーからの質問に対して、簡潔かつ明確に答えてください。"
    prompt_2: str = "あなたは知識豊富なアシスタントです。以下のユーザーからの質問に対して、詳細かつ分かりやすく答えてください。"
    prompt_3: str = "あなたはクリエイティブなアシスタントです。以下のユーザーからの質問に対して、独創的かつ魅力的に答えてください。"

# ----------------------------------------------------------------------------------
# 制約プロンプト

class ChatgptPromisePrompt(str, Enum):
    promise_prompt_1: str = "回答は200文字以内にしてください。"
    promise_prompt_2: str = "専門用語を使わずに説明してください。"
    promise_prompt_3: str = "具体例を交えて説明してください。"

# ----------------------------------------------------------------------------------
# エラーがあった際のプロンプト

class ChatgptErrorPrompt(str, Enum):
    error_prompt_1: str = "申し訳ありませんが、現在システムに問題が発生しており、リクエストを処理できません。後ほど再度お試しください。"
    error_prompt_2: str = "ただいまサービスが一時的に利用できません。ご迷惑をおかけして申し訳ありませんが、しばらくしてからもう一度お試しください。"
    error_prompt_3: str = "システムエラーが発生しました。問題の解決に努めておりますので、少々お待ちいただいてから再度お試しください。"

# ----------------------------------------------------------------------------------
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
<<<<<<< HEAD
    retry_prompt: str = "ただしくレスポンスが取得できませんでした。下記の再度回答をお願いします。"
=======
    max_retries: int = 3  # 最大リトライ回数
    retry_delay: float = 1.0  # 初期リトライ遅延（秒）
    backoff_factor: float = 2.0  # バックオフ係数
>>>>>>> 0d1d1c8cbcb82a427f4d1dcb2983d3ee02908c49

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
        env_file = ".env"
        env_file_encoding = "utf-8"
    
#! 呼び出し方法
# chatgpt_config = ChatgptConfig()
# chatwork_config.chatwork_api_token

# **********************************************************************************


if __name__ == "__main__":
    pass

# ----------------------------------------------------------------------------------
