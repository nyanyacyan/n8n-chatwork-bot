# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 仕様：Promptの値の制限をもたせる

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from dataclasses import dataclass


# ----------------------------------------------------------------------------------
# **********************************************************************************

@dataclass(frozen=True)
class ChatMsgContent:
    value: str

    MAX_LENGTH = 2000

    # 不正な値を除外
    def __post_init__(self):
        if not isinstance(self.value, str):
            raise ValueError("文字列ではありません")
        
        if not self.value.strip():
            raise ValueError("Messageが空です")

        if len(self.value) > self.MAX_LENGTH:
            raise ValueError(f"Messageは{self.MAX_LENGTH}文字以内にしてください")
    
    def length(self) -> int:
        return len(self.value)

# **********************************************************************************
