# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 仕様：実行することを定義しているクラス
# UseCase = アプリケーションのオーケストレーションレイヤー

# 入力（DTO）を受け取る
# Domainの ValueObjectを組み立てる
# Portを呼び出す
# 結果を返す
# この 4つ だけが責務。
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from shared.logger import Logger
from src.domain.values.chatwork_room_id import RoomId
from src.domain.ports.msg_reader_port import MsgReaderPort
from src.application.dtos.get_new_msg import GetNewMsgRequest
from src.domain.entities.chat.chatwork_received_message import ReceivedChatMessage
# ----------------------------------------------------------------------------------
# **********************************************************************************


class GetLatestChatMessageUseCase:
    def __init__(self, reader: MsgReaderPort):
        # logger
        self.logger_setup = Logger()
        self.logger = self.logger_setup.getLogger()
        
        # インスタンス
        self.reader = reader

# ----------------------------------------------------------------------------------
# チャットの新着メッセージを取得する

    def execute(self, req: GetNewMsgRequest):
        
        room_id = RoomId(req.room_id)
        self.logger.debug(f"GetNewMsgRequest から RoomId を作成しました: {room_id}")
        
        # ここで値の制約チェック
        msgs: list[ReceivedChatMessage] = self.reader.execute(room_id=room_id)
        self.logger.debug(f"MsgReaderPort から メッセージリスト を取得しました: {msgs}")
        
        if not msgs:
            raise ValueError("新しいメッセージが存在しません")
        
        new_msg = msgs[-1]
        self.logger.info(f"新しいメッセージを取得しました: {new_msg}")

        return new_msg
    

# **********************************************************************************
