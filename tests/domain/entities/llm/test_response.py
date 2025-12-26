# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 仕様：
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