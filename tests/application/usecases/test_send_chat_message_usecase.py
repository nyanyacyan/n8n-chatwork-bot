# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 仕様：
# SendChatMessageUseCase が Response と room_id から SendMessage を作成し、
# MsgSenderPort に渡すことを確認する。
# 確認方法: Fake の called/received を assert し、渡された内容が期待通りであることを assert。
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import

from src.application.usecases.send_chat_message_usecase import SendChatMessageUseCase
from src.domain.entities.llm.response import Response
from src.domain.values.llm_response_content import LLMResponseContent
from src.domain.values.chatwork_room_id import ChatworkRoomId
from src.domain.values.chat_msg_content import ChatMsgContent

# ----------------------------------------------------------------------------------


class FakeMsgSender:
    def __init__(self):
        self.called = False
        self.received_msg = None

    def execute(self, msg):
        self.called = True
        self.received_msg = msg


# ----------------------------------------------------------------------------------


def test_send_chat_message_usecase_success():
    response = Response(LLMResponseContent("dummy response"))
    room_id = ChatworkRoomId(123)

    fake_sender = FakeMsgSender()
    usecase = SendChatMessageUseCase(fake_sender)

    usecase.execute(response=response, room_id=room_id)

    assert fake_sender.called is True
    assert fake_sender.received_msg.room_id == room_id
    assert isinstance(fake_sender.received_msg.content, ChatMsgContent)
    assert fake_sender.received_msg.content.value == "dummy response"

# **********************************************************************************
