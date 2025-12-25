# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 仕様：
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