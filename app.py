import streamlit as st
import pandas as pd
import plotly.express as px

from inference import predict_all_cities, get_available_cities


st.set_page_config(
    page_title="Megatonn Salary Prediction Platform",
    page_icon="💼",
    layout="wide"
)


st.markdown(
    """
    <style>
    .main {
        background-color: #f7f9fc;
    }

    .big-title {
        font-size: 42px;
        font-weight: 800;
        color: #1f2937;
        margin-bottom: 0px;
    }

    .subtitle {
        font-size: 18px;
        color: #6b7280;
        margin-bottom: 30px;
    }

    .metric-card {
        background-color: white;
        padding: 22px;
        border-radius: 18px;
        box-shadow: 0px 4px 16px rgba(0,0,0,0.06);
        text-align: center;
    }

    .metric-title {
        font-size: 14px;
        color: #6b7280;
        margin-bottom: 8px;
    }

    .metric-value {
        font-size: 28px;
        font-weight: 800;
        color: #111827;
    }

    .section-title {
        font-size: 24px;
        font-weight: 700;
        color: #111827;
        margin-top: 25px;
        margin-bottom: 10px;
    }

    .stButton>button {
        width: 100%;
        border-radius: 14px;
        height: 48px;
        font-weight: 700;
        background-color: #2563eb;
        color: white;
        border: none;
    }

    .stButton>button:hover {
        background-color: #1d4ed8;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)



st.markdown('<div class="big-title">AI Salary Prediction Platform for Megatonn</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Enter one profile once and compare predicted salary across all cities in the dataset.</div>',
    unsafe_allow_html=True
)



st.sidebar.header("Profile Input")

role_name = st.sidebar.text_input("Position", "data analyst")
role_area = st.sidebar.text_input("Role area", "analytics")

experience_years = st.sidebar.slider("Experience years", 0, 15, 2)

experience_id = st.sidebar.selectbox(
    "Experience category",
    ["noExperience", "between1And3", "between3And6", "moreThan6"]
)

schedule_id = st.sidebar.selectbox(
    "Schedule",
    ["fullDay", "remote", "flexible", "shift"]
)

employment_id = st.sidebar.selectbox(
    "Employment type",
    ["full", "part", "project"]
)

key_skills = st.sidebar.text_area(
    "Key skills",
    "python, sql, excel, power bi"
)

hard_skills = st.sidebar.text_area(
    "Hard skills",
    "python, sql, excel"
)

soft_skills = st.sidebar.text_area(
    "Soft skills",
    "communication, teamwork, analytical thinking"
)

predict_button = st.sidebar.button("Predict salaries")



available_cities = get_available_cities()

st.info(
    f"The system will generate predictions for {len(available_cities)} cities using the same profile."
)

if predict_button:

    user_profile = {
        "role_name": role_name,
        "role_area": role_area,
        "experience_years": experience_years,
        "experience_id": experience_id,
        "schedule_id": schedule_id,
        "employment_id": employment_id,
        "key_skills": key_skills,
        "hard_skills": hard_skills,
        "soft_skills": soft_skills
    }

    results = predict_all_cities(user_profile)

    top_city = results.iloc[0]
    bottom_city = results.iloc[-1]
    avg_salary = results["predicted_salary"].mean()
    salary_gap = top_city["predicted_salary"] - bottom_city["predicted_salary"]


    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Highest city</div>
                <div class="metric-value">{top_city["city"]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Highest salary</div>
                <div class="metric-value">{top_city["predicted_salary"]:,.0f} ₽</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Average salary</div>
                <div class="metric-value">{avg_salary:,.0f} ₽</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">City salary gap</div>
                <div class="metric-value">{salary_gap:,.0f} ₽</div>
            </div>
            """,
            unsafe_allow_html=True
        )

  

    st.markdown('<div class="section-title">Main Insight</div>', unsafe_allow_html=True)

    st.success(
        f"For the same profile, the highest predicted salary is in {top_city['city']} "
        f"with {top_city['predicted_salary']:,.0f} ₽, while the lowest predicted salary is in "
        f"{bottom_city['city']} with {bottom_city['predicted_salary']:,.0f} ₽."
    )

 

    left, right = st.columns(2)

    with left:
        st.markdown('<div class="section-title">Top 10 Cities</div>', unsafe_allow_html=True)
        st.dataframe(results.head(10), use_container_width=True)

    with right:
        st.markdown('<div class="section-title">Lowest 10 Cities</div>', unsafe_allow_html=True)
        st.dataframe(results.tail(10).sort_values("predicted_salary"), use_container_width=True)



    st.markdown('<div class="section-title">Salary Comparison by City</div>', unsafe_allow_html=True)

    top_chart = results.head(20).copy()

    fig = px.bar(
        top_chart,
        x="city",
        y="predicted_salary",
        text="predicted_salary",
        title="Top 20 Cities by Predicted Salary"
    )

    fig.update_traces(
        texttemplate="%{text:,.0f} ₽",
        textposition="outside"
    )

    fig.update_layout(
        xaxis_title="City",
        yaxis_title="Predicted Salary, RUB",
        height=550,
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)


    st.markdown('<div class="section-title">Full City Ranking</div>', unsafe_allow_html=True)

    results_display = results.copy()
    results_display["predicted_salary"] = results_display["predicted_salary"].round(0).astype(int)

    st.dataframe(results_display, use_container_width=True)

    csv = results_display.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download results as CSV",
        data=csv,
        file_name="salary_predictions_by_city.csv",
        mime="text/csv"
    )

else:
    st.markdown('<div class="section-title">How it works</div>', unsafe_allow_html=True)

    st.write(
        """
        1. Enter one professional profile in the sidebar.
        2. The system keeps the profile fixed.
        3. The model automatically changes only the city.
        4. The platform predicts salary for every city in the dataset.
        5. Results are shown as rankings, tables, and visual comparisons.
        """
    )
