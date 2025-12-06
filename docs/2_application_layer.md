# Application Layer ガイド

このドキュメントでは、Clean Architecture における **Application層（ユースケース層）** の役割と原則、そして「やってはいけないこと（禁止事項）」を整理する。

---

## 🎯 Application層の役割

Application層は「ビジネス行動（UseCase）」を具体的に実行するレイヤであり、以下の責務を持つ：

### 1. ビジネスフローの実行
- Presentation層から依頼された処理（ユースケース）を実行
- 内部の複数の操作を「ひとつの行動」としてまとめる

例：
- メッセージ受信 → メッセージをDomainで意味化 → 外部APIへ送信

### 2. Domainモデルの利用
- Domain層に定義されているモデル（例：Message）を使用する
- モデルは **生成・検証・行動の中心** であり、Applicationは「使う側」

例：
```python
message = Message(text)
self.client.post(message)
```

### 3. 抽象インターフェースの活用（DIP）
- Domain層で定義された抽象（例：IChatClient）を参照
- Infrastructure層の具体実装（例：ChatWorkClient）は知らない

例：
```python
def __init__(self, client: IChatClient):
    self.client = client
```

### 4. トランザクションの制御
- 1ユースケース = 1トランザクション
- 外部連携や一貫性確保の調整

---

## 🧠 Application層が「しないこと」

Application層は「行動」のみを担当し、「ルール」を持たない。  
以下は **絶対に行ってはいけない**：

### ❌ 1. ドメインルールの実装
NG例：
```python
if not text:
    raise ValueError("empty")
```
→ これはMessage（Domain）の責務

### ❌ 2. 外部API形式の構築
NG例：
```python
payload = {"body": text}
```
→ これはInfrastructureの責務

### ❌ 3. 複雑なデータ変換
- JSON構築
- Header付与
- リトライ処理  
→ すべてInfrastructure

### ❌ 4. Presentation形式を扱う
NG例：
```python
request = Request.json()
```
→ Presentationが吸収すべき形式変換

### ❌ 5. Domainモデルの状態を書き換える
NG例：
```python
message.text = text.upper()
```
→ Domainの不変条件を破壊する

---

## 💡 Application層の設計原則

Application層は **「行動を制御し、実行する指揮者」** であり、
以下の原則で設計する：

### ✔ 1. Domainを中心に設計
- Domainの概念を利用して「意味づけされた処理」を行う

### ✔ 2. 抽象インターフェースを使用
- 具体実装を知らず、抽象のみ参照

### ✔ 3. 1 UseCase = 1アクション
- 「複数の意味」を持つユースケースを作らない

NG例：  
`SendMessageAndStoreInDBUseCase` → 責務が混ざる

---

## 🧭 依存方向（DIP）

Application層は **内側に向かって依存する**：

```
Presentation → Application → Domain
                 ↑
             Infrastructure（実装）
```

- Domainが抽象（契約）
- Infrastructureが実装（色付け）
- Applicationが利用（行動）

---

## 🔗 Composition Rootとの関係

依存注入（DI）は **Presentation層で** 行う：

```python
usecase = SendMessageUseCase(ChatWorkClient())
usecase.execute(text)
```

Application層で new しない：

```python
# ❌ NG
def execute():
    client = ChatWorkClient()
```

→ これをすると「具体実装への依存」が発生し、Cleanの崩壊に繋がる。

---

## ✔ まとめ

- Application層は **ビジネス行動の調整役**
- Domainを利用して「意味のある処理」を実行
- 抽象インターフェースに依存し、具体実装を知らない
- UseCaseは単一責務であり、複雑なロジックは持たない
- 外部形式変換やルール定義は **別レイヤの責務**

このドキュメントは、プロジェクトで Application層を正しく運用するための設計方針を示す目的で作成する。
