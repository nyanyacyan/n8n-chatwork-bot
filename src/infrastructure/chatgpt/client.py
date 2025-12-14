# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 仕様：ChatGPTクライアント実装

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# MACテスト用
# import sys, os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

# import
from openai import OpenAI

# ChatGPT関連
from infrastructure.chatgpt.config import ChatgptConfig

# ----------------------------------------------------------------------------------
# **********************************************************************************
# ここではほぼドキュメント通りに記述する

class OpenAIClient:
    def __init__(self, config: ChatgptConfig):

        self.config = config
        self.client = OpenAI(api_key=self.config.chatgpt_api_token)


    def generate_text(self, prompt: str):
        result = self.client.chat.completions.create(
            model=self.config.model.value,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return result.choices[0].message.content



# **********************************************************************************
# テストOK

if __name__ == "__main__":
    config = ChatgptConfig()  # .env.chatgpt を読む
    test_openai = OpenAIClient(config=config)
    test_prompt = "次の文章を英語に翻訳してください。\nこんにちは、元気ですか？"
    response = test_openai.generate_text(prompt=test_prompt)
    print(response)