# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 仕様：

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from dataclasses import dataclass
from src.domain.ports.message_destination_port import MessageDestination
from src.domain.values.chat_msg_content import ChatMsgContent

# ----------------------------------------------------------------------------------
# **********************************************************************************


@dataclass(frozen=True)
class SendMessage:
    room_id: MessageDestination
    content: ChatMsgContent

    def length(self) -> int:
        return self.content.length()

# **********************************************************************************