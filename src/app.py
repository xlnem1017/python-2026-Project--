import streamlit as st
from pathlib import Path

from pages_ui.chat import show_chat_page
from pages_ui.upload import show_upload_page
from pages_ui.analysis import show_analysis_page
from pages_ui.visualization import show_visualization_page
from pages_ui.report import show_report_page
from utils.config import APP_TITLE, APP_ICON

st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide"
)

st.sidebar.title(APP_TITLE)

page = st.sidebar.radio(
    "导航",
    [
        "AI聊天",
        "上传数据",
        "数据概览",
        "数据可视化",
        "AI分析报告"
    ]
)

if page == "AI聊天":
    show_chat_page()
elif page == "上传数据":
    show_upload_page()
elif page == "数据概览":
    show_analysis_page()
elif page == "数据可视化":
    show_visualization_page()
elif page == "AI分析报告":
    show_report_page()