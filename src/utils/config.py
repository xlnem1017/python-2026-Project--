import os

APP_TITLE = "AI智能数据分析平台"

APP_ICON = "📊"

REPORT_FILENAME = "AI数据分析报告.txt"

MODEL_NAME = "deepseek-chat"

DEEPSEEK_API_KEY = os.getenv(
    "DEEPSEEK_API_KEY",
    ""
)