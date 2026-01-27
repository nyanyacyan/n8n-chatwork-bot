# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# app.py は「DI と 起動」だけを行う
# 「起動時（app.py）に、依存関係を全部組み立ててから渡している」
# これが DI が明確 という状態です。


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from src.shared.logger import Logger

# -----------------------
# Infrastructure (Config)
# -----------------------
from src.infrastructure.chatwork.config import ChatworkConfig
from src.infrastructure.chatgpt.config import ChatgptConfig

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
from src.application.usecases.request_llm_response_usecase import RequestLlmResponseUseCase
from src.application.usecases.send_chat_message_usecase import SendChatMessageUseCase

# Orchestration
from src.application.usecases.assist_chat_reply_usecase import AssistChatReplyUseCase


# ----------------------------------------------------------------------------------
# **********************************************************************************

# -----------------------
# 起動
# -----------------------
def main():
    try:
        logger_setup = Logger()
        logger = logger_setup.getLogger()

        # =====================
        # 0. Config 作成
        # =====================
        chatwork_config = ChatworkConfig()
        chatgpt_config = ChatgptConfig()

        # =====================
        # 1. Client 作成
        # =====================
        chatwork_client = ChatWorkClient(chatwork_config)
        chatgpt_client = OpenAIClient(chatgpt_config)

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
        generate_reply_uc = RequestLlmResponseUseCase(text_generator)
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

    except Exception as e:
        logger.error(f"予期せぬエラーが発生しました: {e}")
        raise e

# **********************************************************************************

if __name__ == "__main__":
    main()

# ----------------------------------------------------------------------------------



