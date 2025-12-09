# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# Adapterファイル作成

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from pydantic import BaseModel
from infrastructure.chatwork.payload import ChatworkSendMsgPayload, ChatworkGetMsgPayload
from infrastructure.chatwork.request_dto import ChatworkSendMsgDTO, ChatworkGetMsgDTO
from data.domain.interfaces.chatwork_client import ChatworkSendMsgClient, ChatworkGetMsgClient

# ----------------------------------------------------------------------------------
# **********************************************************************************


class ChatworkSendMsgAdapter:
    def __init__(self, client: ChatworkSendMsgClient):
        self.client = client
        
    def execute(self, dto: ChatworkSendMsgDTO) -> None:
        # DTOからPayloadへ変換
        payload = ChatworkSendMsgPayload.from_dto(dto)
        
        # ここでClientで定義する内容を定義
        return self.client.send_msg(payload=payload)

# **********************************************************************************


class ChatworkGetMsgAdapter:
    def __init__(self, client: ChatworkGetMsgClient):
        self.client = client
        
    def execute(self, dto: ChatworkGetMsgDTO) -> None:
        # DTOからPayloadへ変換
        payload = ChatworkGetMsgPayload.from_dto(dto)
        
        # ここでClientで定義する内容を定義
        return self.client.get_new_msg(payload=payload) 
    
# **********************************************************************************
