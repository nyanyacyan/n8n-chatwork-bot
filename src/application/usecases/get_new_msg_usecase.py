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
from domain.values.room_id import RoomId
from src.domain.ports.msg_reader_port import MsgReaderPort
from src.application.dtos.get_new_msg import GetNewMsgRequest

# ----------------------------------------------------------------------------------
# **********************************************************************************


class GetNewMsgUseCase:
    def __init__(self, reader: MsgReaderPort):
        self.reader = reader
        
        
    def execute(self, dto: GetNewMsgRequest):
        room_id = RoomId(dto.room_id)
        return self.reader.get_new_msg(room_id)
    

# **********************************************************************************
