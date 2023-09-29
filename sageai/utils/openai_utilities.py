from typing import Dict, List


def get_latest_user_message(messages: List[Dict]) -> Dict | None:
    for message in reversed(messages):
        if message.get("role") == "user":
            return message
    return None
