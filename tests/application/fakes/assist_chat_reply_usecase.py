# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 仕様：
# 値をダミーで渡して流れを確認するためにFakeを定義
#* 値に関しては制約を満たすように最低限の実装のみ
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from src.domain.entities.chat.chatwork_received_message import ChatworkReceivedMessage
from src.domain.entities.llm.prompt import Prompt
from src.domain.entities.llm.response import Response
from src.domain.values.chatwork_room_id import ChatworkRoomId
from src.domain.values.chat_msg_content import ChatMsgContent
from src.domain.values.prompt_content import PromptContent
from src.domain.values.llm_response_content import LLMResponseContent

from src.domain.ports.text_generator_port import TextGeneratorPort

# ----------------------------------------------------------------------------------
# **********************************************************************************

class FakeGetLatestChatMessageUseCase:
    def __init__(self):
        self.called = False  # 処理が呼ばれたか確認
        self.received_req = None

    def execute(self, req):
        self.called = True
        self.received_req = req
        return ChatworkReceivedMessage(
            room_id=ChatworkRoomId(123),
            content=ChatMsgContent("hello")
        )
# **********************************************************************************


class FakeCreatePromptFromChatMessageUseCase:
    def __init__(self):
        self.called = False  # 処理が呼ばれたか確認
        self.received_message = None

    def execute(self, message):
        self.called = True
        self.received_message = message
        return Prompt(PromptContent("dummy prompt"))

# **********************************************************************************


class FakeRequestLlmResponseUseCase:
    def __init__(self, generator: TextGeneratorPort | None = None):
        self.generator = generator
        self.called = False  # 処理が呼ばれたか確認
        self.received_prompt = None

    def execute(self, prompt):
        self.called = True
        self.received_prompt = prompt
        if self.generator is None:
            return Response(content=LLMResponseContent("dummy response"))

        return self.generator.execute(prompt)

# **********************************************************************************


class FakeSendChatMessageUseCase:
    def __init__(self):
        self.called = False  # 処理が呼ばれたか確認
        self.received_response = None
        self.received_room_id = None

    def execute(self, response, room_id):
        self.called = True
        self.received_response = response
        self.received_room_id = room_id
        
# **********************************************************************************


class FakeTextGenerator:
    def __init__(self, response: Response):
        self.response = response
        self.called = False
        self.received_prompt = None

    def execute(self, prompt: Prompt) -> Response:
        self.called = True
        self.received_prompt = prompt
        return self.response

# **********************************************************************************
