# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# リクエストする際のDTOを定義
#! ここではEnumは定義NG

#! 下記の定義以外は記述しない
# 例）
# class CreateMessageDTO(BaseModel):
#     text: str

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from enum import Enum
from pydantic import BaseModel

# ----------------------------------------------------------------------------------

from .model_enum import ChatgptModel


# ----------------------------------------------------------------------------------
# **********************************************************************************
# モデル

class ChatgptRequestValue(BaseModel):
    model: ChatgptModel = ChatgptModel.standard  # デフォルトモデル
    
    success_attribute: str = "choices"
    is_error: bool = False
    
    retry_prompt: str = "ただしくレスポンスが取得できませんでした。下記の再度回答をお願いします。"
    
    max_retries: int = 3  # 最大リトライ回数
    retry_delay: float = 1.0  # 初期リトライ遅延（秒）
    backoff_factor: float = 2.0  # バックオフ係数