# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 仕様：

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from src.domain.entities.llm.response import Response
from src.domain.entities.chat.outgoing_message import OutgoingMessage
from src.domain.values.chat_msg_content import ChatMsgContent
from src.domain.values.room_id import RoomId
from src.domain.ports.msg_sender_port import MsgSenderPort
from shared.logger import Logger


# ----------------------------------------------------------------------------------
# **********************************************************************************


class SendChatMessageUseCase:
    def __init__(self, sender: MsgSenderPort):
        # logger
        self.logger_setup = Logger()
        self.logger = self.logger_setup.getLogger()
        
        # インスタンス
        self.sender = sender
        
# ----------------------------------------------------------------------------------


    def execute(self, response: Response, room_id: RoomId) -> None:
        self.logger.info("Chat メッセージ送信処理を開始")

        # Response → ChatMessage へ変換
        msg = OutgoingMessage(
            room_id=room_id,
            content=ChatMsgContent(response.content.value)
        )

        self.sender.execute(msg)

        self.logger.info("Chat メッセージ送信処理が完了")

# **********************************************************************************