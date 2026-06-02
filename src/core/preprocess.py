import pandas as pd


class DataPreprocessor:

    def clean_data(self, df):

        df = df.copy()

        df.replace(
            ["?", "", " ", "NULL", "null", "NaN"],
            pd.NA,
            inplace=True
        )

        object_columns = (
            df.select_dtypes(
                include=["object"]
            ).columns
        )

        for col in object_columns:

            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
            )

        return df

    def fill_missing_values(self, df):

        df = df.copy()

        numeric_columns = (
            df.select_dtypes(
                include=[
                    "int64",
                    "float64"
                ]
            ).columns
        )

        categorical_columns = (
            df.select_dtypes(
                include=[
                    "object",
                    "category"
                ]
            ).columns
        )

        for col in numeric_columns:

            df[col] = df[col].fillna(
                df[col].median()
            )

        for col in categorical_columns:

            if not df[col].mode().empty:

                df[col] = df[col].fillna(
                    df[col].mode()[0]
                )

        return df

    def remove_duplicates(self, df):

        return df.drop_duplicates()

    def remove_empty_columns(self, df):

        return df.dropna(
            axis=1,
            how="all"
        )

    def get_missing_values(self, df):

        missing = (
            df.isnull()
            .sum()
        )

        return (
            missing[missing > 0]
            .sort_values(
                ascending=False
            )
            .to_dict()
        )

    def get_duplicate_count(self, df):

        return int(
            df.duplicated().sum()
        )

    def get_data_types(self, df):

        return {
            col: str(dtype)
            for col, dtype
            in df.dtypes.items()
        }

    def get_quality_report(self, df):

        return {

            "rows":
            int(df.shape[0]),

            "columns":
            int(df.shape[1]),

            "missing_values":
            int(
                df.isnull()
                .sum()
                .sum()
            ),

            "duplicates":
            int(
                df.duplicated()
                .sum()
            ),

            "numeric_columns":
            len(
                df.select_dtypes(
                    include=[
                        "int64",
                        "float64"
                    ]
                ).columns
            ),

            "categorical_columns":
            len(
                df.select_dtypes(
                    include=[
                        "object",
                        "category"
                    ]
                ).columns
            )
        }

    def process(self, df):

        df = self.clean_data(df)

        df = self.remove_empty_columns(
            df
        )

        df = self.fill_missing_values(
            df
        )

        df = self.remove_duplicates(
            df
        )

        return df