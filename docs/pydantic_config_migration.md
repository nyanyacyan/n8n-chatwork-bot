# Pydantic 設定の書き方（やさしい説明）

このドキュメントは、Pydantic v2 での「設定の書き方」をまとめたものです。
小学生でもわかるように説明します。

---

## 1. なにが起きたの？

Pydantic では、昔の書き方（`class Config`）が「古いやり方」になりました。
そのため、テストをすると **「その書き方はもうすぐ使えなくなるよ」** という警告が出ます。

---

## 2. なぜ直すの？

今は動くけど、将来のPydanticでは動かなくなるからです。
だから **先に新しい書き方に直しておく** と安心です。

---

## 3. どう直すの？

### 古い書き方（もうすぐ使えなくなる）
```
class ChatgptConfig(BaseSettings):
    ...

    class Config:
        env_file = ".env.chatgpt"
        env_file_encoding = "utf-8"
```

### 新しい書き方（これからの正しい形）
```
from pydantic_settings import BaseSettings, SettingsConfigDict

class ChatgptConfig(BaseSettings):
    ...

    model_config = SettingsConfigDict(
        env_file=".env.chatgpt",
        env_file_encoding="utf-8",
    )
```

---

## 4. ざっくり言うと

- **昔**：箱の中に「設定の箱（Config）」を入れてた
- **今**：箱の横に「ラベル（model_config）」を貼る

同じ意味だけど、新しい方がルールに合っています。

---

## 5. このプロジェクトで直した場所

- `src/infrastructure/chatgpt/config.py`
- `src/infrastructure/chatwork/config.py`

どちらも **新しい書き方に変更** しました。
