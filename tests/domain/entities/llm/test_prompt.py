# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 仕様：
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