# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 仕様：
# 検証の順序 > 型チェック > Noneチェック > 値チェック
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
# Fake
from tests.application.fakes.assist_chat_reply_usecase import FakeRequestLlmResponseUseCase, FakeTextGenerator

from src.domain.entities.llm.prompt import Prompt
from src.domain.entities.llm.response import Response
from src.domain.values.prompt_content import PromptContent
from src.domain.values.llm_response_content import LLMResponseContent

# ----------------------------------------------------------------------------------


def test_request_llm_response_usecase_success():
    # --------------------
    # Arrange
    # --------------------
    prompt = Prompt(
        content=PromptContent("dummy prompt")
    )

    expected_response = Response(
        content=LLMResponseContent("dummy response")
    )

    fake_generator = FakeTextGenerator(expected_response)
    usecase = FakeRequestLlmResponseUseCase(fake_generator)

    # --------------------
    # Act
    # --------------------
    result = usecase.execute(prompt)

    # --------------------
    # Assert
    # --------------------
    assert fake_generator.called is True
    assert fake_generator.received_prompt == prompt
    assert result == expected_response

# **********************************************************************************