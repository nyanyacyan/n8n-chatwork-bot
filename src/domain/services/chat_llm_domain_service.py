# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 仕様：

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from src.domain.entities.chat.outgoing_message import OutgoingMessage
from src.domain.entities.llm.prompt import Prompt
from src.domain.entities.llm.response import Response
from src.domain.values.prompt_content import PromptContent

# ----------------------------------------------------------------------------------
# **********************************************************************************

class ChatLlmDomainService:

# ----------------------------------------------------------------------------------


    @staticmethod
    def create_prompt(content: OutgoingMessage) -> Prompt:
        return Prompt(PromptContent(content))

# ----------------------------------------------------------------------------------


    @staticmethod
    def can_reply(response: Response) -> bool:
        return response.length() > 0

# **********************************************************************************