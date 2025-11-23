# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from typing import Dict, Optional, Callable, Any
import time
from openai import OpenAI
from openai import APIError, APIConnectionError, RateLimitError, APITimeoutError
from ..utils.logger import Logger

# value
from ...data.schema.ai import ChatgptConfig, ChatgptRequestValue

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

        def _make_request():
            return self.client.chat.completions.create(
                model="gpt-5-mini-2025-08-07",
                messages=[
                    {"role": "user", "content": "Hello, world!"}
                ]
            )
        
        response = self._retry_request(_make_request)
        
        if response:
            self.logger.info(f"ChatGPTからの応答: {response}")
        else:
            self.logger.error("ChatGPTリクエストが最終的に失敗しました")
            
        return response

# ----------------------------------------------------------------------------------
# プロンプト生成

    def get_response_text(self, response: Dict) -> Optional[str]:
        try:
            self.logger.info("ChatGPTの応答テキストを抽出")
            
            # レスポンスの検証
            if response is None:
                self.logger.error("レスポンスがNoneです")
                return None
                
            if not hasattr(response, 'choices') or not response.choices:
                self.logger.error("レスポンスにchoicesが含まれていません")
                return None
                
            if not response.choices[0].message:
                self.logger.error("レスポンスにmessageが含まれていません")
                return None
            
            response_text = response.choices[0].message.content
            
            if response_text is None or response_text == "":
                self.logger.warning("応答テキストが空です")
                return None
                
            self.logger.debug(f"抽出された応答テキスト: {response_text}")
            return response_text
        
        except AttributeError as e:
            self.logger.error(f"応答の構造が予期しない形式です: {e}")
            return None
            
        except IndexError as e:
            self.logger.error(f"応答のインデックスアクセスに失敗しました: {e}")
            return None
        
        except Exception as e:
            self.logger.error(f"応答テキストの抽出中に予期しないエラーが発生: {e}")
            return None
        
    
# ----------------------------------------------------------------------------------
# TODO 再リクエストを定義

    def _retry_request(self, request_func: Callable, *args, **kwargs) -> Optional[Any]:
        """
        リトライ機能を持つリクエスト実行メソッド
        
        Args:
            request_func: 実行するリクエスト関数
            *args: リクエスト関数の位置引数
            **kwargs: リクエスト関数のキーワード引数
            
        Returns:
            リクエストの結果、または失敗時はNone
        """
        max_retries = self.request_value.max_retries
        retry_delay = self.request_value.retry_delay
        backoff_factor = self.request_value.backoff_factor
        
        for attempt in range(max_retries):
            try:
                self.logger.info(f"リクエスト試行 {attempt + 1}/{max_retries}")
                result = request_func(*args, **kwargs)
                self.logger.info("リクエストが成功しました")
                return result
                
            except RateLimitError as e:
                self.logger.warning(f"レート制限エラー（試行 {attempt + 1}/{max_retries}）: {e}")
                if attempt < max_retries - 1:
                    wait_time = retry_delay * (backoff_factor ** attempt)
                    self.logger.info(f"{wait_time}秒待機してから再試行します")
                    time.sleep(wait_time)
                else:
                    self.logger.error("最大リトライ回数に達しました（レート制限エラー）")
                    return None
                    
            except APITimeoutError as e:
                self.logger.warning(f"タイムアウトエラー（試行 {attempt + 1}/{max_retries}）: {e}")
                if attempt < max_retries - 1:
                    wait_time = retry_delay * (backoff_factor ** attempt)
                    self.logger.info(f"{wait_time}秒待機してから再試行します")
                    time.sleep(wait_time)
                else:
                    self.logger.error("最大リトライ回数に達しました（タイムアウトエラー）")
                    return None
                    
            except APIConnectionError as e:
                self.logger.warning(f"接続エラー（試行 {attempt + 1}/{max_retries}）: {e}")
                if attempt < max_retries - 1:
                    wait_time = retry_delay * (backoff_factor ** attempt)
                    self.logger.info(f"{wait_time}秒待機してから再試行します")
                    time.sleep(wait_time)
                else:
                    self.logger.error("最大リトライ回数に達しました（接続エラー）")
                    return None
                    
            except APIError as e:
                self.logger.error(f"APIエラー（試行 {attempt + 1}/{max_retries}）: {e}")
                # APIエラーは通常リトライしても解決しないため、即座に終了
                return None
                
            except Exception as e:
                self.logger.error(f"予期しないエラー（試行 {attempt + 1}/{max_retries}）: {e}")
                if attempt < max_retries - 1:
                    wait_time = retry_delay * (backoff_factor ** attempt)
                    self.logger.info(f"{wait_time}秒待機してから再試行します")
                    time.sleep(wait_time)
                else:
                    self.logger.error("最大リトライ回数に達しました（予期しないエラー）")
                    return None
        
        return None

# ----------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------

if __name__ == "__main__":
    pass

# ----------------------------------------------------------------------------------
