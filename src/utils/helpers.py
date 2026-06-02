import pandas as pd


def get_numeric_columns(
    df: pd.DataFrame
):

    return (
        df.select_dtypes(
            include=[
                "int64",
                "float64"
            ]
        )
        .columns
        .tolist()
    )


def get_categorical_columns(
    df: pd.DataFrame
):

    return (
        df.select_dtypes(
            include=[
                "object",
                "category"
            ]
        )
        .columns
        .tolist()
    )


def get_missing_summary(
    df: pd.DataFrame
):

    missing = (
        df.isnull()
        .sum()
    )

    return (
        missing[
            missing > 0
        ]
        .sort_values(
            ascending=False
        )
        .to_dict()
    )


def get_duplicate_count(
    df: pd.DataFrame
):

    return int(
        df.duplicated()
        .sum()
    )


def get_memory_usage(
    df: pd.DataFrame
):

    return round(
        df.memory_usage(
            deep=True
        ).sum()
        / 1024
        / 1024,
        2
    )


def get_column_types(
    df: pd.DataFrame
):

    return {
        col: str(dtype)
        for col, dtype
        in df.dtypes.items()
    }


def get_dataframe_summary(
    df: pd.DataFrame
):

    numeric_cols = (
        get_numeric_columns(df)
    )

    categorical_cols = (
        get_categorical_columns(df)
    )

    return {

        "行数":
        int(df.shape[0]),

        "列数":
        int(df.shape[1]),

        "数值列数":
        len(numeric_cols),

        "类别列数":
        len(categorical_cols),

        "缺失值":
        int(
            df.isnull()
            .sum()
            .sum()
        ),

        "重复值":
        get_duplicate_count(df),

        "内存占用(MB)":
        get_memory_usage(df),

        "数值字段":
        numeric_cols,

        "类别字段":
        categorical_cols
    }


def get_top_values(
    df: pd.DataFrame,
    top_n=5
):

    result = {}

    for col in df.columns:

        counts = (
            df[col]
            .value_counts()
            .head(top_n)
        )

        result[col] = (
            counts.to_dict()
        )

    return result