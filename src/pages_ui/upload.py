import streamlit as st

from core.data_loader import DataLoader
from core.preprocess import DataPreprocessor


def show_upload_page():

    st.title("Dataset Upload")

    uploaded_file = st.file_uploader(
        "Upload CSV File",
        type=["csv"]
    )

    if uploaded_file is not None:

        loader = DataLoader()
        preprocessor = DataPreprocessor()

        df = loader.load_csv(uploaded_file)

        df = preprocessor.clean_data(df)

        st.session_state["df"] = df

        st.success("Dataset Loaded Successfully")

        st.subheader("Dataset Preview")

        st.dataframe(
            df.head(10),
            use_container_width=True
        )

        st.subheader("Dataset Information")

        rows, cols = df.shape

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Rows",
                rows
            )

        with col2:
            st.metric(
                "Columns",
                cols
            )

        st.subheader("Column Names")

        st.write(
            df.columns.tolist()
        )

        missing_count = (
            df.isnull()
            .sum()
            .sum()
        )

        st.subheader("Missing Values")

        st.metric(
            "Total Missing Values",
            int(missing_count)
        )