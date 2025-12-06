# Infrastructure Layer ガイド

このドキュメントでは、Clean Architecture における **Infrastructure層（外部実装層）** の役割と原則、そして「やってはいけないこと（禁止事項）」を整理する。

---

## 🎯 Infrastructure層の目的

Infrastructure層は、Domain層で定義された抽象インターフェース（契約）に対して **具体的な実装（色付け）** を提供する層である。

キーワードは：

> **外部世界との通信・技術による実現・具体形式**

であり、ビジネスルールや「意味」を持たない。

---

## 🟢 Infrastructure層の役割

### 1. 抽象インターフェースの実装
DomainやApplication層で定義された抽象（例：`IChatClient`）に基づいて実装する。

例：
```python
class ChatWorkClient(IChatClient):
    def post(self, message: Message):
        payload = message.as_chatwork()
        self._post_api(payload)
```

### 2. 外部APIとの通信
HTTPクライアントやSDKを利用し、外部サービスに接続する。

例：
- ChatWork API
- Slack API
- DBアクセス
- RedisやQueue
- ファイルストレージ

### 3. 具体形式への変換
Domainモデル（Messageなど）を **外部サービスが理解できる形式に変換する**。

例：
```python
payload = {"body": message.text}
```

### 4. 技術処理のカプセル化
- リトライ
- Timeout
- Logging
- Errorハンドリング  
などの技術的処理を担当する。

---

## 🧠 Infrastructure層が「しないこと」

Infrastructureは「技術実装」だけであり、意味を扱わない。

以下は **絶対に行ってはいけない**：

### ❌ 1. Domainルールの実装
NG例：
```python
if not message.text:
    raise ValueError()
```
→ Domainの責務

### ❌ 2. Business Logicの実装
NG例：
```python
if user.is_admin():
    ...
```
→ Application/Domainの責務

### ❌ 3. Domainを変更する
NG例：
```python
message.text = text.upper()
```
→ Domain不変条件の破壊

### ❌ 4. UseCaseを呼び出す
NG例：
```python
SendMessageUseCase(...)
```
→ 依存方向が逆転する

### ❌ 5. Presentation形式（HTTPレスポンス）を扱う
NG例：
```python
return JSONResponse(...)
```
→ Presentationの責務

---

## 📌 Infrastructure層の設計原則

### ✔ 1. 抽象に従う（DIP）
Infrastructureは Domainが定義する抽象インターフェースに従い、  
Domain側に「正しさ」の中心がある。

```
Domain（抽象） → Infrastructure（実装）
```

### ✔ 2. 技術変更に強い構造
チャットサービスが変わっても DomainやApplicationは変更不要：

```
ChatWorkClient → SlackClient → DiscordClient
```

差し替えるだけ。

### ✔ 3. 決定はComposition Root
どのクライアントを使うかの決定は **Presentation層で行う**：

```python
usecase = SendMessageUseCase(ChatWorkClient())
```

Infrastructureが自分で決めない。

---

## 🧭 Applicationとの関係

Infrastructure層は **Application層を知らない**。

正しい依存関係：

```
Application → Domain（抽象）
Infrastructure → Domain（抽象）
```

InfrastructureからApplicationに依存すると逆転し、設計が崩壊する。

---

## 🔧 技術的関心事の例

Infrastructure層で扱うべきこと：

- HTTP通信（requests, httpx）
- リトライ戦略（Exponential Backoff）
- Timeout設定
- Rate Limit対応
- 認証・署名
- Logging
- JSON → Payload変換
- SDK利用

DomainやApplicationはこれらの存在すら知らない。

---

## ✔ まとめ

- Infrastructure層は **外部世界との接続と実現手段** を担当
- Domainが定義した抽象（契約）を実装するだけ
- Businessロジックや「意味」は持たない
- 依存方向は常に「内→外」であり、逆流しない
- 差し替え可能な構造により拡張性が得られる

本ドキュメントは、プロジェクトで Infrastructure層を正しく運用するための設計方針を示す目的で作成する。
