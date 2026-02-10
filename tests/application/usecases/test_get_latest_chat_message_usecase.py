# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 仕様：
# GetLatestChatMessageUseCase が MsgReaderPort を呼び出し、
# 取得したメッセージ配列の最後の要素を返すことを確認する。
# 確認方法: Fake の called/received を assert、戻り値が最後のメッセージであることを assert。
# また、メッセージが空の場合は ValueError になることを確認する。
# 確認方法: pytest.raises を使用。
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import pytest

from src.application.usecases.get_latest_chat_message_usecase import GetLatestChatMessageUseCase
from src.application.dtos.get_new_msg import GetNewMsgRequest
from src.domain.values.chatwork_room_id import ChatworkRoomId
from src.domain.values.chat_msg_content import ChatMsgContent
from src.domain.entities.chat.chatwork_received_message import ChatworkReceivedMessage

# ----------------------------------------------------------------------------------


class FakeMsgReader:
    def __init__(self, messages):
        self.messages = messages
        self.called = False
        self.received_room_id = None

    def execute(self, room_id: ChatworkRoomId):
        self.called = True
        self.received_room_id = room_id
        return self.messages


# ----------------------------------------------------------------------------------


def test_get_latest_chat_message_usecase_success():
    msg1 = ChatworkReceivedMessage(
        room_id=ChatworkRoomId(123),
        content=ChatMsgContent("hello")
    )
    msg2 = ChatworkReceivedMessage(
        room_id=ChatworkRoomId(123),
        content=ChatMsgContent("latest")
    )

    fake_reader = FakeMsgReader([msg1, msg2])
    usecase = GetLatestChatMessageUseCase(fake_reader)

    req = GetNewMsgRequest(room_id=123)

    result = usecase.execute(req)

    assert fake_reader.called is True
    assert fake_reader.received_room_id.value == 123
    assert result == msg2


# ----------------------------------------------------------------------------------


def test_get_latest_chat_message_usecase_empty_list_raises():
    fake_reader = FakeMsgReader([])
    usecase = GetLatestChatMessageUseCase(fake_reader)

    req = GetNewMsgRequest(room_id=123)

    with pytest.raises(ValueError):
        usecase.execute(req)

# **********************************************************************************
