# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 仕様：
# 検証の順序 > 型チェック > Noneチェック > 値チェック
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import pytest

from src.domain.values.reply_content import ReplyContent

# ----------------------------------------------------------------------------------


def test_reply_content_success():
    reply = ReplyContent("これは返信メッセージです")
    assert reply.value == "これは返信メッセージです"

# ----------------------------------------------------------------------------------

@pytest.mark.parametrize(
    "invalid",
    ["", "   ", None, 123],
)

def test_reply_content_invalid(invalid):
    with pytest.raises(ValueError):
        ReplyContent(invalid)

# **********************************************************************************