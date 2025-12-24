# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 仕様：pytestによるroom_idの単体テスト

# 実行：pytest tests/domain/values/test_room_id.py
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import pytest

from src.domain.values.chatwork_room_id import ChatworkRoomId


# ----------------------------------------------------------------------------------
# **********************************************************************************

# ================================
#* 正常系
# ================================

def test_room_id_success():
    room_id = ChatworkRoomId(123)
    assert room_id.value == 123


# ================================
#! 異常系
# ================================

@pytest.mark.parametrize(
    "invalid_value",
    [
        "",
        "   ",
        None,
        "123",
    ],
)

def test_room_id_invalid(invalid_value):
    with pytest.raises(ValueError):
        ChatworkRoomId(invalid_value)

# **********************************************************************************