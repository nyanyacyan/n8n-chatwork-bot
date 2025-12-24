# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 仕様：

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from dataclasses import dataclass
from src.domain.values.chatwork_room_id import RoomId
from domain.values.chat_msg_content import ChatMsgContent



# ----------------------------------------------------------------------------------
# **********************************************************************************


@dataclass(frozen=True)
class OutgoingMessage:
    room_id: RoomId
    content: ChatMsgContent

    def length(self) -> int:
        return self.content.length()

# **********************************************************************************