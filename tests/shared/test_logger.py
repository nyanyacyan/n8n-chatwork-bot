# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 仕様：
# Logger が logger インスタンスを返し、ログ出力用のパスを作成できることを確認する。
# 確認方法: getLogger の戻り値が logging.Logger であることと、
# toLogsPath が実際にディレクトリを作成することを assert。
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import logging
from pathlib import Path

from src.shared.logger import Logger

# ----------------------------------------------------------------------------------


def test_logger_get_logger_returns_instance():
    logger = Logger()
    result = logger.getLogger()
    assert isinstance(result, logging.Logger)


def test_logger_to_logs_path_creates_dir(tmp_path, monkeypatch):
    logger = Logger()

    # currentDir は @property でsetterがないため、クラス側のpropertyを差し替える
    monkeypatch.setattr(
        Logger,
        "currentDir",
        property(lambda self: tmp_path / "dummy" / "file.py"),
    )

    logs_path = logger.toLogsPath(levelsUp=1, dirName="logs")

    assert isinstance(logs_path, Path)
    assert logs_path.exists()
    assert logs_path.is_dir()

# **********************************************************************************
