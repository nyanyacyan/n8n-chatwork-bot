## app.pyにて注意すべきこと

- どの Client を使うか
- どの Adapter を使うか
- どの UseCase が何に依存しているか

👉全部が **app.pyに一列で書かれている**

### 「このアプリの構成図が app.py にそのまま書いてある」

## すべての依存関係がapp.pyに集約されて渡されている状態がベスト
Client → Adapter → UseCase → Orchestration UseCase → main()

```python

# app.py
def main():
    # =====================
    # 1. Client 作成
    # =====================
    chatwork_client = ChatWorkClient()
    chatgpt_client = OpenAIClient()

    # =====================
    # 2. Adapter 作成
    # =====================
    msg_reader = ChatworkGetMessagesAdapter(chatwork_client)
    msg_sender = ChatworkSendMsgAdapter(chatwork_client)
    text_generator = ChatGPTTextGeneratorAdapter(chatgpt_client)

    # =====================
    # 3. UseCase 作成（小）
    # =====================
    get_latest_msg_uc = GetLatestChatMessageUseCase(msg_reader)
    create_prompt_uc = CreatePromptFromChatMessageUseCase()
    generate_reply_uc = GenerateResponseFromPromptUseCase(text_generator)
    send_reply_uc = SendChatMessageUseCase(msg_sender)

    # =====================
    # 4. Orchestration UseCase
    # =====================
    reply_uc = AssistChatReplyUseCase(
        get_latest_msg_uc,
        create_prompt_uc,
        generate_reply_uc,
        send_reply_uc,
    )

    # =====================
    # 5. 実行
    # =====================
    reply_uc.execute()


if __name__ == "__main__":
    main()

```