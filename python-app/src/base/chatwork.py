# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))


# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import requests
from typing import Dict

from src.utils.logger import Logger
from src.utils.read_config import ReadConfig
from data.schema.chatwork import ChatworkConfig, ChatworkParams

# flow

# ----------------------------------------------------------------------------------
# **********************************************************************************
# ChatWork API から “最新のメッセージ” を取得

class ChatworkClient:
    def __init__(self):
        # logger
        self.getLogger = Logger()
        self.logger = self.getLogger.getLogger()
        
        # 値マスククラス
        self.mask = ReadConfig()
        
        # インスタンス
        self.chatwork_config = ChatworkConfig()
        self.chatwork_value = ChatworkParams()
        self.api_token = self._get_api_token()
        self.headers = self._build_headers()

# ----------------------------------------------------------------------------------
# 新しいメッセージを取得するメソッド

    def get_new_message_text(self, check_message_id: int):
        message_data = self._get_new_message_data(check_message_id)
        if message_data and "messages" in message_data:
            messages = message_data["messages"]
            if messages:
                latest_message = messages[-1]  #* 取得するmsg数を調整→最新のみ取得
                message_body = latest_message.get("body", "")
                self.logger.debug(f"最新メッセージ取得: {message_body}")
                return message_body
        self.logger.debug("新しいメッセージがありません。")
        return None

# ----------------------------------------------------------------------------------
# メッセージデータを取得するメソッド

    def _get_new_message_data(self, check_message_id: int):
        request_url = self._get_request_url(check_message_id=check_message_id)
        params = self._get_params(check_message_id=check_message_id)
        response = requests.get(request_url, headers=self.headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            self.logger.error(f"ChatWork APIエラー: {response.status_code} - {response.text}")
            return None

# ----------------------------------------------------------------------------------
# ヘッダーを構築するメソッド

    def _build_headers(self):
        headers = {
            "X-ChatWorkToken": self.api_token,
        }
        return headers

# ----------------------------------------------------------------------------------
# APIトークンを取得するメソッド

    def _get_api_token(self):
        api_token = self.chatwork_config.chatwork_api_token
        mask_value = self.mask.mask_value(value=api_token)
        self.logger.debug(f"ChatWork APIトークン取得: {mask_value}")
        return api_token

# ----------------------------------------------------------------------------------
# リクエストするURLを取得するメソッド

    def _get_request_url(self, check_message_id: int):
        url = f"{self.chatwork_value.endpoint_url}/rooms/{check_message_id}/messages"
        mask_url = self.mask.mask_value(value=url)
        self.logger.debug(f"ChatWork リクエストURL取得: {mask_url}")
        return url

# ----------------------------------------------------------------------------------
# リクエストパラメータを取得するメソッド
# force=1 → 未取得のメッセージがなくても強制的に最新メッセージ一覧を返す（常に全件返す）

    def _get_params(self, check_message_id: int):
        params = {
            "force": 1,
            "since": check_message_id
        }
        mask_params = self.mask.mask_value(value=params)
        self.logger.debug(f"ChatWork リクエストパラメータ取得: {mask_params}")
        return params

# ----------------------------------------------------------------------------------
# マイチャットにメッセージを送信するメソッド


    def send_message_to_my_chat(self, my_room_id: int, message: str):
        request_url = self._get_request_url(check_message_id=my_room_id)
        payload = {
            "body": message
        }
        response = requests.post(request_url, headers=self.headers, data=payload)
        if response.status_code == 200 or response.status_code == 204:
            self.logger.info("メッセージをマイチャットに送信しました。")
        else:
            self.logger.error(f"ChatWork メッセージ送信エラー: {response.status_code} - {response.text}")


# **********************************************************************************

class ChatworkWebhookClient(ChatworkClient):
    def __init__(self):
        # logger
        self.getLogger = Logger()
        self.logger = self.getLogger.getLogger()
        
        # 値マスククラス
        self.mask = ReadConfig()
        
        # インスタンス
        self.chatwork_config = ChatworkConfig()
        self.chatwork_value = ChatworkParams()
        self.chatwork_client = ChatworkClient()
        self.api_token = self._get_api_token()
        self.headers = self._build_headers()
        

# ----------------------------------------------------------------------------------
# Webhookデータを処理するフローメソッド①

    def webhook_flow(self, data: dict):
        self.logger.info("ChatWork Webhook フローを開始します。")
        
        target_room_id = self._get_target_room_id(data=data)
        
        if not target_room_id:
            self.logger.warning("Webhook データにルームIDが含まれていません。処理を終了します。")
            return
        
        check_room_new_text = self.chatwork_client.get_new_message_text(check_message_id=target_room_id)
        
        # 対象のルームにメッセージがあるか確認
        if check_room_new_text:
            self.logger.info(f"新しいメッセージを検出しました: {check_room_new_text}")
            
            # プロンプト生成
            
            # ChatGPTへのリクエスト
            
            # ChatGPTからのレスポンス整理
            
            # マイチャットへ送信
            my_room_id = self.chatwork_config.chatwork_my_room_id
            self.chatwork_client.send_message_to_my_chat(
                my_room_id=my_room_id,
                message=check_room_new_text
            )
            
        else:
            self.logger.info("新しいメッセージはありません。")

# ----------------------------------------------------------------------------------
# ルームIDを取得するメソッド

    def _get_target_room_id(self, data: Dict):
        try:
            self.logger.debug("Webhook データからルームIDを取得します。")
            target_room_id_value = self.chatwork_config.chatwork_my_room_id
            target_room_id = data.get(target_room_id_value)
            self.logger.debug(f"取得したルームID: {target_room_id}")
            return target_room_id
        
        except Exception as e:
            self.logger.error(f"ルームIDの取得中にエラーが発生しました: {e}")
            return None

# ----------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------
# **********************************************************************************

if __name__ == "__main__":
    instance = ChatworkClient()
    config = ChatworkConfig()
    my_room_id = config.chatwork_my_room_id
    print(f"My Room ID: {my_room_id}")
    
    instance.send_message_to_my_chat(my_room_id=my_room_id, message="テストメッセージです。")
    print("メッセージ送信完了")
# ----------------------------------------------------------------------------------
