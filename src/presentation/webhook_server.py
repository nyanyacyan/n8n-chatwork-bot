# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))


from fastapi import FastAPI, Request
from src.base.chatwork import ChatworkClient
from src.base.chatgpt import ChatgptClient
from src.shared.logger import Logger

# Schema
from data.schema.api_response import StandardResponse

# flow


# ----------------------------------------------------------------------------------
# **********************************************************************************


# ----------------------------------------------------------------------------------

class WebhookServer:
    def __init__(self):
        # logger
        self.getLogger = Logger()
        self.logger = self.getLogger.getLogger()
        
        # FastAPI アプリケーションのインスタンス化
        self.app = FastAPI()
        
        # インスタンス
        self.chatwork_client = ChatworkClient()
        self.chatgpt_client = ChatgptClient()
        
        # flow
        
        self._add_routes()
        
# ----------------------------------------------------------------------------------
# ChatworkのWebhook受信ルートの追加メソッド

    def _add_routes(self):
        @self.app.post("/webhook/chatwork/one", response_model=StandardResponse)
        async def chatwork_webhook(request: Request):
            data = await request.json()
            self.logger.debug(f"Webhook 受信データ: {data}")
            
            #TODO ChatWork からのメッセージIDを取得
            return self.chatwork_client.flow_one(data)

# ----------------------------------------------------------------------------------
# slack_webhook

        @self.app.post("/webhook/chatwork/second", response_model=StandardResponse)
        async def slack_webhook(request: Request):
            data = await request.json()
            self.logger.debug(f"Webhook 受信データ: {data}")
            
            #TODO ChatWork からのメッセージIDを取得
            return self.chatwork_client.flow_second(data)

# ----------------------------------------------------------------------------------

# **********************************************************************************


if __name__ == "__main__":
    pass

# ----------------------------------------------------------------------------------
