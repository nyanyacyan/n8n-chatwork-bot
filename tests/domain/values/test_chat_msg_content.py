# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 仕様：

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import pytest

from src.domain.values.chat_msg_content import ChatMsgContent


# ----------------------------------------------------------------------------------


def test_chat_msg_content_success():
    msg = ChatMsgContent("これはテストメッセージです")
    assert msg.value == "これはテストメッセージです"
    assert msg.length() == 13
    

# ----------------------------------------------------------------------------------

@pytest.mark.parametrize(
    "invalid",
    ["", "   ", None, "a" * 2001, 12345],
)
def test_chat_msg_invalid(invalid):
    with pytest.raises(ValueError):
        ChatMsgContent(invalid)

# **********************************************************************************