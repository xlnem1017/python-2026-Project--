from core.analyzer import DataAnalyzer
from llm.llm_client import LLMClient
from core.deepseek_client import DeepSeekClient


class AIChat:

    def __init__(self):

        self.analyzer = DataAnalyzer()

        self.llm = LLMClient()

        self.deepseek = DeepSeekClient()

    def build_context(
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

        column_info = (
            self.analyzer
            .get_column_info(df)
        )

        correlation = (
            self.analyzer
            .correlation_matrix(df)
        )

        context = {

            "数据概览":
            summary,

            "字段信息":
            column_info,

            "数值统计":
            (
                numeric_desc
                .round(2)
                .to_dict()
            )
            if not numeric_desc.empty
            else {},

            "类别统计":
            categorical_desc,

            "相关性分析":
            (
                correlation
                .round(2)
                .to_dict()
            )
            if not correlation.empty
            else {},

            "样本数据":
            (
                df.head(20)
                .to_dict(
                    orient="records"
                )
            )
        }

        return context

    def ask(
        self,
        question,
        df
    ):

        context = self.build_context(
            df
        )

        try:

            answer = (
                self.llm
                .generate_response(
                    question,
                    context
                )
            )

            return answer

        except Exception as e:

            return (
                f"AI分析失败：{str(e)}"
            )

    def generate_dataset_analysis(
        self,
        df
    ):

        context = self.build_context(
            df
        )

        try:

            return (
                self.deepseek
                .analyze_dataframe(
                    context
                )
            )

        except Exception as e:

            return (
                f"DeepSeek分析失败：{str(e)}"
            )

    def get_summary(
        self,
        df
    ):

        return (
            self.analyzer
            .generate_summary(df)
        )

    def get_column_info(
        self,
        df
    ):

        return (
            self.analyzer
            .get_column_info(df)
        )

    def get_numeric_statistics(
        self,
        df
    ):

        return (
            self.analyzer
            .describe_numeric(df)
        )

    def get_categorical_statistics(
        self,
        df
    ):

        return (
            self.analyzer
            .describe_categorical(df)
        )