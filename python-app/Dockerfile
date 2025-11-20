#* 実施Command: docker compose run --rm python-app

# ベースイメージとしてPython 3.10のスリム版を使用
# Linuxの軽量イメージであるため、イメージサイズを小さく保つことができる
FROM python:3.10-slim

# 作業ディレクトリを設定
WORKDIR /app

# Git インストール
RUN apt-get update && apt-get install -y git && apt-get clean

COPY requirements.txt .

# イメージサイズが命なのでなるべくイメージサイズを抑えるためにキャッシュを残さないようにする
RUN pip install --no-cache-dir -r requirements.txt

# python-appディレクトリ内の全てのファイルをコンテナ内の作業ディレクトリにコピー
COPY . .

# ターミナルが待機状態になるようにしているCommand
CMD ["/bin/bash"]
