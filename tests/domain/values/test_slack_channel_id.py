# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 仕様：
# SlackChannelId が空でない文字列を受け付けることと、
# None/数値/空文字/空白で ValueError になることを確認する。
# 確認方法: 正常系は value を assert、異常系は pytest.raises を使用。
# 検証の順序 > 型チェック > Noneチェック > 値チェック
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import pytest

from src.domain.values.slack_channel_id import SlackChannelId


# ----------------------------------------------------------------------------------


def test_slack_channel_id_success():
    msg = SlackChannelId("C12345678")
    assert msg.value == "C12345678"

# ----------------------------------------------------------------------------------

@pytest.mark.parametrize(
    "invalid",
    [None, 123, "", "   "],
)
def test_slack_channel_id_invalid(invalid):
    with pytest.raises(ValueError):
        SlackChannelId(invalid)

# **********************************************************************************
