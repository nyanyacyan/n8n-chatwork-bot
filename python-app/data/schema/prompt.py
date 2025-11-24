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

class ChatgptPromptConfig(BaseSettings):
    start_prompt: ChatgptStartPrompt = ChatgptStartPrompt.prompt_2
    promise_prompt: ChatgptPromisePrompt = ChatgptPromisePrompt.promise_prompt_2
    error_prompt: ChatgptErrorPrompt = ChatgptErrorPrompt.error_prompt_1