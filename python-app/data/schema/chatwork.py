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


# ----------------------------------------------------------------------------------

class ChatworkParams(BaseModel):
    endpoint_url: str = "https://api.chatwork.com/v2"
    # body: str

# ----------------------------------------------------------------------------------

class ChatworkConfig(BaseSettings):
    chatwork_api_token: str
    chatwork_my_room_id: int
    chatwork_check_room_id: int
    chatwork_endpoint_url: str = "https://api.chatwork.com/v2"
    class Config:
        env_file = ".env.chatwork"
        env_file_encoding = "utf-8"

# ----------------------------------------------------------------------------------

# **********************************************************************************


if __name__ == "__main__":
    pass

# ----------------------------------------------------------------------------------
