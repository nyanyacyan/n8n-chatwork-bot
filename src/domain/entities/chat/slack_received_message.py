# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 仕様：
# 返信メッセージを表すエンティティ→ここに関しては送られてきたものが明確になっているだけにここは明確化する
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from dataclasses import dataclass
from src.domain.values.slack_channel_id import SlackChannelId
from src.domain.values.chat_msg_content import ChatMsgContent


# ----------------------------------------------------------------------------------
# **********************************************************************************


@dataclass(frozen=True)
class SlackReceivedMessage:
    room_id: SlackChannelId
    content: ChatMsgContent
    
    def length(self) -> int:
        return self.content.length() 
    
# **********************************************************************************