import pandas as pd
import numpy as np

class DataAnalyzer:

    def __init__(self):
        pass

    def generate_summary(self, df: pd.DataFrame):
        return {
            "行数": int(df.shape[0]),
            "列数": int(df.shape[1]),
            "缺失值": int(df.isnull().sum().sum()),
            "重复值": int(df.duplicated().sum()),
            "数值列数": len(self.numeric_columns(df)),
            "类别列数": len(self.categorical_columns(df))
        }

    def numeric_columns(self, df: pd.DataFrame):
        return df.select_dtypes(include=["int64", "float64"]).columns.tolist()

    def categorical_columns(self, df: pd.DataFrame):
        return df.select_dtypes(include=["object", "category"]).columns.tolist()

    def describe_numeric(self, df: pd.DataFrame):
        numeric_cols = self.numeric_columns(df)
        desc = df[numeric_cols].describe().T
        desc = desc.rename(
            columns={
                "count": "非空数量",
                "mean": "平均值",
                "std": "标准差",
                "min": "最小值",
                "25%": "25分位",
                "50%": "中位数",
                "75%": "75分位",
                "max": "最大值"
            }
        )
        return desc

    def describe_categorical(self, df: pd.DataFrame):
        cat_cols = self.categorical_columns(df)
        desc = {}
        for col in cat_cols:
            counts = df[col].value_counts()
            desc[col] = {
                "唯一值数": df[col].nunique(),
                "最高频值": counts.idxmax() if not counts.empty else None,
                "频率": int(counts.max()) if not counts.empty else None
            }
        return desc

    def get_column_info(self, df: pd.DataFrame):
        info = {}
        for col in df.columns:
            info[col] = {
                "数据类型": str(df[col].dtype),
                "缺失值": int(df[col].isnull().sum()),
                "唯一值数": int(df[col].nunique())
            }
        return info

    def top_values(self, df: pd.DataFrame, n=5):
        result = {}
        for col in df.columns:
            counts = df[col].value_counts().head(n)
            result[col] = counts.to_dict()
        return result

    def correlation_matrix(self, df: pd.DataFrame):
        numeric_cols = self.numeric_columns(df)
        if not numeric_cols:
            return pd.DataFrame()
        return df[numeric_cols].corr()

    # ---------- 新增方法 ----------
    def missing_details(self, df: pd.DataFrame):
        missing = df.isnull().sum()
        missing = missing[missing > 0].sort_values(ascending=False)
        return missing.to_dict()

    def detect_outliers(self, df: pd.DataFrame):
        result = {}
        for col in self.numeric_columns(df):
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            iqr = q3 - q1
            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr
            count = ((df[col] < lower) | (df[col] > upper)).sum()
            result[col] = int(count)
        return result

    def dataset_overview(self, df: pd.DataFrame):
        summary = self.generate_summary(df)
        return {
            "数据规模": f"{summary['行数']}行 × {summary['列数']}列",
            "数值字段": self.numeric_columns(df),
            "类别字段": self.categorical_columns(df),
            "缺失值详情": self.missing_details(df),
            "异常值统计": self.detect_outliers(df)
        }