# Clean Architecture - データフロー概要

本ドキュメントでは、本プロジェクトにおける Clean Architecture の全体的なデータフロー（責務の流れ）をまとめる。

## 🔄 フローの全体像

以下の順序で処理が流れる：

```
Presentation → Application → Domain → Infrastructure → Presentation(Response)

流れは
リクエスト受付はPresentation、ビジネス処理はApplication、
データの意味はDomain、外部アクセスはInfrastructure、レスポンス返却は再びPresentation。

```

例：
① FastAPIでリクエスト受取（Presentation）
② UseCase実行（Application）
③ Domainモデルへ変換（Domain）
④ Client.post()で外部API呼び出し（Infrastructure）
⑤ 結果をPresentationへ戻す（戻り値）
⑥ PresentationがHTTPレスポンス返却

## 🟢 各レイヤの役割

### 1. Presentation（プレゼンテーション層）
- APIリクエスト受付（例：FastAPI Router）
- 必要な入力データを抽出
- UseCaseに処理を依頼
- 戻り値をレスポンスとして返却

### 2. Application（アプリケーション層）
- ビジネス行動（UseCase）を実行
- Domain Modelを生成し、意味を付与
- 抽象インターフェース（IChatClient）を通して外部処理を依頼

### 3. Domain（ドメイン層）
- データの「意味」と「ルール」を定義
- Entity / ValueObject（例：Messageモデル）
- ビジネスロジックの核心

### 4. Infrastructure（インフラ層）
- 抽象インターフェースの実装
- 外部API呼び出し（ChatWork / Slack）
- Domain Modelを具体的な形式に変換

## 🧠 依存方向の原則（DIP）

依存は常に「内側に向かう」。  
外部実装が内部ロジックを汚染しないように設計する：

```
Presentation → Application → Domain
Infrastructure → Domain（実装）
```

### 逆方向の依存は発生しない：

- InfrastructureはApplicationを呼び出さない
- DomainはInfrastructureを知らない
- Applicationは具体実装を知らず抽象のみに依存

## ✅ 依存関係のルール

- **Presentationは Applicationを使える**
- **Applicationは Domainを使える**
- **Domainは Infrastructureを知らない**

## 💡 Composition Root

具体的な依存関係（実装クラス）は **Presentation層で一括注入（DI）** する：

```python
usecase = SendMessageUseCase(ChatWorkClient())
usecase.execute(message)
```

これが唯一の「結合点」となり、拡張性・再利用性を高める。

## 🎯 まとめ

- Clean Architecture は「責務の分離」と「依存方向の統制」が重要
- Domainは「意味とルール」を持つ中心（本質）
- Applicationは「行動」の制御
- Infrastructureは「色付け」（具体実装）
- 結合はPresentation層に1箇所だけ

本ドキュメントはプロジェクト全体の設計思想共有を目的とする。
