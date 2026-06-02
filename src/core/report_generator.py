from core.analyzer import DataAnalyzer


class ReportGenerator:

    def __init__(self):

        self.analyzer = DataAnalyzer()

    def generate_report(
        self,
        df
    ):

        summary = (
            self.analyzer
            .generate_summary(df)
        )

        numeric_desc = (
            self.analyzer
            .describe_numeric(df)
        )

        categorical_desc = (
            self.analyzer
            .describe_categorical(df)
        )

        report = []

        report.append(
            "AI数据分析报告"
        )

        report.append(
            "=" * 30
        )

        report.append(
            f"数据行数：{summary['行数']}"
        )

        report.append(
            f"数据列数：{summary['列数']}"
        )

        report.append(
            f"缺失值数量：{summary['缺失值']}"
        )

        report.append(
            f"重复值数量：{summary['重复值']}"
        )

        report.append(
            f"数值字段数量：{summary['数值列数']}"
        )

        report.append(
            f"类别字段数量：{summary['类别列数']}"
        )

        report.append("")

        report.append(
            "数据质量评估"
        )

        report.append(
            "-" * 20
        )

        if summary["缺失值"] == 0:

            report.append(
                "未发现缺失值。"
            )

        else:

            report.append(
                f"发现 {summary['缺失值']} 个缺失值，建议进一步处理。"
            )

        if summary["重复值"] == 0:

            report.append(
                "未发现重复记录。"
            )

        else:

            report.append(
                f"发现 {summary['重复值']} 条重复记录。"
            )

        report.append("")

        if not numeric_desc.empty:

            report.append(
                "数值字段分析"
            )

            report.append(
                "-" * 20
            )

            for column in numeric_desc.index:

                mean_value = round(
                    numeric_desc.loc[
                        column,
                        "平均值"
                    ],
                    2
                )

                report.append(
                    f"{column} 平均值：{mean_value}"
                )

            report.append("")

        if categorical_desc:

            report.append(
                "类别字段分析"
            )

            report.append(
                "-" * 20
            )

            for column, info in categorical_desc.items():

                report.append(
                    f"{column} 最常见值：{info['最高频值']}"
                )

            report.append("")

        report.append(
            "分析建议"
        )

        report.append(
            "-" * 20
        )

        report.append(
            "1. 重点关注缺失值较多的字段。"
        )

        report.append(
            "2. 查看相关性热力图发现潜在关系。"
        )

        report.append(
            "3. 对异常值进行进一步分析。"
        )

        report.append(
            "4. 根据业务场景建立预测模型。"
        )

        return "\n".join(
            report
        )