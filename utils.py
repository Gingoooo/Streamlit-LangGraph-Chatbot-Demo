import os
import json
import datetime
import streamlit as st

from config import API_SETTING

def save_log(messages):
    """
    儲存對話記錄到 logs 資料夾，同一 Session 使用固定檔名。
    """
    if not os.path.exists("logs"):
        os.mkdir("logs")

    if "log_filename" not in st.session_state:
        now_str = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        st.session_state["log_filename"] = f"logs/chatlog_{now_str}.json"

    filename = st.session_state["log_filename"]
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

def approximate_token_count(text: str) -> int:
    return len(text.split())

def get_total_tokens(messages) -> int:
    total = 0
    for msg in messages:
        total += approximate_token_count(msg["content"])
    return total

def truncate_conversation_if_needed(messages, max_tokens=API_SETTING['MAX_TOKENS']):

    if not messages:
        return messages

    system_msg, other_msgs = messages[0], messages[1:]

    total = get_total_tokens(messages)
    if total <= max_tokens:
        return messages

    while total > max_tokens and other_msgs:
        removed_msg = other_msgs.pop(0)
        total -= approximate_token_count(removed_msg["content"])

    return [system_msg] + other_msgs