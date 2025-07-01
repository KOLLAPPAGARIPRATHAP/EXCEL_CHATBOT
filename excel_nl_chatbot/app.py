# app.py

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from utils import clean_column_names, infer_column_types, clean_data_for_display, safe_serialize_dict
from llm_interface import ask_llm

# Streamlit page setup
st.set_page_config(page_title="📊 Excel NL Chatbot", layout="wide")

# Sidebar
st.sidebar.title("🛠️ Instructions")
st.sidebar.markdown(
    """
    1. Upload an Excel (.xlsx) file  
    2. View data preview & column types  
    3. Ask questions about your data in natural language  
    4. Visual charts will be shown when relevant  
    """
)
st.sidebar.markdown("---")
st.sidebar.markdown("Built with ❤️ using LLaMA 3 + Streamlit")

# Main title
st.title("📊 Excel-Based Natural Language Chatbot")

# File uploader
uploaded_file = st.file_uploader("Upload your Excel (.xlsx) file here", type=["xlsx"])

# Chart functions
def find_relevant_column(text, df):
    if not text:
        return None
    text_lower = str(text).lower()
    for col in df.columns:
        if str(col).lower() in text_lower:
            return col
    return None

def plot_histogram(df, column):
    plt.figure(figsize=(6, 2))
    sns.histplot(df[column].dropna(), bins=20, kde=False, color='skyblue')
    plt.title(f'Histogram of {column}')
    plt.xlabel(column)
    plt.ylabel('Frequency')
    st.pyplot(plt.gcf())
    plt.clf()

def plot_bar_chart(df, column):
    plt.figure(figsize=(6, 2))
    counts = df[column].value_counts().reset_index()
    sns.barplot(x=counts.iloc[:, 0], y=counts.iloc[:, 1], palette='viridis')
    plt.title(f'Bar Chart of {column}')
    plt.xlabel(column)
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    st.pyplot(plt.gcf())
    plt.clf()

# Main logic
if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        df = clean_column_names(df)
        display_df = clean_data_for_display(df.head())

        # Data preview in expander
        with st.expander("📄 Data Preview (click to expand)", expanded=True):
            st.dataframe(display_df)

        # Column types in expander
        with st.expander("📌 Inferred Column Types", expanded=False):
            col_types = infer_column_types(df)
            serializable_types = safe_serialize_dict(col_types)
            st.json(serializable_types)

        # User question input
        st.subheader("💬 Ask a Question about your Data")
        user_question = st.text_input("Type your question here and press Enter")

        if user_question:
            with st.spinner("Thinking... 🤔"):
                data_sample = clean_data_for_display(df.head(20)).to_csv(index=False)
                prompt = f"""
You are a data analyst assistant. The user has uploaded the following Excel data (first 20 rows shown below in CSV format):

{data_sample}

Column types are: {serializable_types}

Now answer the following question in simple terms, based only on the given data:

Question: {user_question}

If appropriate, provide statistics or comparisons. If visualisation is needed, suggest what kind of chart to show.
"""
                llm_response = ask_llm(prompt)
                st.subheader("📢 Answer")
                st.write(llm_response)

                # Detect chart type
                question_lower = user_question.lower()
                answer_lower = llm_response.lower()
                column_to_plot = find_relevant_column(user_question, df) or find_relevant_column(llm_response, df)

                if column_to_plot:
                    if "histogram" in question_lower or "histogram" in answer_lower:
                        plot_histogram(df, column_to_plot)
                    elif ("bar chart" in question_lower or "bar chart" in answer_lower
                          or "bar graph" in question_lower or "bar graph" in answer_lower):
                        plot_bar_chart(df, column_to_plot)

    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        st.stop()

else:
    st.info("Please upload an Excel file to begin.")

# Footer
st.markdown("---")
st.markdown("Made by Prathap | Powered by LLaMA 3 + Streamlit")
