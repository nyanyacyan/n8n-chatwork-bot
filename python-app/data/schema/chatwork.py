# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from enum import Enum
from pydantic import BaseModel
from pydantic_settings import BaseSettings
# flow


# ----------------------------------------------------------------------------------
# **********************************************************************************

class ChatworkEventType(str, Enum):
    nomal = "normal"
    system = "system"

# ----------------------------------------------------------------------------------

class ChatworkParams(BaseModel):
    endpoint_url: str = "https://api.chatwork.com/v2"
    body: str
    event_type: ChatworkEventType

# ----------------------------------------------------------------------------------

class ChatworkConfig(BaseSettings):
    chatwork_api_token: str
    my_room_id: int
    check_room_id: int
    endpoint_url: str = "https://api.chatwork.com/v2"
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# ----------------------------------------------------------------------------------

# **********************************************************************************


if __name__ == "__main__":
    pass

# ----------------------------------------------------------------------------------
