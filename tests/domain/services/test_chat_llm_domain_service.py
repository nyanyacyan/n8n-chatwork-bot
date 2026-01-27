
# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 仕様：
# ChatLlmDomainService の create_prompt と can_reply の挙動を確認する。
# create_prompt は Prompt を返すこと、can_reply は長さ>0で True になることを検証。
# 確認方法: 生成した型と真偽値を assert。
# 正常系のみでOK
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import

from src.domain.entities.llm.response import Response
from src.domain.values.llm_response_content import LLMResponseContent
from src.domain.services.chat_llm_domain_service import ChatLlmDomainService
from src.domain.entities.chat.chatwork_received_message import ChatworkRoomId
from src.domain.entities.llm.prompt import Prompt
from src.domain.entities.chat.send_message import SendMessage
from src.domain.values.chat_msg_content import ChatMsgContent

# ----------------------------------------------------------------------------------


def test_create_prompt_success():
    room_id = ChatworkRoomId(123)
    content = ChatMsgContent("hello")
    outgoing = SendMessage(room_id=room_id, content=content)

    prompt = ChatLlmDomainService.create_prompt(outgoing)

    assert isinstance(prompt, Prompt)

# ----------------------------------------------------------------------------------


def test_can_reply_true():
    response = Response(LLMResponseContent("ok"))
    assert ChatLlmDomainService.can_reply(response) is True


# **********************************************************************************
