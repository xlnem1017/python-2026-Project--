import streamlit as st
import pandas as pd

from io import BytesIO

from core.report_generator import ReportGenerator
from core.analyzer import DataAnalyzer


def show_report_page():

    st.title("AI分析报告")

    if "df" not in st.session_state:

        st.warning(
            "请先上传数据文件"
        )

        return

    df = st.session_state["df"]

    generator = ReportGenerator()

    analyzer = DataAnalyzer()

    st.info(
        "系统将根据当前数据自动生成分析报告。"
    )

    if st.button(
        "生成AI分析报告"
    ):

        report = (
            generator
            .generate_report(df)
        )

        st.success(
            "报告生成成功"
        )

        st.subheader(
            "报告摘要"
        )

        lines = report.split("\n")

        summary_lines = lines[:12]

        st.markdown(
            "\n".join(summary_lines)
        )

        st.divider()

        st.subheader(
            "完整分析报告"
        )

        st.text_area(
            "报告内容",
            value=report,
            height=500
        )

        st.download_button(
            label="下载分析报告(TXT)",
            data=report,
            file_name="AI数据分析报告.txt",
            mime="text/plain"
        )

        st.divider()

        numeric_desc = (
            analyzer
            .describe_numeric(df)
        )

        if not numeric_desc.empty:

            csv_numeric = (
                numeric_desc
                .to_csv(
                    encoding="utf-8-sig"
                )
            )

            st.download_button(
                label="下载数值统计(CSV)",
                data=csv_numeric,
                file_name="数值字段统计.csv",
                mime="text/csv"
            )

        column_info = (
            analyzer
            .get_column_info(df)
        )

        info_df = pd.DataFrame(
            column_info
        ).T

        csv_info = (
            info_df
            .to_csv(
                encoding="utf-8-sig"
            )
        )

        st.download_button(
            label="下载字段信息(CSV)",
            data=csv_info,
            file_name="字段信息统计.csv",
            mime="text/csv"
        )

        st.divider()

        excel_buffer = BytesIO()

        with pd.ExcelWriter(
            excel_buffer,
            engine="xlsxwriter"
        ) as writer:

            df.to_excel(
                writer,
                sheet_name="原始数据",
                index=False
            )

            if not numeric_desc.empty:

                numeric_desc.to_excel(
                    writer,
                    sheet_name="数值统计"
                )

            info_df.to_excel(
                writer,
                sheet_name="字段信息"
            )

        excel_buffer.seek(0)

        st.download_button(
            label="下载分析报告(Excel)",
            data=excel_buffer,
            file_name="AI数据分析报告.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        st.divider()

        st.subheader(
            "导出说明"
        )

        st.markdown(
            """
- TXT：完整AI分析报告

- Excel：原始数据 + 数值统计 + 字段信息

- 数值统计CSV：均值、最大值、最小值等统计结果

- 字段信息CSV：字段类型、缺失值、唯一值数量

适用于课程作业提交、实验报告和后续分析。
"""
        )