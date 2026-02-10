# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 仕様：
# generate_reply_request.GenerateReplyRequest が room_id と message を保持できることを確認する。
# 確認方法: 生成後に room_id と message を assert。
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import

from src.application.dtos.generate_reply_request import GenerateReplyRequest

# ----------------------------------------------------------------------------------


def test_generate_reply_request_success():
    req = GenerateReplyRequest(room_id="123", message="hello")
    assert req.room_id == "123"
    assert req.message == "hello"

# **********************************************************************************
