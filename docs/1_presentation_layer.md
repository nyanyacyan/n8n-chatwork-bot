# Presentation Layer ガイド

このドキュメントでは、Clean Architecture における Presentation 層の役割と、実装時に **やってはいけないこと（禁止事項）** をまとめる。

---

## 🎯 Presentation層の役割

Presentation層は「外部の世界」と「アプリケーション内部」をつなぐ「入口（インターフェース）」である。

具体的には以下の責務を持つ：

### 1. 外部リクエストの受け取り
- HTTP / Webhook / CLI / UI などを受け取る
- 例：FastAPI Router

### 2. 入力データの抽出
- リクエストBodyやクエリパラメータから必要なデータを取り出す
- 必要最小限の処理のみ

### 3. UseCaseへの処理依頼（DI）
- UseCaseのインスタンスを作成
- 抽象インターフェース（IChatClientなど）を注入して実行

例：

```python
usecase = SendMessageUseCase(ChatWorkClient())
usecase.execute(text)
```

### 4. 戻り値をレスポンスとして返却
- UseCaseの戻り値を利用し、HTTPレスポンスを生成
- Presentation層でレスポンス形式を決める

---

## ❌ Presentation層で「やってはいけないこと」

Presentation層は「入出力の窓口」であるため、自身に余計な責務を持たせると、設計が破綻する。

以下は必ず避けるべき：

### 1. ビジネスロジックを書く
NG例：
```python
# メッセージの意味付けを直接書く（NG）
if not text:
    raise ValueError()
```
→ Domain/UseCaseに書くべき

### 2. Infrastructureの内部実装を使う
NG例：
```python
client = ChatWorkClient()
client._build_payload(...)
```
→ Presentationは「具体実装の詳細」を知らない

### 3. Domainモデルを変更する
NG例：
```python
message.text = message.text.upper()
```
→ Domain内部の意味を破壊する

### 4. UseCaseを複数回呼び出して連携処理する
- 複雑なフロー制御はUseCase内部で行う
- Presentationは「1アクション＝1UseCase」

### 5. データ変換ロジック（形式変換）を書く
NG例：
```python
payload = {"body": text}
```
→ Infrastructureの責務

### 6. DIポイントが複数箇所に存在する
NG例：
```python
usecase = UseCase(ChatWorkClient())
usecase2 = OtherUseCase(ChatWorkClient())
```
→ DIは「1箇所」に集約する（Composition Root）

---

## 📌 Presentation層の設計原則

Presentationは **「入り口の責務に徹する」**ことで、Clean Architectureの全体構造が保たれる。

原則：

- 「外部＝ここ」
- 「内部＝ここから先」
- 「境界＝ここで責務を切る」

つまり：

```
外部形式 → Presentationで吸収 → 内部へ「意味」だけ渡す
```

例：
- HTTPのJSON形式はPresentationで吸収
- Domainには「意味のある値」を渡す（Messageなど）

---

## 🧭 Composition Root の役割

Presentationは「唯一の結合ポイント」である：

- UseCaseへの依存注入
- 抽象（インターフェース）へ具体を渡す
- 以降、上位層は具体を知らない

つまり：

```
Presentation = 依存性注入の「根（Root）」
```

---

## ✔ まとめ

- Presentation層は **アプリケーションの入口**
- 責務は **受け取り → 依頼 → 返却** のみ
- 内部処理、ルール、形式変換は **他レイヤが担当**
- 「やってはいけないこと」を守ることで、設計の方向性が保たれる

本ドキュメントは、プロジェクト内での Presentation層の運用指針を示す目的で作成する。
