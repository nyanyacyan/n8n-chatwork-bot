# n8n + Chatwork Bot Architecture

このプロジェクトは **FastAPI + n8n + ChatWork + OpenAI** を連携させるためのアーキテクチャ設計例です。

## 目的：
- アーキテクチャ設計の基礎理解
- レイヤ分離による保守性の向上
- Django / 大規模 API 設計にも流用できる設計

本 README は「ディレクトリ構造」と「責務の定義（レイヤ）」を明確にするためのドキュメントです。

---

# 🟢 Presentation Layer（入口）

## 役割：
- **外部からのアクセスを受け付ける層**
- HTTP リクエストを受けて、必要なデータを Application に渡す
- 戻り値を JSON として返すだけ

できること：
- Webhook の受信
- Request の JSON を DTO に変換
- Application の呼び出し
- Response を JSON 変換して返す

やっていい：
✔ Request のバリデーション
✔ JSON → DTO 変換
✔ Application への処理委譲

やってはいけない：
❌ ビジネス判断
❌ ドメインロジック実行
❌ 「このあと何をするか」を決めてはダメ

理由：
「外部に触って、結果を返すだけ」に留める

例：
```python
@app.post("/webhook/chatwork")
async def chatwork_webhook(request: Request):
    dto = ChatworkWebhookDTO.from_json(await request.json())
    result = app_flow.process(dto)
    return StandardResponse(status="ok", message="success", data=result)
```

---

# 🟡 Application Layer（ビジネス処理の本体）

役割：
- プレゼンテーション層から受け取った入力を「意味のある処理」にする
- ビジネスルールを実行する
- 外部サービスへ問い合わせが必要なら Infrastructure 層を使う

できること：
- ビジネスロジック（業務処理）
- ドメインルールの実行
- 例外処理・再試行など

やっていい：
✔ ドメインルール実行
✔ ChatGPT の再試行制御
✔ ChatWork API の使い方を決める

やってはいけない：
❌ UI を決める
❌ FastAPI の request/response を触る
❌ Infrastructure を直接 import して固定する

理由：
技術詳細とルールを分離することで、変更に強くなる

---

# 🔵 Infrastructure Layer（外部接続）

役割：
- 外部 API / DB / 外部サービスとの通信
- Application 層からの要求に応じて実際の通信を行う
- 結果データを DTO に変換して返す

できること：
- ChatWork API 呼び出し
- OpenAI API 呼び出し
- ロギング
- 設定値読み込み

やっていい：
✔ requests / http 通信
✔ URL の組み立て
✔ JSON パース

やってはいけない：
❌ 業務判断
❌ ビジネスロジック
❌ 「どう使うか」を決める

理由：
「外部に触って、結果を返すだけ」

---

# 🟣 DTO（Data Transfer Object）とは？

DTO とは：
外部から渡ってくる JSON や dict を **型が明確なデータ構造** に変換するためのオブジェクト。

例：
- Webhook JSON → `ChatworkWebhookDTO`
- ChatGPT Response JSON → `ChatGPTResponseDTO`

目的：
- 型安全性が上がる
- 名前が付くことでコードが理解しやすい
- 「JSON をそのまま操作する」混乱を防ぐ

やっていい：
✔ Pydantic で型定義
✔ JSON → DTO 変換

やってはいけない：
❌ DTO 内でビジネス処理する
❌ 外部 API を呼び出す

---

# 🚫 レイヤを跨いで「やってはいけないこと」

こうなると破綻します：

❌ FastAPI から直接 OpenAI を呼ぶ  
❌ DTO の中から ChatWork API を叩く  
❌ Infrastructure の中にビジネス判断を書く  

理由：
- 依存関係が逆転し、変更できなくなる
- テストが難しくなる
- 再利用できないコードになる

---

# 💡 正しい依存関係の流れ

```
[Presentation] → [Application] → [Infrastructure]
```

戻りは DTO として返す：

```
[Infrastructure] → DTO → [Application] → Response → [Presentation]
```

---

# 🌱 なぜこの分離が必要か？

- 「どこで何をするか」が明確になる
- チーム開発で役割分担しやすい
- Django や FastAPI でも同じ考え方が使える
- ドメインロジックが育っていく
- テストしやすい
- レビューしやすい

---

# 🧭 推奨ディレクトリ構成

```
src/
  base/                  ← Presentation
    webhook_server.py

  flow/                  ← Application
    main_flow.py

  infra/                 ← Infrastructure
    chatwork_client.py
    openai_client.py

  data/
    schema/              ← DTO
      chatwork.py
      ai.py
      api_response.py

  utils/                 ← 横断的機能
    logger.py
    read_config.py
```

※ utils は横断的な機能として自由に使ってよい

---

# 📝 ベストプラクティスまとめ

| レイヤ | やっていいこと | やっていけないこと |
|--------|----------------|---------------------|
| Presentation | 入力受取、DTO変換、返す | ビジネス判断 |
| Application | ビジネスロジック | HTTP 通信 |
| Infrastructure | API 通信 | 業務判断 |
| DTO | 型変換 | 外部接続 |

---

# 🎯 今後の展望

この設計は以下に拡張できます：

- Django + Clean Architecture
- DDD（ドメイン駆動設計）
- マイクロサービス分離
- ChatWork 以外の Bot 拡張（Slack / LINE / Discord）

---

# 🏁 結論

> **レイヤ分離が「強いコード」を作る。**

- 「どこに書くべきか」が明確
- 「やってはいけないこと」も明確
- 設計思想が Django / FastAPI でも共通
- 企業のアーキテクチャに近い

この README をベースに、今後の開発を進めてください 🚀

```
