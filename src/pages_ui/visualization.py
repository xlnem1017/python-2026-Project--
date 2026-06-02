import streamlit as st
from core.visualizer import DataVisualizer

def show_visualization_page():

    st.title("📊 数据可视化分析")

    if "df" not in st.session_state:
        st.warning("请先上传数据文件")
        return

    df = st.session_state["df"]
    visualizer = DataVisualizer()

    numeric_columns = visualizer.get_numeric_columns(df)
    categorical_columns = visualizer.get_categorical_columns(df)

    st.subheader("字段概览")
    st.markdown(
        f"- 数值字段数量: {len(numeric_columns)}  \n"
        f"- 类别字段数量: {len(categorical_columns)}"
    )

    st.divider()
    st.subheader("自动生成图表")

    figures = visualizer.auto_plot_all(df)

    for title, fig in figures.items():
        st.markdown(f"### {title}")
        st.pyplot(fig)
        st.divider()

    st.subheader("手动选择字段查看单独图表")
    all_columns = numeric_columns + categorical_columns

    if len(all_columns) == 0:
        st.warning("没有可分析字段")
        return

    selected_column = st.selectbox("请选择字段", all_columns)
    fig = visualizer.plot_column(df, selected_column)
    if fig:
        st.pyplot(fig)

    st.divider()
    st.subheader("相关性热力图")
    heatmap_fig = visualizer.plot_correlation_heatmap(df)
    if heatmap_fig:
        st.pyplot(heatmap_fig)
    else:
        st.info("当前数据集数值字段不足，无法生成热力图。")