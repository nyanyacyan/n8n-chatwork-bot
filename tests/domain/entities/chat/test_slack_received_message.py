# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 仕様：
# SlackReceivedMessage が channel_id と content を保持し、
# length が内容文字数と一致することを確認する。
# 確認方法: 生成後に room_id/content/length を assert。
# 正常系のみでOK
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from src.domain.entities.chat.slack_received_message import SlackReceivedMessage
from src.domain.values.slack_channel_id import SlackChannelId
from src.domain.values.chat_msg_content import ChatMsgContent

# **********************************************************************************


def test_slack_received_message_success():
    channel_id = SlackChannelId("C123456")
    content = ChatMsgContent("hello")

    msg = SlackReceivedMessage(
        room_id=channel_id,
        content=content,
    )

    assert msg.room_id == channel_id
    assert msg.content == content
    assert msg.length() == len("hello")

# **********************************************************************************
