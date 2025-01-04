import os
import asyncio
import streamlit as st
from dotenv import load_dotenv

from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langchain_core.runnables import RunnableConfig
from langchain_google_genai import ChatGoogleGenerativeAI

# 從 config 檔案匯入設定
from prompts import SYSTEM_PROMPT
from config import API_SETTING
from utils import truncate_conversation_if_needed, save_log

load_dotenv()

# .env 取設定的 Google API 金鑰
os.environ['GOOGLE_API_KEY'] = os.getenv('API_KEY', default=None)

# 定義狀態類型
class State(TypedDict):
    messages: Annotated[list, add_messages]

# 定義 chatbot 函式
async def chatbot(state: State, config: RunnableConfig):
    response = await llm_chat_mode.ainvoke(state["messages"], config)
    return {"messages": response}

# 初始化 LLM 與圖形生成器
llm_chat_mode = ChatGoogleGenerativeAI(model=API_SETTING['MODEL_NAME'])
graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.set_entry_point("chatbot")
graph_builder.set_finish_point("chatbot")
graph = graph_builder.compile()


async def main():
    """
    主程式，負責初始化 Streamlit 界面，處理使用者輸入，
    與 LangGraph 進行互動並顯示流式聊天機器人的回應。

    功能包括：
    1. 初始化對話記錄與系統提示。
    2. 提供「清除對話」按鈕以重置對話狀態。
    3. 處理使用者輸入，調用聊天 API，並以流式方式顯示回應。
    4. 儲存對話記錄到本地檔案。
    """
    st.title("Streamlit Chatbot Demo: LangGraph with Streaming Mode")

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

    if st.button("清除對話"):
        st.session_state["messages"] = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]
        if "log_filename" in st.session_state:
            del st.session_state["log_filename"]
        st.rerun()

    for msg in st.session_state["messages"]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if user_input := st.chat_input("請輸入您的訊息..."):
        st.session_state["messages"].append({"role": "user", "content": user_input})
        st.session_state["messages"] = truncate_conversation_if_needed(
            st.session_state["messages"],
            max_tokens=API_SETTING['MAX_TOKENS']
        )

        with st.chat_message("user"):
            st.write(user_input)

        assistant_reply = ""
        with st.chat_message("assistant"):
            partial_placeholder = st.empty()
            async for msg, _ in graph.astream({"messages": st.session_state["messages"]}, stream_mode="messages"):
                chunk_text = msg.content
                assistant_reply += chunk_text
                partial_placeholder.write(assistant_reply + "▌")

        st.session_state["messages"].append({"role": "assistant", "content": assistant_reply})

        st.session_state["messages"] = truncate_conversation_if_needed(
            st.session_state["messages"],
            max_tokens=API_SETTING['MAX_TOKENS']
        )

        save_log(st.session_state["messages"])

if __name__ == "__main__":
    asyncio.run(main())