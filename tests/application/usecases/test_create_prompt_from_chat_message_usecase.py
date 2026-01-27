# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 仕様：
# CreatePromptFromChatMessageUseCase が OutgoingMessage から Prompt を生成し、
# Prompt の内容が空でないことを確認する。
# 確認方法: execute の戻り値が Prompt 型であることと content.value が空でないことを assert。
# 検証の順序 > 型チェック > Noneチェック > 値チェック
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from src.application.usecases.create_prompt_from_chat_message_usecase import CreatePromptFromChatMessageUseCase
from src.domain.entities.chat.outgoing_message import OutgoingMessage
from src.domain.values.chat_msg_content import ChatMsgContent
from src.domain.values.chatwork_room_id import ChatworkRoomId
from src.domain.entities.llm.prompt import Prompt

# ----------------------------------------------------------------------------------


def test_create_prompt_from_chat_message_usecase_success():
    # --------------------
    # Arrange
    # --------------------
    usecase = CreatePromptFromChatMessageUseCase()

    msg = OutgoingMessage(
        room_id=ChatworkRoomId(123),
        content=ChatMsgContent("こんにちは"),
    )

    # --------------------
    # 実施
    # --------------------
    prompt = usecase.execute(msg)

    # --------------------
    # Assert
    # --------------------
    assert isinstance(prompt, Prompt)
    assert prompt.content.value  # 空でないこと（中身の詳細は見ない）

# **********************************************************************************
