# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from pydantic import BaseModel
from .request_dto import ChatworkSendMsgDTO, ChatworkGetMsgDTO

# ----------------------------------------------------------------------------------
# **********************************************************************************


class ChatworkSendMsgPayload(BaseModel):
    body: str
    room_id: int

    @classmethod
    def from_dto(cls, dto: ChatworkSendMsgDTO):
        return cls(
            body=dto.body
        )

# **********************************************************************************


class ChatworkGetMsgPayload(BaseModel):
    room_id: int
    since: int

    @classmethod
    def from_dto(cls, dto: ChatworkGetMsgDTO):
        return cls(
            room_id=dto.room_id,
            since=dto.since
        )
        
# **********************************************************************************
