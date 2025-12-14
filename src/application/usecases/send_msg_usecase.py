# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 仕様：Domainで定義した値をinitにて実施して値オブジェクト化させて設定内容を発動させる

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from domain.values.room_id import RoomId
from domain.values.reply_content import MsgContent
from src.application.dtos.send_msg_request import SendMsgRequest
from src.domain.ports.msg_sender_port import MsgSenderPort

# ----------------------------------------------------------------------------------
# **********************************************************************************


class SendMessageUseCase:
    def __init__(self, sender: MsgSenderPort):
        self.sender = sender

    def execute(self, dto: SendMsgRequest):
        room_id = RoomId(dto.room_id)
        content = MsgContent(dto.message)
        
        self.sender.send_msg(room_id, content)

# **********************************************************************************