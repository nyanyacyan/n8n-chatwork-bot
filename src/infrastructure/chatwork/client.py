# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# Adapterファイル作成

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import requests
from infrastructure.chatwork.config import ChatworkConfig

# ----------------------------------------------------------------------------------
# **********************************************************************************


class ChatWorkClient:
    def __init__(self, config: ChatworkConfig):
        self.api_key = config.chatwork_api_token
        self.base_url = config.chatwork_endpoint_url
        
        self.headers = {
            "X-ChatWorkToken": self.api_key,
        }

# ----------------------------------------------------------------------------------
# msg送信

    def send_message(self, room_id: int, text: str) -> dict:
        url = f"{self.base_url}/rooms/{room_id}/messages"
        response = requests.post(
            url,
            headers=self.headers,
            data={"body": text}
        )
        response.raise_for_status()
        return response.json()

# ----------------------------------------------------------------------------------
# 最新のmsgを取得

    def get_new_msg(self, room_id: int, since: int) -> dict:
        url = f"{self.base_url}/rooms/{room_id}/messages"
        response = requests.get(
            url,
            headers=self.headers,
            params={"force": 1}
        )
        response.raise_for_status()
        return response.json()

# ----------------------------------------------------------------------------------


# **********************************************************************************




    
# **********************************************************************************
