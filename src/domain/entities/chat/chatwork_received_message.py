# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 仕様：
# 返信メッセージを表すエンティティ→ここに関しては送られてきたものが明確になっているだけにここは明確化する
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from dataclasses import dataclass
from src.domain.values.chatwork_room_id import ChatworkRoomId
from src.domain.values.chat_msg_content import ChatMsgContent

# ----------------------------------------------------------------------------------
# **********************************************************************************


@dataclass(frozen=True)
class ChatworkReceivedMessage:
    room_id: ChatworkRoomId
    content: ChatMsgContent
    
    def length(self) -> int:
        return self.content.length() 

# **********************************************************************************

