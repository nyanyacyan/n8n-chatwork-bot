# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# infrastructureからを渡すためにのAdapterを定義

# ① DTO → Payload の変換を呼び出す
# ② Client に通信を依頼する
# ③ 外部の結果を DTO に戻す

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from enum import Enum
from pydantic import BaseModel
from pydantic_settings import BaseSettings

# infrastructure
from .payload import ChatGptPayload
from .response_dto import ChatgptResponseDTO
from data.domain.interfaces.chatgpt_client import ChatGPTClient

# ----------------------------------------------------------------------------------
# **********************************************************************************


class ChatgptAdapter:
    def __init__(self, client: ChatGPTClient):
        self.client = client

    def generate(self, dto: ChatgptResponseDTO) -> str:
        # ① DTO → Payload の変換を呼び出す
        payload = ChatGptPayload.from_dto(dto)

        # ② Client に通信を依頼する
        response = self.client.completion(payload.prompt)

        # ③ 外部の結果を DTO に戻す
        return response.choices[0].message.content

# **********************************************************************************


if __name__ == "__main__":
    ChatgptAdapter()