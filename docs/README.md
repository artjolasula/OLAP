Supermarket OLAP Dashboard

An interactive OLAP Dashboard built with Streamlit for analyzing supermarket sales data using multidimensional data analysis techniques.

The application supports classical OLAP operations (Slice, Dice, Drill-Down, Compare) and integrates an AI-powered assistant that allows users to query the dataset using natural language.

📌 Project Overview

This project demonstrates how OLAP concepts can be implemented programmatically using Python and Pandas within an interactive dashboard.

The dashboard allows users to:

Explore and preview the dataset

Perform multidimensional filtering

Analyze revenue by different dimensions

Compare sales across categories and months

Use an AI assistant to dynamically generate analysis code

The goal of this project is to combine:

Data analysis

Business intelligence concepts

Interactive visualization

Large Language Model (LLM) integration

🚀 Features
📊 Dataset Exploration

Dataset preview

Basic statistical summary

🔎 OLAP Operations
Slice

Filter data by:

Product Category

City

Dice

Filter data by multiple dimensions:

Category

City

Gender

Drill Down

Year → Month revenue analysis

Category → Payment Method breakdown

Compare

Compare revenue between two months

Compare revenue between two product categories

📈 Group & Summarize

Group by:

City

Gender

Product Category

Payment Method

Revenue visualization with bar charts

Average rating analysis

🤖 AI Data Assistant

Ask questions in natural language

AI generates Pandas code dynamically

Executes generated code

Automatically displays results

Powered by Groq API and Llama 3.3 model.