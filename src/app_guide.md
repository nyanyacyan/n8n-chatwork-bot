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
        # 0. Config 作成
        # =====================
        chatwork_config = ChatworkConfig()
        chatgpt_config = ChatgptConfig()

        # =====================
        # 1. Client 作成
        # =====================
        chatwork_client = ChatWorkClient(chatwork_config)
        chatgpt_client = OpenAIClient(chatgpt_config)

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

---



## 例外処理に関して
### 予測して構築するのはNG
**基本は例外が発生してから構築する⭕️**

- 無駄なコードが増える（時間の浪費）
- 可読性が下がる
- メンテナンス性が下がる

<br>

### 例外が発生した場合
**発生箇所にあわせてその箇所で構築⭕️**
- 例外が発生したら、その箇所で例外をキャッチしてログを残す
- 必要に応じて再度例外を投げる


<br>

### 例外の投げ方
**基本はそのArchitectureに合わせた例外名を使って投げる⭕️**

- 例: DomainError, InfraError

```python

except DomainError as e:
    logger.warning(e)

except InfraError as e:
    logger.error(e)

except Exception as e:
    logger.exception(e)
```