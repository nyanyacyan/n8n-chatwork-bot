# Domain Layer ガイド

このドキュメントでは、Clean Architecture における **Domain層（ドメインモデル層）** の役割と原則、そして「やってはいけないこと（禁止事項）」を整理する。

---

## 🎯 Domain層の目的

Domain層はシステムの「本質的な知識」と「意味」を保持する中心であり、技術的な外部要因に影響されず **ビジネスルールを守るための層** である。

キーワードは：

> **意味・概念・ルール・不変条件**

であり、技術やAPIへの依存は存在しない。

---

## 🟢 Domain層の役割

### 1. ビジネスの「意味付け」
文字列や数値などの生データを **意味のあるモデル** に変換する。

例：
- `"Hello"` → `Message("Hello")`
- `12345` → `UserId(12345)`

### 2. 不変条件（Invariant）の保護
値が常に「正しい状態」で存在するように制約する。

例：
```python
class Message:
    def __init__(self, text: str):
        if not text:
            raise ValueError("empty message")
        self.text = text
```

### 3. ビジネスルールの保持
「何が正しいか？」「どうあるべきか？」を記述する場所。

例：
- メッセージは空であってはならない
- UserId は正数でなければならない

### 4. 表現・変換の提供
外部形式（JSONなど）ではなく **「意味のある変換」** を提供する。

例：
```python
def as_chatwork(self):
    return {"body": self.text}
```

---

## 🧠 Domainモデルの種類

Domain層では、概念を「種類」で表現し、責務を分割する。

### ✔ 1. Entity（エンティティ）
- **識別子（ID）がある**
- 状態を持ち、変化する可能性がある
- 例：User、Room、Ticket

### ✔ 2. Value Object（値オブジェクト）
- **値そのものが識別である**
- 不変であり、意味を持つ
- 例：Message、Email、UserId

※今回の例では `Message` は Value Object。

---

## ❌ Domain層で「やってはいけないこと」

Domainは「意味の中心」であり、技術的詳細や外部世界を知らない。  
以下は **絶対に禁止**：

### 1. 外部APIの知識を持つ
NG例：
```python
def send_to_chatwork(self):
    requests.post(... )
```
→ Infrastructureの責務

### 2. データベース操作を書く
NG例：
```python
db.insert(self)
```
→ Repositoryの責務

### 3. JSON形式を扱う
NG例：
```python
json.dumps({"body": self.text})
```
→ Presentation/Infrastructureの責務

### 4. フレームワーク依存
NG例：
```python
from fastapi import ...
```
→ 完全にNG

### 5. Mutable（変更可能）な状態管理をする
- Value Objectは不変であるべき

NG例：
```python
message.text = new_text
```

---

## 📌 Domain層の設計原則

### ✔ 1. 不変条件（Invariant）
モデルは常に「正しい状態」で存在し続ける必要がある：

- 空文字禁止
- 無効な範囲は禁止
- 不正な状態への変化を防止

### ✔ 2. 閉じた形で責務を持つ
「意味」を同じ場所にまとめる：
- 検証
- 変換
- 表現
- 等価性

全てが同じクラス内で完結する。

### ✔ 3. 技術ではなく概念で設計する
Domain層は「チャットワークAPI」ではなく「メッセージ」という概念で考える。

例：
❌ ChatworkMessage  
✔ Message

---

## 🧭 Applicationとの関係

Applicationは **Domainを利用する側** であり、Domainに依存する。

```
Application → Domain
```

Domainは **Applicationを知らない**。

Domainは「何が正しいか」を知っており、Applicationは「何をするか」を知っている。

---

## 🔗 Infrastructureとの関係

Domainは **抽象（インターフェース）** を定義し、Infrastructureが **具体実装** を提供する。

例：

```python
class IChatClient(Protocol):
    def post(self, message: Message): ...
```

- Domainは `post` という意味を知っている
- Infrastructureは「どうAPIを呼ぶか」を知っている

---

## 🎯 まとめ

- Domain層は **システムの中心（意味とルール）**
- 技術に依存せず「正しさ」を表現する
- Entity/ValueObjectで概念を明確化
- 外部API・DB・JSON・フレームワークは完全に禁止
- Domainは「いつでも再利用できる純粋なPythonコード」であることが原則

本ドキュメントは、プロジェクトで Domain層を正しく運用するための設計方針を示す目的で作成する。
