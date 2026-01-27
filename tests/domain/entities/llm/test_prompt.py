# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 仕様：
# Prompt エンティティが PromptContent を保持し、
# length が内容文字数と一致することを確認する。
# 確認方法: 生成後に content と length を assert。
# 正常系のみでOK
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from src.domain.entities.llm.prompt import Prompt
from src.domain.values.prompt_content import PromptContent

# ----------------------------------------------------------------------------------


def test_prompt_success():
    content = PromptContent("hello prompt")

    prompt = Prompt(content=content)

    assert prompt.content == content
    assert prompt.length() == len("hello prompt")

# **********************************************************************************
