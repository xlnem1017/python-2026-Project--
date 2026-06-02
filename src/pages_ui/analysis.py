import streamlit as st
from core.analyzer import DataAnalyzer

def show_analysis_page():
    st.title("数据概览")

    if "df" not in st.session_state:
        st.warning("请先上传数据文件以开始分析")
        return

    df = st.session_state["df"]
    analyzer = DataAnalyzer()

    summary = analyzer.generate_summary(df)
    column_info = analyzer.get_column_info(df)
    numeric_desc = analyzer.describe_numeric(df)
    categorical_desc = analyzer.describe_categorical(df)

    st.subheader("总体数据概览")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("数据行数", summary["行数"])
    with col2:
        st.metric("数据列数", summary["列数"])
    with col3:
        st.metric("缺失值", summary["缺失值"])
    with col4:
        st.metric("重复值", summary["重复值"])

    st.divider()
    st.subheader("字段信息")
    for col, info in column_info.items():
        st.markdown(
            f"- **{col}** ({info['数据类型']}), 缺失值: {info['缺失值']}, 唯一值数: {info['唯一值数']}"
        )

    if not numeric_desc.empty:
        st.divider()
        st.subheader("数值字段描述统计")
        st.dataframe(numeric_desc, use_container_width=True)

    if categorical_desc:
        st.divider()
        st.subheader("类别字段描述统计")
        for col, desc in categorical_desc.items():
            st.markdown(
                f"- **{col}**: 唯一值数 {desc['唯一值数']}, 最高频值 {desc['最高频值']}, 频率 {desc['频率']}"
            )