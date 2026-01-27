# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 仕様：
# LLMResponseContent が有効な文字列を保持できることと、
# 空文字で ValueError になることを確認する。
# 確認方法: 正常系は value と length を assert、異常系は pytest.raises を使用。
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import pytest

from src.domain.values.llm_response_content import LLMResponseContent

# ----------------------------------------------------------------------------------


def test_llm_response_content_success():
    content = LLMResponseContent("ok")
    assert content.value == "ok"
    assert content.length() == 2


# ----------------------------------------------------------------------------------


def test_llm_response_content_invalid_empty():
    with pytest.raises(ValueError):
        LLMResponseContent("")

# **********************************************************************************
