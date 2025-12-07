# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# Client は “外部サービスと通信する実体(=外部の窓口)” 
# API通信を行う役
# HTTP/リクエスト処理の責務
# 外部仕様に合わせて作られる層
# インフラ層の実装者

# ・Application層 → Clientの契約 (=Protocol)を知る
# ・Infrastructure層 → Clientの実装を持つ

# Application
#    │  (知るのは “clientがある”という事実だけ)
#    ▼
# ChatGPTClient(Protocol)
#    ▲
#    │
# OpenAIClient(実装)
#    │
# 外部API(OpenAI)

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import openai
from enum import Enum
from pydantic import BaseModel
from pydantic_settings import BaseSettings


# ChatGPT関連
from .config import ChatgptConfig
from .response_dto import ChatgptResponseDTO
from .request_dto import ChatgptRequestValue
from data.domain.interfaces.chatgpt_client import ChatGPTClient

# ----------------------------------------------------------------------------------
# **********************************************************************************
# ChatGPTClientという抽象インターフェースの実装
# 中身を抽象化（=隠蔽）し、外側に漏れない=Clean Architectureの原則
# ChatGPTClientはdomainにて抽象化された値

class OpenAIClient(ChatGPTClient):
    def __init__(self, config: ChatgptConfig):
        self.config = config

    def completion(self, dto: ChatgptRequestValue):
        result = openai.chat.completions.create(
            model=dto.model.value,
            messages=[
                {"role": "user", "content": dto.prompt}
            ],
            api_key=ChatgptConfig.chatgpt_api_token.value
        )
        return ChatgptResponseDTO(
            msg=result.choices[0].message["content"]
        )


# **********************************************************************************


if __name__ == "__main__":
    test_openai = OpenAIClient()
    test_dto = ChatgptRequestValue(
        prompt="Hello, ChatGPT! How are you today?"
    )
    response = test_openai.completion(test_dto)
    print(response.msg)