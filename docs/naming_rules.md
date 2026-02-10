# 命名規則（Clean Architecture / Python）

## このドキュメントの目的

このプロジェクトでは Clean Architecture を採用しており、  
**ファイル数が100〜200を超えることを前提**にしています。

そのため命名は次のことを最優先にします。

- VSCodeの検索ですぐに目的のファイルに行ける
- 図・ドキュメント・コードで名前がズレない
- 英語力に依存しすぎない
- 後から見ても「どこに何があるか」分かる

---

## 最重要ルール（これだけは守る）

### ① クラス名とファイル名は必ず対応させる

```text
クラス名:
AssistChatReplyUseCase

ファイル名:
assist_chat_reply_usecase.py

- 1ファイルに1つの主要クラス
- クラス名からファイル名を 機械的に想像できる こと
```
---

② 役割は suffix（語尾）で表す

名前の最後を見れば 役割が分かる 状態にする。

種類	suffix	例
UseCase	UseCase	AssistChatReplyUseCase
Entity	なし（名詞）	SendMessage
Value	Content / Id	ChatMsgContent
DomainService	DomainService	ChatLlmDomainService
Port	Port	TextGeneratorPort
Adapter	Adapter	ChatGptAdapter
Fake	Fake	FakeTextGeneratorPort


---

③ 動詞は UseCase にしか使わない
- 動詞 = UseCase
- 名詞 = Entity / Value / Port

OK
```
CreatePromptFromChatMessageUseCase
SendChatMessageUseCase
```
NG
```
PromptCreator
MessageSender
```

---

## レイヤ別 命名ルール

---

### Application / UseCase

命名ルール
```
{動詞}{対象}{UseCase}
```
例
```
AssistChatReplyUseCase
GetLatestChatMessageUseCase
CreatePromptFromChatMessageUseCase
RequestLlmResponseUseCase
SendChatMessageUseCase
```
ファイル名
```
assist_chat_reply_usecase.py
get_latest_chat_message_usecase.py
```
👉 処理の流れ（フロー）を表すのは UseCase だけ

---

### Application / DTO（Request / Response）

役割
- Presentation から受け取る入力、または返却する出力の型を表す
- UseCase の入出力境界を明確にする

命名ルール
```
{動詞}{対象}Request
{動詞}{対象}Response
```
例
```
GenerateReplyRequest
GetNewMsgRequest
SendChatMessageRequest
```

ファイル名ルール
```
{動詞}_{対象}_request.py
{動詞}_{対象}_response.py
```
例
```
generate_reply_request.py
get_new_msg_request.py
send_chat_message_request.py
```

禁止（衝突しやすい）
```
send_msg_request.py + class SendMsgRequest を複数用途で使い回す
```

理由
- 同じクラス名を複数DTOで使うと、import時に別名（as）が必要になり可読性が落ちる
- 一意な名前にすると、型名だけでユースケースが分かる

---

### Domain / Entity

命名ルール
```
業務上の意味を持つ名詞
```
例
```
SendMessage
ChatworkReceivedMessage
SlackReceivedMessage
Prompt
Response
```
- 状態を持つ
- UseCase の都合で名前を変えない

---

### Domain / Value（Value Object）

命名ルール
```
意味 + Content / Id / Value
```
例
```
ChatMsgContent
PromptContent
LLMResponseContent
ChatworkRoomId
SlackChannelId
```
- 必ず不変（immutable）
- validation はここに書く

---

### Domain / Service

役割
- Value や Entity だけでは表せない 判断・組み立て
- if / 条件分岐 / ルール

命名ルール
```
{対象}{DomainService}
```
例

ChatLlmDomainService


---

### Port（Interface）

役割
- UseCase が「やりたいこと」を表す
- 実装（ChatGPT / Slack 等）を知らない

命名ルール
```
{責務}{Port}
```
例
```
TextGeneratorPort
MsgReaderPort
MsgSenderPort
```

---

### Infrastructure / Adapter

役割
- 外部API・SDKとの接続
- Port を実装する

命名ルール
```
{技術名}{Adapter}
```
例
```
ChatGptAdapter
ChatworkAdapter
SlackAdapter
```

ファイル名ルール（必須）
```
{技術名}_adapter.py
```
例
```
chatgpt_adapter.py
chatwork_adapter.py
slack_adapter.py
```

禁止（曖昧名）
```
adapter.py
```

理由
- `adapter.py` は同名が増えやすく、検索・import・レビューで判別しづらい
- 技術名を先頭に入れると、どの外部接続の実装か即判別できる
- 将来 adapter が増えても命名衝突しない

Adapter テストファイル名ルール（必須）
```
test_{技術名}_adapter.py
```
例
```
test_chatgpt_adapter.py
test_chatwork_adapter.py
```

禁止（衝突しやすい）
```
test_adapter.py
```

---

### Test / Fake の命名

Fake クラス
```
Fake{対象}
```
例
```
FakeTextGeneratorPort
FakeMsgReaderPort
FakeSendChatMessageUseCase
```
Fake ファイル名
```
fake_text_generator_port.py
fake_msg_reader_port.py
```

---

## 図・ドキュメントとの連携ルール

Mermaid / Markdown では「クラス名」を書く
```
A[AssistChatReplyUseCase]
B[GetLatestChatMessageUseCase]
```
👉 VSCodeで
```
Cmd + P → assist
```
ですぐファイルを開く前提。

---

命名に迷ったらこの3つを見る
```
1. VSCode検索で一瞬で出る？
2. suffix で役割が分かる？
3. UseCase / Domain / Infra が混ざってない？
```
2つ以上 YES ならOK。

---

この命名規則のゴール
- ファイルが増えても迷わない
- 図 → コード → テストを往復できる
- Clean Architecture が「重くならない」

---
