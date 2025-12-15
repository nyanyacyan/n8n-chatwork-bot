# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 仕様：

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from domain.entities.chat.outgoing_message import Message
from domain.entities.llm.prompt import Prompt
from domain.entities.llm.response import Response
from domain.values.prompt_content import PromptContent


# ----------------------------------------------------------------------------------
# **********************************************************************************
# このチャットメッセージは LLM に投げてよいか？

class ChatLlmDomainService:

# ----------------------------------------------------------------------------------
# Message → Prompt への変換ルール

    @staticmethod
    def create_prompt(msg: Message) -> Prompt:
        content = PromptContent(msg.content.value)
        return Prompt(content=content)

# ----------------------------------------------------------------------------------
# この LLM Response は返信に使えるか？
    @staticmethod
    def can_reply(response: Response) -> bool:
        return response.length() > 0

# **********************************************************************************