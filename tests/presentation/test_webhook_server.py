# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 仕様：
# WebhookServer が chatwork webhook を受け取り、room_id を DTO 化して
# AssistChatReplyUseCase に委譲することを確認する。
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from fastapi.testclient import TestClient

from src.presentation.webhook_server import WebhookServer

# ----------------------------------------------------------------------------------


class FakeAssistChatReplyUseCase:
    def __init__(self):
        self.called = False
        self.received_req = None
        self.should_raise = False

    def execute(self, req):
        self.called = True
        self.received_req = req
        if self.should_raise:
            raise RuntimeError("usecase error")


# ----------------------------------------------------------------------------------


def _build_client(fake_usecase: FakeAssistChatReplyUseCase) -> TestClient:
    server = WebhookServer(reply_usecase=fake_usecase)
    return TestClient(server.app)


# ----------------------------------------------------------------------------------
# テスト内容: Chatwork Webhook 用の3ルートが FastAPI に登録されていることを確認

def test_webhook_server_routes_exist():
    client = _build_client(FakeAssistChatReplyUseCase())
    route_paths = {route.path for route in client.app.routes}

    assert "/webhook/chatwork" in route_paths
    assert "/webhook/chatwork/one" in route_paths
    assert "/webhook/chatwork/second" in route_paths


# ----------------------------------------------------------------------------------
# テスト内容: room_id が直下にある payload で UseCase が実行されることを確認

def test_webhook_server_execute_success_with_room_id():
    fake_usecase = FakeAssistChatReplyUseCase()
    client = _build_client(fake_usecase)

    response = client.post("/webhook/chatwork", json={"room_id": 123})

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["room_id"] == 123
    assert fake_usecase.called is True
    assert fake_usecase.received_req.room_id == 123


# ----------------------------------------------------------------------------------
# テスト内容: webhook_event.room.id 形式でも room_id を抽出できることを確認

def test_webhook_server_execute_success_with_nested_room_id():
    fake_usecase = FakeAssistChatReplyUseCase()
    client = _build_client(fake_usecase)

    payload = {"webhook_event": {"room": {"id": "456"}}}
    response = client.post("/webhook/chatwork/one", json=payload)

    assert response.status_code == 200
    assert response.json()["room_id"] == 456
    assert fake_usecase.called is True
    assert fake_usecase.received_req.room_id == 456


# ----------------------------------------------------------------------------------
# テスト内容: Chatwork 公式に近い payload 形式で正常処理できることを確認

def test_webhook_server_execute_success_with_chatwork_official_payload():
    fake_usecase = FakeAssistChatReplyUseCase()
    client = _build_client(fake_usecase)

    payload = {
        "webhook_setting_id": "12345",
        "webhook_event_type": "mention_to_me",
        "webhook_event_time": 1498028130,
        "webhook_event": {
            "from_account_id": 123456,
            "to_account_id": 1484814,
            "room_id": 567890123,
            "message_id": "789012345",
            "body": "[To:1484814]おかずはなんですか？",
            "send_time": 1498028125,
            "update_time": 0,
        },
    }
    response = client.post("/webhook/chatwork", json=payload)

    assert response.status_code == 200
    assert response.json()["room_id"] == 567890123
    assert fake_usecase.called is True
    assert fake_usecase.received_req.room_id == 567890123


# ----------------------------------------------------------------------------------
# テスト内容: 最初の候補が不正でも後続候補から room_id を取得できることを確認

def test_webhook_server_execute_success_with_fallback_room_id_source():
    fake_usecase = FakeAssistChatReplyUseCase()
    client = _build_client(fake_usecase)

    payload = {
        "room_id": "invalid",
        "webhook_event": {"room_id": "789"},
    }
    response = client.post("/webhook/chatwork", json=payload)

    assert response.status_code == 200
    assert response.json()["room_id"] == 789
    assert fake_usecase.called is True
    assert fake_usecase.received_req.room_id == 789


# ----------------------------------------------------------------------------------
# テスト内容: room_id が存在しない場合は 400 を返して UseCase を呼ばないことを確認

def test_webhook_server_bad_request_when_room_id_missing():
    fake_usecase = FakeAssistChatReplyUseCase()
    client = _build_client(fake_usecase)

    response = client.post("/webhook/chatwork/second", json={"message": "x"})

    assert response.status_code == 400
    assert "room_id" in response.json()["detail"]
    assert fake_usecase.called is False


# ----------------------------------------------------------------------------------
# テスト内容: room_id が 0 の場合は 400 を返して UseCase を呼ばないことを確認

def test_webhook_server_bad_request_when_room_id_is_zero():
    fake_usecase = FakeAssistChatReplyUseCase()
    client = _build_client(fake_usecase)

    response = client.post("/webhook/chatwork", json={"room_id": 0})

    assert response.status_code == 400
    assert "room_id" in response.json()["detail"]
    assert fake_usecase.called is False


# ----------------------------------------------------------------------------------
# テスト内容: room_id が数値に変換できない場合は 400 を返すことを確認

def test_webhook_server_bad_request_when_room_id_is_not_number():
    fake_usecase = FakeAssistChatReplyUseCase()
    client = _build_client(fake_usecase)

    response = client.post("/webhook/chatwork", json={"room_id": "abc"})

    assert response.status_code == 400
    assert "room_id" in response.json()["detail"]
    assert fake_usecase.called is False


# ----------------------------------------------------------------------------------
# テスト内容: UseCase 側で例外が起きた場合に 500 を返すことを確認

def test_webhook_server_internal_error_when_usecase_failed():
    fake_usecase = FakeAssistChatReplyUseCase()
    fake_usecase.should_raise = True
    client = _build_client(fake_usecase)

    response = client.post("/webhook/chatwork", json={"room_id": 123})

    assert response.status_code == 500
    assert response.json()["detail"] == "返信処理でエラーが発生しました"

# **********************************************************************************
