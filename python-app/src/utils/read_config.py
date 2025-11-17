# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
import json
import os

from logger import Logger

# ----------------------------------------------------------------------------------
# **********************************************************************************

class ReadConfig:
    def __init__(self):
        # logger
        self.getLogger = Logger()
        self.logger = self.getLogger.getLogger()

# ----------------------------------------------------------------------------------
# 実施結果を返すメソッド

    def process(self, key: str, detail_key: str):
        self.logger.debug("configの値の読込開始")

        value = self.get_json_value(key, detail_key)

        self.logger.debug("configの値の読込終了")
        return value

# ----------------------------------------------------------------------------------
# 現在のカレントディレクトリを取得するメソッド

    def currentDir(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.logger.debug(f"Current directory: {current_dir}")
        return current_dir

# ----------------------------------------------------------------------------------
# 指定した階層分だけ上の階層へ移動するメソッド

    def up_dir(self, path: str, levels: int = 1):
        up_dir = os.path.abspath(os.path.join(path, *[".."] * levels))
        self.logger.debug(f"Up {levels} 対象の階層: {up_dir}")
        return up_dir
# ----------------------------------------------------------------------------------
# configのパスを取得するメソッド

    def get_config_path(self):
        base_dir = self.currentDir()
        parent_dir = self.up_dir(base_dir, levels=3)
        config_path = os.path.join(parent_dir, 'data', 'config', 'config.json')
        self.logger.debug(f"Config path: {config_path}")
        return config_path

# ----------------------------------------------------------------------------------
# jsonファイルを読み込むメソッド

    def load_config(self):
        config_path = self.get_config_path()
        try:
            with open(config_path, 'r', encoding='utf-8') as config_file:
                config = json.load(config_file)
                self.logger.info("Configuration loaded successfully.")
                return config

        except FileNotFoundError as e:
            self.logger.critical(f"configファイルが見つかりませんでした: {config_path}")
            raise FileNotFoundError(f"configファイルが見つかりませんでした: {config_path}") from e

        except json.JSONDecodeError as e:
            self.logger.critical(f"configファイルのJSONデコードエラーが発生しました: {config_path}")
            raise ValueError(f"configファイルのJSONデコードエラーが発生しました: {config_path}") from e

# ----------------------------------------------------------------------------------
# jsonファイルから値を取得するメソッド

    def get_json_value(self, key: str, detail_key: str):
        config = self.load_config()
        try:
            values = config[key]
            masked_values = self.mask_value(values)
            self.logger.debug(f"'config[{key}]': {masked_values}")
            value = values[detail_key]
            masked_value = self.mask_value(value)
            self.logger.info(f"configから取得した内容 '{detail_key}': {masked_value}")
            return value

        except KeyError as e:
            self.logger.error(f"指定されたキーがconfigファイルに存在しません: {key}")
            raise KeyError(f"指定されたキーがconfigファイルに存在しません: {key}") from e

# ----------------------------------------------------------------------------------
# 値を隠すメソッド

    def mask_value(self, value: str, unmasked: int =2):
        # 文字列じゃなければ固定のマスク
        if not isinstance(value, str):
            mask_value = "****"
        else:
            # 短い場合：そのまま + "****" でごまかす
            if len(value) <= unmasked:
                mask_value = value + "*" * 4
            else:
                # 先頭 unmasked 文字だけ残して残りは *
                mask_value = value[:unmasked] + "*" * (len(value) - unmasked)

        self.logger.debug(f"Masked value: {mask_value}")
        return mask_value

# ----------------------------------------------------------------------------------


# **********************************************************************************

if __name__ == "__main__":
    key = "CHATWORK"
    detail_key = "ROOM_ID"
    ReadConfig().process(key=key, detail_key=detail_key)
# ----------------------------------------------------------------------------------
