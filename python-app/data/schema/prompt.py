# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from typing import Union, List
from enum import Enum
from pydantic import BaseModel
from pydantic_settings import BaseSettings

from src.utils.logger import Logger


# ----------------------------------------------------------------------------------
# **********************************************************************************
# 通常プロンプト

class ChatgptStartPrompt(str, Enum):
    PROMPT_1: str = "あなたは優秀なアシスタントです。以下のユーザーからの質問に対して、簡潔かつ明確に答えてください。"
    PROMPT_2: str = "あなたは知識豊富なアシスタントです。以下のユーザーからの質問に対して、詳細かつ分かりやすく答えてください。"
    PROMPT_3: str = "あなたはクリエイティブなアシスタントです。以下のユーザーからの質問に対して、独創的かつ魅力的に答えてください。"

# ----------------------------------------------------------------------------------
# 制約プロンプト

class ChatgptPromisePrompt(str, Enum):
    PROMISE_PROMPT_1: str = "回答は200文字以内にしてください。"
    PROMISE_PROMPT_2: str = "専門用語を使わずに説明してください。"
    PROMISE_PROMPT_3: str = "具体例を交えて説明してください。"

# ----------------------------------------------------------------------------------
# エラーがあった際のプロンプト

class ChatgptEndPrompt(str, Enum):
    END_PROMPT_1: str = "必ず正確な情報を提供してください。"
    END_PROMPT_2: str = "必ず正確な情報を提供した上で、丁寧な言葉遣いを心がけてください。"
    END_PROMPT_3: str = "上記の情報を基に、正確かつ丁寧な回答を提供してください。"

# ----------------------------------------------------------------------------------

class ChatgptPromptConfig(BaseSettings):
    START_PROMPT: ChatgptStartPrompt = ChatgptStartPrompt.PROMPT_1
    PROMISE_PROMPT: ChatgptPromisePrompt = ChatgptPromisePrompt.PROMISE_PROMPT_1
    END_PROMPT: ChatgptEndPrompt = ChatgptEndPrompt.END_PROMPT_1
    

# **********************************************************************************

class PromptBuilder:
    def __init__(self):
        self.config = ChatgptPromptConfig()

    def start(self):
        return self.config.START_PROMPT.value

    def promise(self):
        return self.config.PROMISE_PROMPT.value

    def end(self):
        return self.config.END_PROMPT.value

# **********************************************************************************


class CallPrompt:
    def __init__(self):
        # logger
        self.getLogger = Logger()
        self.logger = self.getLogger.getLogger()
        
        self.config = ChatgptPromptConfig()
        

# ----------------------------------------------------------------------------------
    # リクエスト用プロンプト作成メソッド

    def build_request(self):
        self.logger.debug("プロンプトの作成開始")
        
        start_prompt = self.config.START_PROMPT.value
        promise_prompt = self.config.PROMISE_PROMPT.value
        
        all_prompt = f"{start_prompt}\n\n{promise_prompt}"
        
        self.logger.debug(f"作成したプロンプト: {all_prompt}")
        
        self.logger.debug("プロンプトの作成終了")
        return all_prompt