# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 仕様：
# WebhookServer はルーティングと依存注入のみを担当する

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from fastapi import FastAPI, Request

from src.application.usecases.assist_chat_reply_usecase import AssistChatReplyUseCase
from src.presentation.controllers.chatwork_webhook_controller import ChatworkWebhookController
from src.shared.logger import Logger

# ----------------------------------------------------------------------------------
# **********************************************************************************


class WebhookServer:
    def __init__(self, reply_usecase: AssistChatReplyUseCase):
        if reply_usecase is None:
            raise ValueError("reply_usecase は必須です")

        logger_setup = Logger()
        self.logger = logger_setup.getLogger()

        self.app = FastAPI()
        self.chatwork_controller = ChatworkWebhookController(
            reply_usecase=reply_usecase,
            logger=self.logger,
        )
        self._add_routes()

# ----------------------------------------------------------------------------------
# Chatwork Webhook ルート追加

    def _add_routes(self):
        @self.app.post("/webhook/chatwork")
        async def chatwork_webhook(request: Request):
            return await self.chatwork_controller.chatwork_webhook(request)

        # 互換性のため旧ルートを残す
        @self.app.post("/webhook/chatwork/one")
        async def chatwork_webhook_one(request: Request):
            return await chatwork_webhook(request)

        @self.app.post("/webhook/chatwork/second")
        async def chatwork_webhook_second(request: Request):
            return await chatwork_webhook(request)

# **********************************************************************************


def create_app(reply_usecase: AssistChatReplyUseCase) -> FastAPI:
    return WebhookServer(reply_usecase=reply_usecase).app
