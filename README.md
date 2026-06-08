# Megatonn Salary Prediction App

AI-powered salary benchmarking platform developed for Megatonn.

## Project Goal

The platform estimates market-based salary ranges for selected job roles and cities using machine learning and labor market vacancy data.

## Business Context

Megatonn is expanding geographically and needs a data-driven tool to compare salary expectations across regions, especially for roles such as office, driver, warehouse, sales, and accountant.

## Model

Final model: LightGBM  
Target variable: average monthly salary in RUB  
Output: estimated salary range across selected cities

## Main Features

- Salary prediction across multiple cities
- One fixed candidate/job profile
- Estimated salary range
- City ranking
- Salary gap comparison
- CSV export
- Bilingual interface: English and Russian

## Main Inputs

- Position
- Role area
- Experience
- Schedule
- Employment type
- Key skills
- Hard skills
- Soft skills
- City

## How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
