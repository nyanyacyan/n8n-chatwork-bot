# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 仕様：
# ChatworkSendMsgAdapter が SendMessage の値を client.send_message に渡すこと、
# ChatworkGetMessagesAdapter が client.get_messages の結果を ChatworkReceivedMessage に変換することを確認する。
# 確認方法: Fake client の受け取り値と、戻り値の型・中身を assert。
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import

from src.infrastructure.chatwork.chatwork_adapter import ChatworkSendMsgAdapter, ChatworkGetMessagesAdapter
from src.domain.entities.chat.send_message import SendMessage
from src.domain.values.chatwork_room_id import ChatworkRoomId
from src.domain.values.chat_msg_content import ChatMsgContent
from src.domain.entities.chat.chatwork_received_message import ChatworkReceivedMessage

# ----------------------------------------------------------------------------------


class FakeChatWorkClient:
    def __init__(self, get_messages_response=None):
        self.get_messages_response = get_messages_response or []
        self.send_called = False
        self.send_room_id = None
        self.send_msg_content = None
        self.get_called = False
        self.get_room_id = None

    def send_message(self, room_id: int, msg_content: str):
        self.send_called = True
        self.send_room_id = room_id
        self.send_msg_content = msg_content
        return {"message_id": "dummy"}

    def get_messages(self, room_id: int):
        self.get_called = True
        self.get_room_id = room_id
        return self.get_messages_response


# ----------------------------------------------------------------------------------


def test_chatwork_send_msg_adapter_success():
    fake_client = FakeChatWorkClient()
    adapter = ChatworkSendMsgAdapter(fake_client)

    msg = SendMessage(
        room_id=ChatworkRoomId(123),
        content=ChatMsgContent("hello")
    )

    adapter.execute(msg)

    assert fake_client.send_called is True
    assert fake_client.send_room_id == 123
    assert fake_client.send_msg_content == "hello"


# ----------------------------------------------------------------------------------


def test_chatwork_get_messages_adapter_success():
    fake_client = FakeChatWorkClient(
        get_messages_response=[
            {"body": "first"},
            {"body": "second"},
        ]
    )
    adapter = ChatworkGetMessagesAdapter(fake_client)

    room_id = ChatworkRoomId(456)
    result = adapter.execute(room_id)

    assert fake_client.get_called is True
    assert fake_client.get_room_id == 456
    assert isinstance(result, list)
    assert len(result) == 2
    assert all(isinstance(m, ChatworkReceivedMessage) for m in result)
    assert result[0].content.value == "first"
    assert result[1].content.value == "second"
    assert result[0].room_id == room_id

# **********************************************************************************
