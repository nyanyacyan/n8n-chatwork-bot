# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 仕様：最新メッセージ取得能力を定義するポート

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from typing import Protocol
from src.domain.values.chatwork_room_id import RoomId
from domain.entities.chat.received_message import ReceivedChatMessage

# ----------------------------------------------------------------------------------
# **********************************************************************************


class MsgReaderPort(Protocol):
    def execute(self,room_id: RoomId) -> list[ReceivedChatMessage]:
        ...

# **********************************************************************************
