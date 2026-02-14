# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 仕様：
# Chatwork Webhook の受信処理本体を担当する Controller
# Presentation層として、受信 -> DTO化 -> UseCase委譲 -> HTTP応答を行う

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from fastapi import HTTPException, Request

from src.application.dtos.get_new_msg import GetNewMsgRequest
from src.application.usecases.assist_chat_reply_usecase import AssistChatReplyUseCase
from src.presentation.dtos.webhook_request_dto import ChatworkWebhookRequestDto


# ----------------------------------------------------------------------------------
# **********************************************************************************


class ChatworkWebhookController:
    def __init__(self, reply_usecase: AssistChatReplyUseCase, logger):
        if reply_usecase is None:
            raise ValueError("reply_usecase は必須です")

        self.reply_usecase = reply_usecase
        self.logger = logger

# ----------------------------------------------------------------------------------
# 問題がなかった際のResponse

    @staticmethod
    def _to_response(room_id: int) -> dict:
        return {
            "status": "ok",
            "message": "webhook processed",
            "room_id": room_id,
        }

# ----------------------------------------------------------------------------------
# Chatwork webhook を受け取って UseCase を実行する

    async def chatwork_webhook(self, request: Request) -> dict:
        data = await request.json()
        self.logger.debug(f"Webhook 受信データ: {data}")

        try:
            webhook_req = ChatworkWebhookRequestDto.from_payload(data)
        except ValueError as e:
            self.logger.error(f"Webhook payload の room_id 解析に失敗: {e}")
            raise HTTPException(status_code=400, detail=str(e)) from e

        req = GetNewMsgRequest(room_id=webhook_req.room_id)

        try:
            self.reply_usecase.execute(req)
        except Exception as e:
            self.logger.error(f"返信処理に失敗: {e}")
            raise HTTPException(
                status_code=500,
                detail="返信処理でエラーが発生しました",
            ) from e

        return self._to_response(webhook_req.room_id)

# **********************************************************************************
