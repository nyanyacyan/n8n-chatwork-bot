# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 仕様：
# SendMsgRequest が room_id と msg を保持できることを確認する。
# 確認方法: 生成後に room_id と msg を assert。
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import

from src.application.dtos.send_msg_request import SendMsgRequest

# ----------------------------------------------------------------------------------


def test_send_msg_request_success():
    req = SendMsgRequest(room_id="123", msg="hello")
    assert req.room_id == "123"
    assert req.msg == "hello"

# **********************************************************************************
