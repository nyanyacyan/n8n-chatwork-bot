# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from enum import Enum
from pydantic import BaseModel, BaseSettings

# flow


# ----------------------------------------------------------------------------------
# **********************************************************************************

class ChatworkEventType(str, Enum):
    nomal = "normal"
    system = "system"

# ----------------------------------------------------------------------------------

class ChatworkValue(BaseModel):
    room_id: int
    message_id: int
    body: str
    event_type: ChatworkEventType


# ----------------------------------------------------------------------------------

class ChatworkConfig(BaseSettings):
    chatwork_api_token: str
    base_url: str = "https://api.chatwork.com/v2"

    class Config:
        # envファイルの中から検索する
        env_file = ".env"
        env_file_encoding = "utf-8"
    
#! 呼び出し方法
# chatwork_config = ChatworkConfig()
# chatwork_config.chatwork_api_token

# **********************************************************************************


if __name__ == "__main__":
    pass

# ----------------------------------------------------------------------------------
