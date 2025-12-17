# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 仕様：

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from src.domain.entities.llm.prompt import Prompt
from src.domain.entities.llm.response import Response
from src.domain.ports.text_generator_port import TextGeneratorPort
from shared.logger import Logger


# ----------------------------------------------------------------------------------
# **********************************************************************************


class GenerateResponseFromPromptUseCase:
    def __init__(self, generator: TextGeneratorPort):
        self.generator = generator

        # logger
        self.logger_setup = Logger()
        self.logger = self.logger_setup.getLogger()
        
        
# ----------------------------------------------------------------------------------

    def execute(self, prompt: Prompt) -> Response:
        self.logger.info("LLM へのリクエストを開始")

        response = self.generator.execute(prompt)

        self.logger.info("LLM からのレスポンスを受信")
        self.logger.debug(f"Response: {response}")

        return response

# **********************************************************************************