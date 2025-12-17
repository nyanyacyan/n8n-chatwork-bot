# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# app.py は「DI と 起動」だけを行う
# 「起動時（app.py）に、依存関係を全部組み立ててから渡している」
# これが DI が明確 という状態です。


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
# -----------------------
# Infrastructure (Client)
# -----------------------
from src.infrastructure.chatwork.client import ChatWorkClient
from src.infrastructure.chatgpt.client import OpenAIClient

# -----------------------
# Infrastructure (Adapter)
# -----------------------
from src.infrastructure.chatwork.adapter import (
    ChatworkGetMessagesAdapter,
    ChatworkSendMsgAdapter,
)
from src.infrastructure.chatgpt.adapter import ChatGPTTextGeneratorAdapter

# -----------------------
# Application (UseCases)
# -----------------------
from src.application.usecases.get_lastest_chat_message_usecase import GetLatestChatMessageUseCase
from src.application.usecases.create_prompt_from_chat_message_usecase import CreatePromptFromChatMessageUseCase
from src.application.usecases.generate_response_from_prompt_usecase import GenerateResponseFromPromptUseCase
from src.application.usecases.send_chat_message_usecase import SendChatMessageUseCase

# Orchestration
from application.usecases.assist_chat_reply_usecase import AssistChatReplyUseCase


# ----------------------------------------------------------------------------------
# **********************************************************************************

# -----------------------
# 起動
# -----------------------
def main():
    # =====================
    # 1. Client 作成
    # =====================
    chatwork_client = ChatWorkClient()
    chatgpt_client = OpenAIClient()

    # =====================
    # 2. Adapter 作成
    # =====================
    msg_reader = ChatworkGetMessagesAdapter(chatwork_client)
    msg_sender = ChatworkSendMsgAdapter(chatwork_client)
    text_generator = ChatGPTTextGeneratorAdapter(chatgpt_client)

    # =====================
    # 3. UseCase 作成（小）
    # =====================
    get_latest_msg_uc = GetLatestChatMessageUseCase(msg_reader)
    create_prompt_uc = CreatePromptFromChatMessageUseCase()
    generate_reply_uc = GenerateResponseFromPromptUseCase(text_generator)
    send_reply_uc = SendChatMessageUseCase(msg_sender)

    # =====================
    # 4. Orchestration UseCase
    # =====================
    reply_uc = AssistChatReplyUseCase(
        get_latest_msg_uc,
        create_prompt_uc,
        generate_reply_uc,
        send_reply_uc,
    )

    # =====================
    # 5. 実行
    # =====================
    reply_uc.execute()

# **********************************************************************************

if __name__ == "__main__":
    main()

# ----------------------------------------------------------------------------------




