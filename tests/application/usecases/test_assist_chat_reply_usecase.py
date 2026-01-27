# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 仕様：
# AssistChatReplyUseCase が 取得→Prompt化→LLM→送信 の順に実行され、
# 各 UseCase が呼ばれ、受け渡しの room_id が一致することを確認する。
# 確認方法: Fake 各種の called フラグと受け渡し値を assert。
# 検証の順序 > 型チェック > Noneチェック > 値チェック
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from src.application.usecases.assist_chat_reply_usecase import AssistChatReplyUseCase
from src.application.dtos.get_new_msg import GetNewMsgRequest

from tests.application.fakes.assist_chat_reply_usecase import (
    FakeGetLatestChatMessageUseCase,
    FakeCreatePromptFromChatMessageUseCase,
    FakeRequestLlmResponseUseCase,
    FakeSendChatMessageUseCase,
)

# ----------------------------------------------------------------------------------


def test_assist_chat_reply_usecase_flow_success():
    # --------------------
    # Arrange（準備）
    # --------------------
    fake_get_latest = FakeGetLatestChatMessageUseCase()
    fake_create_prompt = FakeCreatePromptFromChatMessageUseCase()
    fake_generate_response = FakeRequestLlmResponseUseCase()
    fake_send_chat = FakeSendChatMessageUseCase()

    usecase = AssistChatReplyUseCase(
        get_latest_msg_uc=fake_get_latest,
        create_prompt_uc=fake_create_prompt,
        generate_response_uc=fake_generate_response,
        send_chat_msg_uc=fake_send_chat,
    )

    req = GetNewMsgRequest(room_id=123)

    # --------------------
    # Act（実行）
    # --------------------
    usecase.execute(req)

    # --------------------
    # Assert（検証）
    # --------------------
    assert fake_get_latest.called is True
    assert fake_create_prompt.called is True
    assert fake_generate_response.called is True
    assert fake_send_chat.called is True

    # 受け渡しの検証（Flow の核心）
    assert fake_create_prompt.received_message.room_id.value == 123
    assert fake_send_chat.received_room_id.value == 123


# ----------------------------------------------------------------------------------
# **********************************************************************************

