# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 仕様：
# ReadConfig が設定ファイルから値を読み出せること、
# キーが存在しない場合に KeyError になることを確認する。
# 確認方法: 一時的な config.json を作成し、process の戻り値と例外を assert。
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import json
from pathlib import Path

import pytest

from src.shared.read_config import ReadConfig

# ----------------------------------------------------------------------------------


def _create_config(tmp_path: Path, data: dict) -> Path:
    config_dir = tmp_path / "data" / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    config_path = config_dir / "config.json"
    config_path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return config_path


# ----------------------------------------------------------------------------------


def test_read_config_process_success(tmp_path, monkeypatch):
    _create_config(
        tmp_path,
        {
            "CHATWORK": {
                "ROOM_ID": 123,
            }
        },
    )

    reader = ReadConfig()

    # get_config_path がこの tmp_path を指すように差し替える
    def fake_get_config_path():
        return str(tmp_path / "data" / "config" / "config.json")

    monkeypatch.setattr(reader, "get_config_path", fake_get_config_path)

    result = reader.process(key="CHATWORK", detail_key="ROOM_ID")
    assert result == 123


def test_read_config_process_key_error(tmp_path, monkeypatch):
    _create_config(
        tmp_path,
        {
            "OTHER": {
                "ROOM_ID": 123,
            }
        },
    )

    reader = ReadConfig()

    def fake_get_config_path():
        return str(tmp_path / "data" / "config" / "config.json")

    monkeypatch.setattr(reader, "get_config_path", fake_get_config_path)

    with pytest.raises(KeyError):
        reader.process(key="CHATWORK", detail_key="ROOM_ID")

# **********************************************************************************
