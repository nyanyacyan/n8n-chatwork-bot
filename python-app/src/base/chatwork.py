# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import requests
from fastapi import FastAPI, Request

from ..utils.logger import Logger
from ..utils.read_config import ReadConfig
from ...data.schema.chatwork import ChatworkConfig, ChatworkParams

# flow

# ----------------------------------------------------------------------------------
# **********************************************************************************
#TODO WebhookServerの構築
class ChatworkWebhookServer:
    def __init__(self):
        # logger
        self.getLogger = Logger()
        self.logger = self.getLogger.getLogger()

        self.app = FastAPI()

# ----------------------------------------------------------------------------------
# webhookのアクセスを検知して処理を実行するメソッド

    def process(self):
        pass


# ----------------------------------------------------------------------------------

    @app.post("/chatwork/webhook")
    async def chatwork_webhook(self, request: Request):
        data = await request.json()
        self.logger.info(f"Webhook受信: {data}")

        # TODO: Chatworkの内容を抽出して次の処理へ渡す
        return {"status": "ok"}

# ----------------------------------------------------------------------------------
# ChatWork API から “最新のメッセージ” を取得

class ChatworkClient:
    def __init__(self):
        # logger
        self.getLogger = Logger()
        self.logger = self.getLogger.getLogger()
        
        # 値マスククラス
        self.mask = ReadConfig()
        
        # インスタンス
        self.chatwork_config = ChatworkConfig()
        self.chatwork_value = ChatworkParams()
        self.api_token = self._get_api_token()
        self.headers = self._build_headers()

# ----------------------------------------------------------------------------------
# 新しいメッセージを取得するメソッド

    def get_new_message_text(self, check_message_id: int):
        message_data = self._get_new_message_data(check_message_id)
        if message_data and "messages" in message_data:
            messages = message_data["messages"]
            if messages:
                latest_message = messages[-1]
                message_body = latest_message.get("body", "")
                self.logger.debug(f"最新メッセージ取得: {message_body}")
                return message_body
        self.logger.debug("新しいメッセージがありません。")
        return None

# ----------------------------------------------------------------------------------
# メッセージデータを取得するメソッド

    def _get_new_message_data(self, check_message_id: int):
        request_url = self._get_request_url(check_message_id=check_message_id)
        params = self._get_params(check_message_id=check_message_id)
        response = requests.get(request_url, headers=self.headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            self.logger.error(f"ChatWork APIエラー: {response.status_code} - {response.text}")
            return None

# ----------------------------------------------------------------------------------
# ヘッダーを構築するメソッド

    def _build_headers(self):
        headers = {
            "X-ChatWorkToken": self.api_token,
            "Content-Type": "application/json"
        }
        return headers

# ----------------------------------------------------------------------------------
# APIトークンを取得するメソッド

    def _get_api_token(self):
        api_token = self.chatwork_config.chatwork_api_token
        mask_value = self.mask.mask_value(value=api_token)
        self.logger.debug(f"ChatWork APIトークン取得: {mask_value}")
        return api_token

# ----------------------------------------------------------------------------------
# リクエストするURLを取得するメソッド

    def _get_request_url(self, check_message_id: int):
        url = f"{self.chatwork_value.endpoint_url}/rooms/{check_message_id}/messages"
        mask_url = self.mask.mask_value(value=url)
        self.logger.debug(f"ChatWork リクエストURL取得: {mask_url}")
        return url

# ----------------------------------------------------------------------------------
# リクエストパラメータを取得するメソッド
# force=1 → 未取得のメッセージがなくても強制的に最新メッセージ一覧を返す（常に全件返す）

    def _get_params(self, check_message_id: int):
        params = {
            "force": 1,
            "since": check_message_id
        }
        mask_params = self.mask.mask_value(value=params)
        self.logger.debug(f"ChatWork リクエストパラメータ取得: {mask_params}")
        return params

# ----------------------------------------------------------------------------------
#TODO ChatWork のマイチャットへの返信




# ----------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------



# **********************************************************************************

if __name__ == "__main__":
    ChatworkWebhookServer().process()

# ----------------------------------------------------------------------------------
