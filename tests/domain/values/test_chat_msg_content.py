# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 仕様：
# ChatMsgContent の値オブジェクトが有効な文字列を保持できることと、
# 空文字・空白・None・長すぎる文字列・非文字列で ValueError になることを確認する。
# 確認方法: 正常系は value と length を assert、異常系は pytest.raises を使用。

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
