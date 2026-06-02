import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class DataVisualizer:

    def __init__(self):
        sns.set_style("whitegrid")

    def plot_numeric_distribution(self, df, column):
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.histplot(data=df, x=column, bins=20, kde=True, ax=ax)
        ax.set_title(f"{column} 数值分布")
        ax.set_xlabel(column)
        ax.set_ylabel("数量")
        return fig

    def plot_numeric_boxplot(self, df, column):
        fig, ax = plt.subplots(figsize=(6, 5))
        sns.boxplot(x=df[column], ax=ax)
        ax.set_title(f"{column} 箱线图（异常值检测）")
        ax.set_xlabel(column)
        return fig

    def plot_categorical_distribution(self, df, column):
        fig, ax = plt.subplots(figsize=(10, 5))
        counts = df[column].value_counts().head(15)
        sns.barplot(x=counts.index, y=counts.values, ax=ax)
        ax.set_title(f"{column} 类别分布")
        ax.set_xlabel(column)
        ax.set_ylabel("数量")
        plt.xticks(rotation=45)
        return fig

    def plot_correlation_heatmap(self, df):
        numeric_df = df.select_dtypes(include=["int64", "float64"])
        if numeric_df.shape[1] < 2:
            return None
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(numeric_df.corr(), annot=True, cmap="Blues", ax=ax)
        ax.set_title("数值字段相关性热力图")
        return fig

    def get_numeric_columns(self, df):
        return df.select_dtypes(include=["int64", "float64"]).columns.tolist()

    def get_categorical_columns(self, df):
        return df.select_dtypes(include=["object", "category"]).columns.tolist()

    def plot_column(self, df, column):
        if column in self.get_numeric_columns(df):
            return self.plot_numeric_distribution(df, column)
        elif column in self.get_categorical_columns(df):
            return self.plot_categorical_distribution(df, column)
        else:
            return None

    def auto_plot_all(self, df):
        """
        自动生成所有字段图表，返回字典 {字段名: 图表fig}
        数值字段：直方图 + 箱线图
        类别字段：柱状图
        """
        figs = {}
        numeric_cols = self.get_numeric_columns(df)
        categorical_cols = self.get_categorical_columns(df)

        for col in numeric_cols:
            figs[f"{col}_直方图"] = self.plot_numeric_distribution(df, col)
            figs[f"{col}_箱线图"] = self.plot_numeric_boxplot(df, col)

        for col in categorical_cols:
            figs[f"{col}_柱状图"] = self.plot_categorical_distribution(df, col)

        heatmap_fig = self.plot_correlation_heatmap(df)
        if heatmap_fig:
            figs["相关性热力图"] = heatmap_fig

        return figs