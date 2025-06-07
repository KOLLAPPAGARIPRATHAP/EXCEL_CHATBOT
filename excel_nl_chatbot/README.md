# Excel-Based Natural Language Chatbot

This project is a Streamlit app that lets users upload Excel files and ask natural language questions about the data. It uses a large language model (LLaMA 3 via Groq) to interpret questions and generate answers, and it can create simple visualizations like bar charts and histograms dynamically.

## Features

- Upload `.xlsx` Excel files
- Preview data and inferred column types
- Ask natural language questions about your data
- Automatic chart generation for histograms and bar charts
- Integration with LLaMA 3 model via Groq API for smart responses

## Installation

```bash
pip install -r requirements.txt

## Run the app with
streamlit run app.py
