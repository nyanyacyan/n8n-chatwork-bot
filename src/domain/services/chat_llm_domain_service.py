# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 仕様：

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from src.domain.entities.chat.send_message import SendMessage
from src.domain.entities.llm.prompt import Prompt
from src.domain.entities.llm.response import Response
from src.domain.values.prompt_content import PromptContent

# ----------------------------------------------------------------------------------
# **********************************************************************************

class ChatLlmDomainService:

# ----------------------------------------------------------------------------------


    @staticmethod
    def create_prompt(content: SendMessage) -> Prompt:
        return Prompt(PromptContent(content.content.value))

# ----------------------------------------------------------------------------------


    @staticmethod
    def can_reply(response: Response) -> bool:
        return response.length() > 0

# **********************************************************************************
