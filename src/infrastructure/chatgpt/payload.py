# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# DTOからpayloadへ変換する際のモデルを定義

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from pydantic import BaseModel
from .request_dto import ChatgptRequestDTO


# ----------------------------------------------------------------------------------
# **********************************************************************************


class ChatGptPayload(BaseModel):
    model: str
    prompt: str

    @classmethod
    def from_dto(cls, dto: ChatgptRequestDTO):
        return cls(
            model=dto.model,
            prompt=dto.prompt,
        )

# **********************************************************************************
