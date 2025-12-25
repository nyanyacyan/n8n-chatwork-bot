# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 仕様：
# 検証の順序 > 型チェック > Noneチェック > 値チェック
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import pytest

from src.domain.values.slack_channel_id import SlackChannelId


# ----------------------------------------------------------------------------------


def test_XXX_success():
    msg = SlackChannelId("C12345678")
    assert msg.value == "C12345678"

# ----------------------------------------------------------------------------------

@pytest.mark.parametrize(
    "invalid",
    [None, 123, "", "   "],
)
def test_xxx_invalid(invalid):
    with pytest.raises(ValueError):
        SlackChannelId(invalid)

# **********************************************************************************