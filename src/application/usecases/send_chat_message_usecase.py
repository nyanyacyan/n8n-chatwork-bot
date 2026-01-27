# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 仕様：

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from src.domain.entities.llm.response import Response
from src.domain.entities.chat.send_message import SendMessage
from src.domain.values.chat_msg_content import ChatMsgContent
from src.domain.values.chatwork_room_id import ChatworkRoomId
from src.domain.ports.msg_sender_port import MsgSenderPort
from src.shared.logger import Logger


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


    def execute(self, response: Response, room_id: ChatworkRoomId) -> None:
        self.logger.info("Chat メッセージ送信処理を開始")

        # Response → ChatMessage へ変換
        msg = SendMessage(
            room_id=room_id,
            content=ChatMsgContent(response.content.value)
        )

        self.sender.execute(msg)

        self.logger.info("Chat メッセージ送信処理が完了")

# **********************************************************************************