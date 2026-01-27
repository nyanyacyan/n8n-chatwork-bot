# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# リクエストする際のDTOを定義
#! ここではEnumは定義NG

#! 下記の定義以外は記述しない
# 例）
# class CreateMessageDTO(BaseModel):
#     text: str

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from pydantic_settings import BaseSettings, SettingsConfigDict

#
# ----------------------------------------------------------------------------------
# **********************************************************************************


class ChatworkConfig(BaseSettings):
    chatwork_api_token: str
    chatwork_endpoint_url: str = "https://api.chatwork.com/v2"
    chatwork_send_room_id: int
    chatwork_reception_room_id: int
    
    model_config = SettingsConfigDict(
        env_file=".env.chatwork",
        env_file_encoding="utf-8",
    )

# ----------------------------------------------------------------------------------
# **********************************************************************************
