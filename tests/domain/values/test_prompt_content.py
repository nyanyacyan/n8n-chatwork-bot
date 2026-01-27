# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 仕様：
# PromptContent の値オブジェクトが有効な文字列を保持できることと、
# 空文字・空白・None・非文字列・最大長超過で ValueError になることを確認する。
# 確認方法: 正常系は value と length を assert、異常系は pytest.raises を使用。
# 検証の順序 > 型チェック > Noneチェック > 値チェック
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import pytest

from src.domain.values.prompt_content import PromptContent
# ----------------------------------------------------------------------------------


def test_prompt_content_success():
    prompt = PromptContent("これはテストのユーザープロンプトです")
    assert prompt.value == "これはテストのユーザープロンプトです"
    assert prompt.length() == 18

# ----------------------------------------------------------------------------------

@pytest.mark.parametrize(
    "invalid",
    ["", "   ", None, 123, "a" * 2001],
)

def test_prompt_content_invalid(invalid):
    with pytest.raises(ValueError):
        PromptContent(invalid)

# **********************************************************************************
