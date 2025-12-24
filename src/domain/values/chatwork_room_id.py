# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 仕様：
# ValueObjectは基本、値の変更はNG → ValueObjectの原則に一致 → frozen=True
# 値が入ってきたときに全く空のの値もNGにするために、__post_init__でバリデーションを実施

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from dataclasses import dataclass


# ----------------------------------------------------------------------------------
# **********************************************************************************


@dataclass(frozen=True)
class ChatworkRoomId:
    value: int

    # 不正な値を除外
    def __post_init__(self):
        # Noneチェック
        if not self.value:
            raise ValueError("値が送信先の指定がありません")

        # 型チェック（ここが重要）
        if not isinstance(self.value, int):
            raise ValueError("room_idは整数型である必要があります")
        
        # 0以下の値はNG
        if self.value <= 0:
            raise ValueError("room_idは1以上の整数である必要があります")
        
# **********************************************************************************
