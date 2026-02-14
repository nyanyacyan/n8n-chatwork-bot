# Webhook JSON サンプル集（ノーエンジニア向け）

作成日: 2026-02-11  
対象: `src/presentation/webhook_server.py`

---

## 1. まず結論

- Webhook は「URLにアクセスするだけ」ではなく、通常は **`POST` + JSONデータ** で届きます。
- `src/presentation/webhook_server.py:37` は受信口（POSTエンドポイント）です。
- `src/presentation/controllers/chatwork_webhook_controller.py:43` の `request.json()` は、届いたJSON本文を取り出しています。

---

## 2. どこでデータを指定しているのか？

Chatworkの設定画面では、主に「Webhook URL」を登録します。  
**JSONの中身は、Chatwork側がイベント発生時に自動生成して送ります。**

つまり:
- あなたが手入力するのは主に「送信先URL」
- 送るデータ本体はChatworkの仕様で決まる

---

## 3. データが届く流れ（図）

```text
[Chatworkでイベント発生]
   例: メッセージ投稿 / 編集 / メンション
            |
            v
[Chatworkサーバー]
   HTTPS POST + JSON本文 を送信
            |
            v
[あなたのWebhook URL]
   /webhook/chatwork
            |
            v
[Presentation: webhook_server.py]
   request.json()で本文を取得
   room_idを抽出
   DTO(GetNewMsgRequest)を作成
   UseCaseへ委譲
            |
            v
[HTTP 200/400/500 を返却]
   呼び出し元（通常はChatwork）へ返す
```

---

## 4. Chatworkから届く代表的なJSON（公式形式）

```json
{
  "webhook_setting_id": "12345",
  "webhook_event_type": "mention_to_me",
  "webhook_event_time": 1498028130,
  "webhook_event": {
    "from_account_id": 123456,
    "to_account_id": 1484814,
    "room_id": 567890123,
    "message_id": "789012345",
    "body": "[To:1484814]おかずはなんですか？",
    "send_time": 1498028125,
    "update_time": 0
  }
}
```

`room_id` は通常 `webhook_event.room_id` に含まれます。

---

## 5. このプロジェクトで2パターン受ける理由

現在 `src/presentation/webhook_server.py:35` は、以下を受けられるようにしています。

1. 公式寄り: `webhook_event.room_id`
2. 簡易テスト寄り: `room_id` 直下 or `webhook_event.room.id`

理由:
- 開発初期の互換性
- 手動テストのしやすさ
- 旧実装からの移行安全性

要するに「壊れにくくするための緩衝材」です。  
本番仕様を固める段階で、受ける形式を1つに絞るとより明確になります。

---

## 6. DTOをここで作る理由

`src/presentation/controllers/chatwork_webhook_controller.py:52` で DTO を作ってから UseCase に渡すのは、  
**UseCaseをFastAPI/HTTP仕様から切り離すため**です。

- Presentation: Web特有の形を受ける（JSON, HTTP）
- UseCase: 業務手順だけを実行する

この分離が Clean Architecture の狙いです。

---

## 7. 「返却」は誰に返すのか？

`src/presentation/controllers/chatwork_webhook_controller.py:63` の返却は、  
このAPIを呼んだ相手（通常はChatwork）へのHTTPレスポンスです。

注意:
- これは「チャットに返信メッセージを投稿した」こととは別です。
- チャット投稿はUseCase側で別途Chatwork APIを呼ぶ処理です。

---

## 8. 今の実装は問題ないか？

結論:
- Clean Architectureの方向性としては妥当です。
- ただし、仕様確定後は payload 形式を絞ると保守しやすくなります。

推奨:
- T1残タスクで「受けるJSON形式」を1つに固定
- `_extract_room_id` の分岐を最小化

---

## 9. 参考（公式）

- Chatwork APIドキュメント: Webhookについて  
  https://developer.chatwork.com/docs/webhook
- Chatworkヘルプ: Webhookを設定する  
  https://help.chatwork.com/hc/ja/articles/115000169541-Webhook%E3%82%92%E8%A8%AD%E5%AE%9A%E3%81%99%E3%82%8B



---
## 10. 参考（全体フロー図）

```Mermaid
flowchart TD

  A[Webhook受信] --> B[署名検証]
  B --> C[Webhook URLで切り分け]
  C -->|chatwork用URL| D1[Chatwork Adapterへ割り振り]
  C -->|line用URL| D2[LINE Adapterへ割り振り]
  C -->|slack用URL| D3[Slack Adapterへ割り振り]

  D1 --> E1[Schema検証]
  D2 --> E2[Schema検証]
  D3 --> E3[Schema検証]

  E1 --> F[共通DTO生成]
  E2 --> F
  E3 --> F

  F --> G[UseCaseで返信内容を構築]
  G --> H[ReplyPortを呼ぶ]
  H --> I[ReplyPort実装が送信先を切替]
  I -->|platformがchatwork| J1[Chatwork Clientで送信]
  I -->|platformがline| J2[LINE Clientで送信]
  I -->|platformがslack| J3[Slack Clientで送信]

```

---

## 11. 用語メモ（理解しやすい言葉）

- `payload`:
  - 「送られてきたデータ本体」のことです。
  - たとえると、HTTPリクエストという封筒の中に入っている手紙の本文です。
  - 今回は `request.json()` で取り出した JSON 全体が payload です。

- `@classmethod`:
  - インスタンスを作る前に呼べる「クラスに属するメソッド」です。
  - 今回の `from_payload` は「payload から DTO を作る入口」なので classmethod が合います。

- `@dataclass(frozen=True)`:
  - `@dataclass` は、クラスの初期化処理（`__init__`）などを自動で作ってくれる機能です。
  - 例: `room_id: int` と書くだけで、`ChatworkWebhookRequestDto(room_id=123)` のように作れます。
  - `frozen=True` は「作成後に値を変更できない」設定です（読み取り専用）。
  - DTOの値が途中で書き換わらないため、バグを減らしやすくなります。

- `cls(room_id=room_id)`:
  - `cls` は「このクラス自身」を指します。
  - つまり `cls(room_id=room_id)` は、実質 `ChatworkWebhookRequestDto(room_id=room_id)` と同じです。
  - `@dataclass` により `room_id` を受け取る初期化処理（`__init__`）が自動で作られています。

- `from_payload` がやっていること:
  - payload から候補の `room_id` を探す
  - 空/不正値を除外する
  - 通過した値で `ChatworkWebhookRequestDto` を作って返す
