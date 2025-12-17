# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# Adapterファイル作成

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from src.domain.ports.msg_sender_port import MsgSenderPort
from src.domain.ports.msg_reader_port import MsgReaderPort

# 値
from src.domain.values.chat_msg_content import ChatMsgContent
from src.domain.values.room_id import RoomId
from domain.entities.chat.outgoing_message import Message
from domain.entities.chat.received_message import ReceivedChatMessage

from .client import ChatWorkClient
from .config import ChatworkConfig

# ----------------------------------------------------------------------------------
# **********************************************************************************


class ChatworkSendMsgAdapter(MsgSenderPort):
    def __init__(self, client: ChatWorkClient):
        self.client = client

# ----------------------------------------------------------------------------------


    def execute(self, msg: Message) -> None:
        room_id = msg.room_id.value
        msg_content = msg.content.value

        # メッセージを送信
        return self.client.send_message( room_id=room_id, msg_content=msg_content )
        
# **********************************************************************************


class ChatworkGetMessagesAdapter(MsgReaderPort):
    def __init__(self, client: ChatWorkClient):
        self.client = client
        
# ----------------------------------------------------------------------------------


    def execute(self, room_id: RoomId):
        raw_room_id = room_id.value
        return self.client.get_messages(room_id=raw_room_id)

# **********************************************************************************