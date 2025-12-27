# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 仕様：

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from src.application.usecases.get_lastest_chat_message_usecase import GetLatestChatMessageUseCase
from src.application.usecases.create_prompt_from_chat_message_usecase import CreatePromptFromChatMessageUseCase
from src.application.usecases.request_llm_response_usecase import RequestLlmResponseUseCase
from src.application.usecases.send_chat_message_usecase import SendChatMessageUseCase
from src.application.dtos.get_new_msg import GetNewMsgRequest
from src.domain.values.chatwork_room_id import ChatworkRoomId
from src.shared.logger import Logger


# ----------------------------------------------------------------------------------
# **********************************************************************************


class AssistChatReplyUseCase:
    def __init__(
        self,
        get_latest_msg_uc: GetLatestChatMessageUseCase,
        create_prompt_uc: CreatePromptFromChatMessageUseCase,
        generate_response_uc: RequestLlmResponseUseCase,
        send_chat_msg_uc: SendChatMessageUseCase,
    ):
        # logger
        self.logger_setup = Logger()
        self.logger = self.logger_setup.getLogger()
        
        # インスタンス
        self.get_latest_msg_uc = get_latest_msg_uc
        self.create_prompt_uc = create_prompt_uc
        self.generate_response_uc = generate_response_uc
        self.send_chat_msg_uc = send_chat_msg_uc
        
# ----------------------------------------------------------------------------------

    def execute(self, req: GetNewMsgRequest) -> None:
        self.logger.debug("返信処理を開始")

        # ① 最新メッセージ取得
        message = self.get_latest_msg_uc.execute(req)

        # ② Prompt 作成
        prompt = self.create_prompt_uc.execute(message)

        # ③ LLM に投げる
        response = self.generate_response_uc.execute(prompt)

        # ④ Chat に送信
        self.send_chat_msg_uc.execute(
            response=response,
            room_id=message.room_id
        )

        self.logger.debug("返信処理が完了")

# **********************************************************************************