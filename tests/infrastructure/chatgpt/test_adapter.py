# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 仕様：
# ChatGPTTextGeneratorAdapter が Prompt の内容を client.generate_text に渡し、
# 戻り値を ReplyContent → Response に包んで返すことを確認する。
# 確認方法: Fake client の受け取り引数と、戻り値の型・値を assert。
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import

from src.infrastructure.chatgpt.adapter import ChatGPTTextGeneratorAdapter
from src.domain.entities.llm.prompt import Prompt
from src.domain.values.prompt_content import PromptContent
from src.domain.entities.llm.response import Response
from src.domain.values.reply_content import ReplyContent

# ----------------------------------------------------------------------------------


class FakeOpenAIClient:
    def __init__(self, response_text: str):
        self.response_text = response_text
        self.called = False
        self.received_prompt = None

    def generate_text(self, prompt: str):
        self.called = True
        self.received_prompt = prompt
        return self.response_text


# ----------------------------------------------------------------------------------


def test_chatgpt_text_generator_adapter_success():
    fake_client = FakeOpenAIClient("dummy reply")
    adapter = ChatGPTTextGeneratorAdapter(fake_client)

    prompt = Prompt(PromptContent("hello prompt"))

    result = adapter.execute(prompt)

    assert fake_client.called is True
    assert fake_client.received_prompt == "hello prompt"
    assert isinstance(result, Response)
    assert isinstance(result.content, ReplyContent)
    assert result.content.value == "dummy reply"

# **********************************************************************************
