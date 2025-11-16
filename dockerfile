# n8nの公式イメージをベースにする
# Node.jsとn8nのフレームワークをインストール
FROM n8nio/n8n:latest


# OSパッケージ更新＆Pythonインストール
USER root
RUN apt-get update && apt-get install -y python3 python3-pip && apt-get clean

# 必要なPythonパッケージをインストール
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# ------------------------------
# ③ パーミッション調整
# ------------------------------
RUN mkdir -p /home/node/ && \
    chown -R node:node /home/node/

USER node

# ------------------------------
# ④ 起動コマンド（公式のまま）
# ------------------------------
CMD ["n8n"]
