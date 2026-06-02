import pandas as pd


class DataLoader:

    def __init__(self):
        self.df = None

    def load_file(self, uploaded_file):

        file_name = uploaded_file.name.lower()

        if file_name.endswith(".csv"):

            self.df = self._load_csv(
                uploaded_file
            )

        elif file_name.endswith(
            (".xlsx", ".xls")
        ):

            self.df = pd.read_excel(
                uploaded_file
            )

        elif file_name.endswith(".json"):

            self.df = pd.read_json(
                uploaded_file
            )

        else:

            raise ValueError(
                "不支持的文件格式"
            )

        return self.df

    def _load_csv(
        self,
        uploaded_file
    ):

        encodings = [
            "utf-8",
            "utf-8-sig",
            "gbk",
            "gb2312",
            "latin1"
        ]

        for encoding in encodings:

            try:

                uploaded_file.seek(0)

                return pd.read_csv(
                    uploaded_file,
                    encoding=encoding,
                    skipinitialspace=True
                )

            except Exception:

                continue

        raise ValueError(
            "CSV文件读取失败"
        )

    def get_dataframe(self):

        return self.df

    def get_preview(
        self,
        rows=10
    ):

        if self.df is None:

            return None

        return self.df.head(rows)

    def get_shape(self):

        if self.df is None:

            return (0, 0)

        return self.df.shape

    def get_columns(self):

        if self.df is None:

            return []

        return (
            self.df.columns.tolist()
        )

    def get_numeric_columns(self):

        if self.df is None:

            return []

        return (
            self.df
            .select_dtypes(
                include=[
                    "int64",
                    "float64"
                ]
            )
            .columns
            .tolist()
        )

    def get_categorical_columns(self):

        if self.df is None:

            return []

        return (
            self.df
            .select_dtypes(
                include=[
                    "object",
                    "category"
                ]
            )
            .columns
            .tolist()
        )

    def get_basic_info(self):

        if self.df is None:

            return {}

        return {

            "rows":
            self.df.shape[0],

            "columns":
            self.df.shape[1],

            "numeric_columns":
            len(
                self.get_numeric_columns()
            ),

            "categorical_columns":
            len(
                self.get_categorical_columns()
            ),

            "memory_usage":
            round(
                self.df.memory_usage(
                    deep=True
                ).sum()
                / 1024
                / 1024,
                2
            )
        }