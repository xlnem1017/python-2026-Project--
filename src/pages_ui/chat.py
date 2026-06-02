import streamlit as st

from core.data_loader import DataLoader
from core.preprocess import DataPreprocessor
from core.ai_chat import AIChat
from utils.config import APP_TITLE


def show_chat_page():

    st.title(APP_TITLE)

    st.info(
        "上传任意数据文件后，你可以直接向AI提问，获取数据分析结果、图表建议和分析报告。"
    )

    if "messages" not in st.session_state:

        st.session_state.messages = []

    uploaded_file = st.file_uploader(
        "上传CSV、Excel或JSON文件",
        type=[
            "csv",
            "xlsx",
            "xls",
            "json"
        ]
    )

    if uploaded_file is not None:

        loader = DataLoader()

        preprocessor = DataPreprocessor()

        try:

            df = loader.load_file(
                uploaded_file
            )

        except Exception as e:

            st.error(
                f"数据加载失败: {str(e)}"
            )

            return

        df = preprocessor.process(df)

        st.session_state["df"] = df

        st.subheader(
            "数据预览"
        )

        st.dataframe(
            df.head(10),
            use_container_width=True
        )

        analyzer = AIChat().analyzer

        summary = (
            analyzer.generate_summary(df)
        )

        with st.expander(
            "查看数据概览"
        ):

            st.markdown(
                f"""
- **数据行数**：{summary['行数']}
- **数据列数**：{summary['列数']}
- **缺失值**：{summary['缺失值']}
- **重复值**：{summary['重复值']}
- **数值字段数量**：{summary['数值列数']}
- **类别字段数量**：{summary['类别列数']}
"""
            )

        st.subheader(
            "AI数据分析对话"
        )

        for message in st.session_state.messages:

            with st.chat_message(
                message["role"]
            ):

                st.markdown(
                    message["content"]
                )

        question = st.chat_input(
            "请输入你的问题..."
        )

        if question:

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": question
                }
            )

            with st.chat_message(
                "user"
            ):

                st.markdown(question)

            chatbot = AIChat()

            try:

                answer = chatbot.ask(
                    question,
                    df
                )

            except Exception as e:

                answer = (
                    f"AI分析失败：{str(e)}"
                )

            with st.chat_message(
                "assistant"
            ):

                st.markdown(answer)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

    else:

        st.warning(
            "请先上传数据文件以开始分析"
        )