# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# infrastructureからを渡すためにのAdapterを定義

# ① DTO → Payload の変換を呼び出す
# ② Client に通信を依頼する
# ③ 外部の結果を DTO に戻す

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import

# Domain
from src.domain.ports.text_generator_port import TextGeneratorPort
from domain.values.reply_content import MsgContent

# infrastructure
from .client import OpenAIClient

# ----------------------------------------------------------------------------------
# **********************************************************************************


class ChatGPTTextGeneratorAdapter(TextGeneratorPort):
    def __init__(self, client: OpenAIClient):
        self.client = client

    def generate(self, msg: MsgContent) -> str:
        # ① DTO → Payload の変換を呼び出す
        prompt = msg.value

        # ② Client に通信を依頼する
        response = self.client.generate_text(prompt=prompt)

        # ③ 外部の結果を DTO に戻す
        return MsgContent(value=response)

# **********************************************************************************
