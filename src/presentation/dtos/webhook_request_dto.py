# coding: utf-8
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# 仕様：
# Chatwork Webhook payload を Presentation層で解釈するDTO

# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# import
from dataclasses import dataclass


# ----------------------------------------------------------------------------------
# **********************************************************************************


@dataclass(frozen=True)
class ChatworkWebhookRequestDto:
    room_id: int

# ----------------------------------------------------------------------------------
# payload から room_id を抽出して DTO 化

    @classmethod
    def from_payload(cls, data: dict) -> "ChatworkWebhookRequestDto":
        if not isinstance(data, dict):
            raise ValueError("Webhook payload が不正です")

        candidates = [
            data.get("room_id"),
            data.get("roomId"),
            data.get("chatwork_room_id"),
        ]

        webhook_event = data.get("webhook_event")
        if isinstance(webhook_event, dict):
            candidates.extend([
                webhook_event.get("room_id"),
                webhook_event.get("roomId"),
            ])
            room = webhook_event.get("room")
            if isinstance(room, dict):
                candidates.extend([
                    room.get("room_id"),
                    room.get("id"),
                ])

        for candidate in candidates:
            if candidate is None:
                continue
            try:
                room_id = int(candidate)
                if room_id > 0:
                    return cls(room_id=room_id)
            except (TypeError, ValueError):
                continue

        raise ValueError("room_id が取得できませんでした")

# **********************************************************************************
