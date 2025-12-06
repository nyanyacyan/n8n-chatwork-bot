# Domain Layer & Model Design (Clean Architecture)

このドキュメントは **Clean Architecture** における **Domain Layer** の役割と、
各レイヤーで扱う「型（Types）」の考え方をまとめたものです。
ValueObject・Domain Model・DTO・Schema・Payload の違いを理解できれば、
設計品質が大幅に向上します。

---

# 🏛 Clean Architecture 全体構造

Clean Architecture は「中心＝ビジネスルール」を守る設計です。

外向き：
Infrastructure → Presentation → Application → **Domain（中心）**

内側：
**Domain** は外部仕様（DB/HTTP/API）を知らず、
「意味のあるデータ」と「不変条件（Invariant）」だけを扱います。

---

# 📌 各レイヤーの責務（重要）

## 🟣 Domain Layer（中心）

### 役割
- ビジネスルールの表現
- 意味のあるデータ（ValueObject）
- 不変条件（Invariant）保証
- 抽象（Interface）で外部依存を遮断

### 含むもの
- Entity（意味のある対象）
- ValueObject（意味と制約）
- Domain Error（正しくない状態の拒否）
- Interface（「必要な能力」の抽象）

### 含まないもの（禁止）
× HTTP用のSchema  
× JSON  
× Payload  
× DBモデル  
× Config  
× API呼出  
× 外部情報

> Domainは「正しい状態しか存在できない世界」

---

## 🟡 Application Layer（UseCase）

### 役割
- Domain Modelに仕事を依頼する
- 処理フロー（UseCase）
- DTOで境界を渡す
- Domain Errorを受け取り変換する

### 含むもの
- UseCase（行動の定義）
- DTO（データ転送オブジェクト）

### 含まないもの
× HTTP Schema  
× Payload  
× DBアクセス  

---

## 🔵 Presentation Layer（Web / FastAPI）

### 役割
- 外部からの入口（HTTP/Request）
- バリデーション（Schema）
- DTOへの変換
- Domain ErrorをUIに変換

### 含むもの
- Schema（外向けの型）
- Controller（HTTPハンドラ）

> Schemaは **HTTP仕様** を表す “外向きの約束”

---

## 🔴 Infrastructure Layer（外部I/O）

### 役割
- 外部API呼び出し
- DBアクセス
- Payload変換
- Retry/Timeout

### 含むもの
- API Client
- Payload
- Repository実装

> Payloadは **外部APIが要求するフォーマット**

---

# 🎯 型の役割（Domain / DTO / Schema / Payload）

## ① Domain Model（ValueObject）

**意味のあるデータ＋ルール**

例：
```
class Message:
    def __init__(self, text: str):
        cleaned = text.strip()
        if not cleaned:
            raise EmptyMessageError()
        if len(cleaned) > 100:
            raise TooLongMessageError()
        self.value = cleaned
```

特徴：
- 空文字禁止
- trim済み
- 最大長保証
- “これは意味のあるメッセージ”という保証

→ アプリ内を「普通の文字列」が流れなくなる。

---

## ② DTO（Application層）

**層を渡るための箱**

役割：
- Schema（HTTP世界）→ DTO → Domain（意味の世界）

例：
```
class CreateMessageDTO(BaseModel):
    text: str
```

注意：
- DTOは外部仕様を吸収し、Domainを守る「変換点」

---

## ③ Schema（Presentation）

**HTTP仕様（外向けの型）**

例：
```
class MessageRequest(BaseModel):
    text: Annotated[str, Field(..., max_length=300)]
```

目的：
- ユーザーから受け取る形
- HTTP 400 / 422などのエラー変換

> DomainはHTTPを知らない  
> Schemaはビジネスルールを知らない

---

## ④ Payload（Infrastructure）

**外部API用の形式**

例：
```
{
  "model": "gpt-4",
  "messages": [...]
}
```

特徴：
- Domain Modelとは無関係
- APIが求める仕様に合わせる
- 仕様変更はここだけで対応可能

---

# 🔥 例外処理の考え方

## Domainは「不正状態を拒否する」という責務

- Domain Model生成時に例外を投げる
- 不正値を存在させない
- エラー種別がビジネスルールを表現

例：
```
class EmptyMessageError(DomainError): ...
class TooLongMessageError(DomainError): ...
```

## Applicationで例外を受け取り、意味を変換
```
try:
    message = Message(dto.text)
except EmptyMessageError:
    raise UseCaseMessageError("空文字は許可されません")
```

## PresentationでHTTP形式に変換
```
@app.exception_handler(UseCaseMessageError)
async def handler(...):
    return JSONResponse(400, {"label": "入力されていません"})
```

> Domainは「400」や「日本語メッセージ」を一切知らない

---

# 🧠 Domain が中心である理由

1. **正しい状態だけを許す**
2. **バリデーションが1箇所に集約**
3. **表記ゆれ・バグの根源を排除**
4. **UI変更は外側だけで完結**
5. **外部API追加が簡単**
6. **修正コストが最小**

> 「ValueObjectを導入するだけで設計品質が跳ね上がる」

---

# 📦 importについて（実装上のポイント）

ValueObjectが増えると import が増えるように見えるが、
実務では以下の形で集約する。

```
domain/value_objects/
  message.py
  email.py
  title.py
  user_id.py
```

```
# domain/value_objects/__init__.py
from .message import Message
from .email import Email
...
```

→ 外側では：

```
from domain.value_objects import Message
```

だけで良い。

Importが増えるのは「設計成功の証拠」。

---

# ✨ Domain = 日本語で言うと？

- 問題領域
- 業務領域
- 意味の世界
- ルールが住む場所

> 「このデータは何を意味するのか？」だけを扱う場所

---

# 🏁 結論（最重要まとめ）

- Domain = 意味 + ルール + 不変条件
- DTO = 層を渡る箱
- Schema = HTTP世界の型
- Payload = 外部API仕様
- DomainはHTTPやDBを知らない
- 不正状態はDomain Model生成時に拒否
- エラー種別がビジネスルールになる

> **Domain Modelを導入すると「普通の文字列」は世界から消える**  
> → アプリは「意味のあるデータ」だけで動く。

この1点が理解できれば、Clean Architectureの本質は掴めています。
