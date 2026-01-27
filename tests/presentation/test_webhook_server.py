# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 仕様：
# WebhookServer が /webhook/chatwork/one と /webhook/chatwork/second のルートを持ち、
# 受け取ったJSONを ChatworkClient に渡して結果を返すことを確認する。
# 確認方法: TestClient でPOSTし、返却内容が FakeChatworkClient の戻り値と一致することを assert。
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import asyncio
import importlib
import sys
import types

from pydantic import BaseModel

# ----------------------------------------------------------------------------------


class FakeLogger:
    def debug(self, *args, **kwargs):
        return None


class FakeLoggerProvider:
    def getLogger(self):
        return FakeLogger()


class FakeChatworkClient:
    def flow_one(self, data):
        return {"ok": True, "flow": "one", "data": data}

    def flow_second(self, data):
        return {"ok": True, "flow": "second", "data": data}


class FakeChatgptClient:
    pass


class StandardResponse(BaseModel):
    ok: bool
    flow: str
    data: dict


def _inject_fake_modules():
    # Create minimal module tree for missing imports
    modules = {}

    modules["src"] = types.ModuleType("src")
    modules["src.base"] = types.ModuleType("src.base")
    modules["src.base.chatwork"] = types.ModuleType("src.base.chatwork")
    modules["src.base.chatgpt"] = types.ModuleType("src.base.chatgpt")
    modules["src.utils"] = types.ModuleType("src.utils")
    modules["src.utils.logger"] = types.ModuleType("src.utils.logger")
    modules["data"] = types.ModuleType("data")
    modules["data.schema"] = types.ModuleType("data.schema")
    modules["data.schema.api_response"] = types.ModuleType("data.schema.api_response")

    modules["src.base.chatwork"].ChatworkClient = FakeChatworkClient
    modules["src.base.chatgpt"].ChatgptClient = FakeChatgptClient
    modules["src.utils.logger"].Logger = FakeLoggerProvider
    modules["data.schema.api_response"].StandardResponse = StandardResponse

    sys.modules.update(modules)


# ----------------------------------------------------------------------------------

class FakeRequest:
    def __init__(self, payload):
        self._payload = payload

    async def json(self):
        return self._payload


def test_webhook_server_routes_and_handlers():
    _inject_fake_modules()
    module = importlib.import_module("src.presentation.webhook_server")

    server = module.WebhookServer()
    routes = {route.path: route.endpoint for route in server.app.routes}

    assert "/webhook/chatwork/one" in routes
    assert "/webhook/chatwork/second" in routes

    payload = {"hello": "world"}
    req = FakeRequest(payload)

    res_one = asyncio.run(routes["/webhook/chatwork/one"](req))
    assert res_one == {"ok": True, "flow": "one", "data": payload}

    res_second = asyncio.run(routes["/webhook/chatwork/second"](req))
    assert res_second == {"ok": True, "flow": "second", "data": payload}

# **********************************************************************************
