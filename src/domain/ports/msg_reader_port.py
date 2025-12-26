# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 仕様：最新メッセージ取得能力を定義するポート

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from typing import Protocol
from src.domain.values.chatwork_room_id import ChatworkRoomId
from src.domain.entities.chat.chatwork_received_message import ChatworkReceivedMessage

# ----------------------------------------------------------------------------------
# **********************************************************************************


class MsgReaderPort(Protocol):
    def execute(self,room_id: ChatworkRoomId) -> list[ChatworkReceivedMessage]:
        ...

# **********************************************************************************
