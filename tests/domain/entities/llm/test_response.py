# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 仕様：
# Response エンティティが LLMResponseContent を保持し、
# length が内容文字数と一致することを確認する。
# 確認方法: 生成後に content と length を assert。
# 正常系のみでOK
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import

from src.domain.entities.llm.response import Response
from src.domain.values.llm_response_content import LLMResponseContent


# ----------------------------------------------------------------------------------


def test_response_success():
    content = LLMResponseContent("hello response")

    response = Response(content=content)

    assert response.content == content
    assert response.length() == len("hello response")

# **********************************************************************************
