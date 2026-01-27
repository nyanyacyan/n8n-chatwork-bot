# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# Adapterファイル作成

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from src.domain.ports.msg_sender_port import MsgSenderPort
from src.domain.ports.msg_reader_port import MsgReaderPort

# 値
from src.domain.values.chat_msg_content import ChatMsgContent
from src.domain.values.chatwork_room_id import ChatworkRoomId
from src.domain.entities.chat.send_message import SendMessage
from src.domain.entities.chat.chatwork_received_message import ChatworkReceivedMessage

from .client import ChatWorkClient

# ----------------------------------------------------------------------------------
# **********************************************************************************


class ChatworkSendMsgAdapter(MsgSenderPort):
    def __init__(self, client: ChatWorkClient):
        self.client = client

# ----------------------------------------------------------------------------------


    def execute(self, msg: SendMessage) -> None:
        room_id = msg.room_id.value
        msg_content = msg.content.value

        # メッセージを送信
        return self.client.send_message( room_id=room_id, msg_content=msg_content )
        
# **********************************************************************************


class ChatworkGetMessagesAdapter(MsgReaderPort):
    def __init__(self, client: ChatWorkClient):
        self.client = client
        
# ----------------------------------------------------------------------------------


    def execute(self, room_id: ChatworkRoomId) -> list[ChatworkReceivedMessage]:
        raw_messages = self.client.get_messages(room_id=room_id.value)

        messages = []
        for raw in raw_messages:
            messages.append(
                ChatworkReceivedMessage(
                    room_id=room_id,
                    content=ChatMsgContent(raw["body"])
                )
            )
        return messages

# **********************************************************************************
