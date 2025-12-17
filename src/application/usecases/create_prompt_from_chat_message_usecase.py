# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 仕様：

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from src.domain.entities.chat.outgoing_message import OutgoingMessage
from src.domain.entities.llm.prompt import Prompt
from src.domain.services.chat_llm_domain_service import ChatLlmDomainService
from shared.logger import Logger



# ----------------------------------------------------------------------------------
# **********************************************************************************


class CreatePromptFromChatMessageUseCase:
    def __init__(self):

        # logger
        self.logger_setup = Logger()
        self.logger = self.logger_setup.getLogger()
        
# ----------------------------------------------------------------------------------


    def execute(self, msg: OutgoingMessage) -> Prompt:
        self.logger.info("Prompt 作成処理を開始")

        prompt = ChatLlmDomainService.create_prompt(msg)

        self.logger.debug(f"作成されたPrompt: {prompt}")
        return prompt

# **********************************************************************************