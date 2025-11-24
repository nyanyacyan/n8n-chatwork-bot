# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import time, random, asyncio
from typing import Dict
from openai import OpenAI
from openai import AsyncOpenAI
from src.utils.logger import Logger

# value
from data.schema.ai import ChatgptConfig, ChatgptRequestValue


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
        
        # 基本の値
        self.request_value = ChatgptRequestValue()

        # 蓄積するメッセージ履歴(別ファイルで実装予定)
        self.message_history = []

# **********************************************************************************
# ----------------------------------------------------------------------------------
# 【同期】単独のリクエスト

    def simple_request(self, prompt: str) -> Dict:
        self.logger.info("ChatGPTへの単独リクエストを実行")
        
        model_enum = self.request_value.model
        self.logger.debug(f"現在のモデル: {model_enum.value}")

        try:
            response = self.client.chat.completions.create(
                model=model_enum.value,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            self.logger.info(f"ChatGPTからの応答: {response}")
            response_text = self.get_response_text(response)
            return response_text
        
        except Exception as e:
            # リトライ
            retry_prompt = self.request_value.retry_prompt
            succsess_attribute = self.request_value.success_attribute
            
            self.logger.warning("ChatGPTリクエストに失敗、再リクエストを試みます")
            retry_response = self.retry_request(
                retry_prompt=retry_prompt,
                obj_attribute=succsess_attribute
            )
            if retry_response:
                return retry_response
            self.logger.error(f"ChatGPTリクエスト中にエラーが発生: {e}")
            return None

# ----------------------------------------------------------------------------------
# レスポンスから応答テキストを抽出

    def get_response_text(self, response: Dict) -> str:
        try:
            self.logger.info("ChatGPTの応答テキストを抽出")
            response_text = response.choices[0].message.content
            self.logger.debug(f"抽出された応答テキスト: {response_text}")
            return response_text
        
        except Exception as e:
            self.logger.error(f"応答テキストの抽出中にエラーが発生: {e}")
            return
        
    
# ----------------------------------------------------------------------------------
# 再リクエストを定義

    def retry_request(self, retry_prompt: str, obj_attribute: str, max_retries: int =3) -> Dict:
        for attempt in range(1, max_retries + 1):

            self.logger.info(f"再リクエスト {attempt}/{max_retries}")

            response = self.simple_request(prompt=retry_prompt)

            # -------------------------------------------------------
            # 成功判定ロジック（重要）
            # hasattrはオブジェクトに特定の属性が存在するかを確認する関数
            # -------------------------------------------------------
            if response and hasattr(response, obj_attribute):
                return response

            # -------------------------------------------------------
            # 最終試行なら終了
            # -------------------------------------------------------
            if attempt == max_retries:
                self.logger.error("全ての再リクエストに失敗しました。")
                return None

            # -------------------------------------------------------
            # Exponential Backoff + Jitter
            # → API制限や一時的なエラー時に、待機時間を指数的に伸ばしつつランダム性を加えることで
            #    他の再試行と衝突しにくくし、成功率を上げるための一般的なアルゴリズム
            # -------------------------------------------------------
            sleep_time = (2 ** attempt) + random.uniform(0, 0.5)
            self.logger.warning(f"リトライ待機: {sleep_time:.1f} 秒")
            time.sleep(sleep_time)
        
# ----------------------------------------------------------------------------------
# 【非同期】単独リクエスト

    async def async_simple_request(self, prompt: str) -> Dict:
        self.logger.info("ChatGPTへの非同期単独リクエストを実行")
        
        model_enum = self.request_value.model
        self.logger.debug(f"現在のモデル: {model_enum.value}")

        async_client = AsyncOpenAI(api_key=self.api_token)

        try:
            response = await async_client.chat.completions.create(
                model=model_enum.value,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            self.logger.info(f"ChatGPTからの応答: {response}")
            response_text = self.get_response_text(response)
            return response_text
        
        except Exception as e:
            retry_prompt = self.request_value.retry_prompt
            succ_attr = self.request_value.success_attribute
            return await self.retry_request(retry_prompt, succ_attr)

# ----------------------------------------------------------------------------------
# 【非同期】再リクエストを定義

    async def retry_request(self, retry_prompt: str, obj_attribute: str, max_retries: int = 3):
        for attempt in range(1, max_retries + 1):
            response = await self.simple_request(retry_prompt)

            if response and hasattr(response, obj_attribute):
                return response

            if attempt == max_retries:
                return None

            sleep_time = (2 ** attempt) + random.uniform(0, 0.5)
            await asyncio.sleep(sleep_time)

# ----------------------------------------------------------------------------------
#TODO ここからは別ファイルにてこれから実装予定
# 【同期】蓄積型のリクエスト

    def save_type_request(self, prompt: str) -> Dict:
        self.logger.info("ChatGPTへの単独リクエストを実行")
        
        model_enum = self.request_value.model
        self.logger.debug(f"現在のモデル: {model_enum.value}")

        self.saved_request_msg(prompt=prompt)

        try:
            response = self.client.chat.completions.create(
                model=model_enum.value,
                messages=self.message_history
            )
            self.logger.info(f"ChatGPTからの応答: {response}")
            self.saved_response_msg(response=response)
            return response
        
        except Exception as e:
            # リトライ
            retry_prompt = self.request_value.retry_prompt
            succsess_attribute = self.request_value.success_attribute
            
            self.logger.warning("ChatGPTリクエストに失敗、再リクエストを試みます")
            retry_response = self.retry_request(
                retry_prompt=retry_prompt,
                obj_attribute=succsess_attribute
            )
            if retry_response:
                return retry_response
            self.logger.error(f"ChatGPTリクエスト中にエラーが発生: {e}")
            return None

# ----------------------------------------------------------------------------------
# リクエストmsgを蓄積
#TODO ここからは別ファイルにてこれから実装予定

    def saved_request_msg(self, prompt: str) -> Dict:
        request_content = {"role": "user", "content": prompt}
        self.message_history.append(request_content)
        self.logger.debug(f"ChatGPTへの蓄積型リクエストを実行: {self.message_history:50}")
        return request_content

# ----------------------------------------------------------------------------------
# レスポンスmsgを蓄積
#TODO ここからは別ファイルにてこれから実装予定

    def saved_response_msg(self, response: Dict) -> Dict:
        try:
            response_text = self.get_response_text(response)
            response_content = {"role": "assistant", "content": response_text}
            self.message_history.append(response_content)
            self.logger.debug(f"ChatGPTからの蓄積型応答を実行: {response_content:50}")
            return response_content
        
        except Exception as e:
            self.logger.error(f"応答テキストの抽出中にエラーが発生: {e}")
            return



# ----------------------------------------------------------------------------------

# if __name__ == "__main__":
#     chatgpt = AIChatGPT()
#     test_prompt = "こんにちは、元気ですか？"
#     response = chatgpt.simple_request(test_prompt)
#     print(f"ChatGPTの応答: {response}")
    
if __name__ == "__main__":
    chatgpt = AIChatGPT()
    test_prompt = "こんにちは、元気ですか？"
    response = asyncio.run(chatgpt.async_simple_request(test_prompt))
    print(f"ChatGPTの応答: {response}")
        
# ----------------------------------------------------------------------------------
