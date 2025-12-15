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

    def send_message(self, room_id: int, msg_content: str) -> dict:
        url = f"{self.base_url}/rooms/{room_id}/messages"
        response = requests.post(
            url,
            headers=self.headers,
            data={"body": msg_content}
        )
        response.raise_for_status()
        return response.json()

# ----------------------------------------------------------------------------------
# すべてのmsg取得

    def get_messages(self, room_id: int):
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
