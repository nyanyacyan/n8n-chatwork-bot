# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 仕様：
# 正常系のみでOK
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from src.domain.entities.chat.chatwork_received_message import ChatworkReceivedMessage
from src.domain.values.chatwork_room_id import ChatworkRoomId
from src.domain.values.chat_msg_content import ChatMsgContent

# **********************************************************************************


def test_chatwork_received_message_success():
    room_id = ChatworkRoomId(123)
    content = ChatMsgContent("hello")

    msg = ChatworkReceivedMessage(
        room_id=room_id,
        content=content,
    )

    assert msg.room_id == room_id
    assert msg.content == content
    assert msg.length() == len("hello")

# **********************************************************************************