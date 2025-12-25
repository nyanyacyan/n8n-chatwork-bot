# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 仕様：LLMにおけるResponseを定義

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from dataclasses import dataclass
from archive.response_content import ResponseContent


# ----------------------------------------------------------------------------------
# **********************************************************************************


@dataclass(frozen=True)
class Response:
    content: ResponseContent

    def length(self) -> int:
        return self.content.length()

# **********************************************************************************