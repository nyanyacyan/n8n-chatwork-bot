# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from typing import Dict
from openai import OpenAI
from ..utils.logger import Logger

# value
from ...data.schema.ai import ChatgptValue, ChatgptConfig, ChatgptRequestValue

# flow


# ----------------------------------------------------------------------------------
# **********************************************************************************

class AIChatGPT:
    def __init__(self):
        # logger
        self.getLogger = Logger()
        self.logger = self.getLogger.getLogger()
        
        chatgpt_config = ChatgptConfig()

        #! api_key →必ずvalueで値を取得する
        self.api_token = chatgpt_config.chatgpt_api_token

        # リクエストの核となるクライアントを生成
        self.client = OpenAI(api_key=self.api_token)
        
        self.request_value = ChatgptRequestValue()

# **********************************************************************************
# ----------------------------------------------------------------------------------
# 単独のリクエスト

    def simple_request(self):
        self.logger.info("ChatGPTへの単独リクエストを実行")
        
        model_enum = self.request_value.model
        self.logger.debug(f"現在のモデル: {model_enum.value}")

        
        try:
            response = self.client.chat.completions.create(
                model="gpt-5-mini-2025-08-07",
                messages=[
                    {"role": "user", "content": "Hello, world!"}
                ]
            )
            self.logger.info(f"ChatGPTからの応答: {response}")
            return response
        
        except Exception as e:
            self.logger.error(f"ChatGPTリクエスト中にエラーが発生: {e}")
            return None

# ----------------------------------------------------------------------------------
# プロンプト生成

    def get_response_text(self, response: Dict) -> str:
        try:
            self.logger.info("ChatGPTの応答テキストを抽出")
            response_text = response.choices[0].message.content
            self.logger.debug(f"抽出された応答テキスト: {response_text}")
            return response_text
        
        # TODO: 詳細な例外処理を追加→再リクエストを定義
        except Exception as e:
            self.logger.error(f"応答テキストの抽出中にエラーが発生: {e}")
            return
        
    
# ----------------------------------------------------------------------------------
# TODO 再リクエストを定義

# ----------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------

if __name__ == "__main__":
    pass

# ----------------------------------------------------------------------------------
