import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Growth Mindset Challenge", layout="wide")

# Custom CSS
st.markdown(
    """
    <style>
    .stApp {
        background-color: black;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title And Description
st.title("Data Sweeper Web App Developed By Usama Muzammil")
st.write("Transform your CSV and Excel data cleaning with Data Sweeper App")

# Upload Files
uploaded_files = st.file_uploader("Upload your files (Accepts CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        try:
            if file_ext == ".csv":
                df = pd.read_csv(file)
            elif file_ext == ".xlsx":
                df = pd.read_excel(file)
            else:
                st.error(f"Unsupported file type: {file_ext}")
                continue
        except Exception as e:
            st.error(f"Error reading file {file.name}: {e}")
            continue

        # File Detail
        st.subheader(f"Preview of {file.name}")
        st.dataframe(df.head())

        # Data Cleaning Options
        st.subheader("Data Cleaning Options")
        clean_data = st.checkbox(f"Clean Data for {file.name}")

        if clean_data:
            col1, col2 = st.columns(2)

            if col1.button(f"Remove Duplicates from {file.name}"):
                df.drop_duplicates(inplace=True)
                st.success("Duplicates Removed!")

            if col2.button(f"Fill Missing Values for {file.name}"):
                numeric_cols = df.select_dtypes(include=['number']).columns
                if not numeric_cols.empty:
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("Missing Values Have Been Filled!")
                else:
                    st.warning("No numeric columns found to fill missing values.")

        # Column Selection
        st.subheader("Select Columns to Keep")
        columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
        if columns:
            df = df[columns]

        # Data Visualization
        st.subheader("Data Visualization")
        show_visualization = st.checkbox(f"Show Visualization for {file.name}")
        
        if show_visualization:
            numeric_cols = df.select_dtypes(include="number").columns
            if len(numeric_cols) >= 2:
                st.bar_chart(df[numeric_cols].iloc[:, :2])
            else:
                st.warning("Not enough numeric columns to visualize.")

        # Conversion Options
        st.subheader("Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            else:
                df.to_excel(buffer, index=False, engine='xlsxwriter')
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            
            buffer.seek(0)  # Reset buffer position
            
            st.download_button(
                label=f"Download {file_name}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )
