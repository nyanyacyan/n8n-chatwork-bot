# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 仕様：
# 正常系のみでOK
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import pytest

from src.domain.entities.chat.outgoing_message import OutgoingMessage
from src.domain.values.chatwork_room_id import ChatworkRoomId
from src.domain.values.slack_channel_id import SlackChannelId
from src.domain.values.chat_msg_content import ChatMsgContent

# **********************************************************************************

@pytest.mark.parametrize(
    "destination",
    [
        ChatworkRoomId(123),
        SlackChannelId("C123456"),
    ],
)

def test_outgoing_message_accepts_any_destination(destination):
    content = ChatMsgContent("hello")

    msg = OutgoingMessage(
        room_id=destination,
        content=content,
    )

    assert msg.room_id == destination
    assert msg.length() == len("hello")

# **********************************************************************************