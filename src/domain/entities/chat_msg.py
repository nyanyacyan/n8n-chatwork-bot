# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 仕様：

# valueObjectは具体的なファイル名、機能をもたせることでファイル名を少し曖昧にする
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from dataclasses import dataclass
from domain.values.room_id import RoomId
from domain.values.chat_msg_content import ChatMsgContent

# ----------------------------------------------------------------------------------
# **********************************************************************************


@dataclass(frozen=True)
class ChatMsg:
    room_id: RoomId
    content: ChatMsgContent

# **********************************************************************************
