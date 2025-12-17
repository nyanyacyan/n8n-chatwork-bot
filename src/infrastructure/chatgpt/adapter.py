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
from domain.entities.llm.response import Response
from src.domain.entities.llm.prompt import Prompt
from domain.values.response_content import ResponseContent

# infrastructure
from .client import OpenAIClient

# ----------------------------------------------------------------------------------
# **********************************************************************************


class ChatGPTTextGeneratorAdapter(TextGeneratorPort):
    def __init__(self, client: OpenAIClient):
        self.client = client

    def execute(self, prompt: Prompt) -> Response:
        prompt_text = prompt.content.value

        # APIの実施
        response_text = self.client.generate_text(prompt=prompt_text)

        # 値フィルター実施
        raw_response = ResponseContent(value=response_text)

        # 値のステータス取得
        # 値+ステータスも持たせている状態
        return Response(content=raw_response)

# **********************************************************************************
