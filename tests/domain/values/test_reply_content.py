# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 仕様：
# ReplyContent の値オブジェクトが有効な文字列を保持できることと、
# 空文字・空白・None・非文字列で ValueError になることを確認する。
# 確認方法: 正常系は value を assert、異常系は pytest.raises を使用。
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
