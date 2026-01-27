# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 仕様：

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from src.domain.entities.chat.send_message import SendMessage
from src.application.llm.prompt_templates import REPLY_PROMPT_TEMPLATE
from src.domain.entities.llm.prompt import Prompt
from src.domain.values.prompt_content import PromptContent
from src.shared.logger import Logger

# ----------------------------------------------------------------------------------
# **********************************************************************************


class CreatePromptFromChatMessageUseCase:
    def __init__(self):

        # logger
        self.logger_setup = Logger()
        self.logger = self.logger_setup.getLogger()
        
# ----------------------------------------------------------------------------------


    def execute(self, msg: SendMessage) -> Prompt:
        self.logger.info("Prompt 作成処理を開始")

        new_msg = msg.content.value
        
        prompt_content = REPLY_PROMPT_TEMPLATE.format(message=new_msg)

        prompt = Prompt(content=PromptContent(prompt_content))

        self.logger.debug(f"作成されたPrompt: {prompt_content}")
        return prompt

# **********************************************************************************