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


st.markdown(
    '<div class="big-title">AI Salary Prediction Platform for Megatonn</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Enter one profile once and compare predicted salary across selected cities.</div>',
    unsafe_allow_html=True
)


available_cities = get_available_cities()


# =========================
# OPTIONS
# =========================

position_options = [
    "Data Analyst",
    "Business Analyst",
    "Product Manager",
    "Project Manager",
    "Python Developer",
    "Frontend Developer",
    "Backend Developer",
    "Data Scientist",
    "System Analyst",
    "HR Specialist",
    "Accountant",
    "Sales Manager",
    "Marketing Specialist",
    "Other"
]

role_area_options = [
    "Analytics",
    "IT",
    "Product",
    "Project Management",
    "HR",
    "Finance",
    "Sales",
    "Marketing",
    "Operations",
    "Other"
]

key_skill_options = [
    "python", "sql", "excel", "power bi", "tableau", "pandas", "numpy",
    "machine learning", "data analysis", "business analysis", "statistics",
    "dashboarding", "reporting", "project management", "product analytics",
    "crm", "1c", "git", "api", "english"
]

hard_skill_options = [
    "python", "sql", "excel", "power bi", "tableau", "pandas", "numpy",
    "machine learning", "scikit-learn", "lightgbm", "xgboost", "catboost",
    "statistics", "data visualization", "etl", "api", "git", "1c"
]

soft_skill_options = [
    "communication", "teamwork", "analytical thinking", "problem solving",
    "attention to detail", "adaptability", "leadership", "time management",
    "critical thinking", "stress resistance", "responsibility"
]

schedule_label_to_value = {
    "On-site": "fullDay",
    "Remote": "remote",
    "Hybrid": "flexible",
    "Shift": "shift"
}

employment_label_to_value = {
    "Full time": "full",
    "Part time": "part",
    "Project contract": "project"
}


def experience_id_from_years(years):
    if years == 0:
        return "noExperience"
    elif years <= 3:
        return "between1And3"
    elif years <= 6:
        return "between3And6"
    return "moreThan6"


# =========================
# SIDEBAR
# =========================

st.sidebar.header("Profile Input")

selected_position = st.sidebar.selectbox("Position", position_options)

if selected_position == "Other":
    role_name = st.sidebar.text_input("Write position", "")
else:
    role_name = selected_position.lower()

selected_role_area = st.sidebar.selectbox("Role area", role_area_options)

if selected_role_area == "Other":
    role_area = st.sidebar.text_input("Write role area", "")
else:
    role_area = selected_role_area.lower()

experience_years = st.sidebar.slider("Experience years", 0, 15, 2)
experience_id = experience_id_from_years(experience_years)

selected_schedule_label = st.sidebar.selectbox(
    "Schedule",
    list(schedule_label_to_value.keys())
)
schedule_id = schedule_label_to_value[selected_schedule_label]

selected_employment_label = st.sidebar.selectbox(
    "Employment type",
    list(employment_label_to_value.keys())
)
employment_id = employment_label_to_value[selected_employment_label]

selected_key_skills = st.sidebar.multiselect(
    "Key skills",
    key_skill_options,
    default=["python", "sql", "excel", "power bi"]
)

selected_hard_skills = st.sidebar.multiselect(
    "Hard skills",
    hard_skill_options,
    default=["python", "sql", "excel"]
)

selected_soft_skills = st.sidebar.multiselect(
    "Soft skills",
    soft_skill_options,
    default=["communication", "teamwork", "analytical thinking"]
)

city_options = ["All cities"] + available_cities

selected_cities = st.sidebar.multiselect(
    "Cities",
    city_options,
    default=["All cities"]
)

predict_button = st.sidebar.button("Predict salaries")


# =========================
# MAIN CONTENT
# =========================

if "All cities" in selected_cities or len(selected_cities) == 0:
    final_selected_cities = available_cities
else:
    final_selected_cities = selected_cities

st.info(
    f"The system will generate predictions for {len(final_selected_cities)} city/cities using the same profile."
)


if predict_button:

    with st.spinner("Calculating salary predictions..."):

        if not str(role_name).strip():
            st.error("Please enter or select a position before predicting.")
            st.stop()

        if not selected_key_skills and not selected_hard_skills and not selected_soft_skills:
            st.error("Please select at least one skill before predicting.")
            st.stop()

        user_profile = {
            "role_name": role_name,
            "role_area": role_area,
            "experience_years": experience_years,
            "experience_id": experience_id,
            "schedule_id": schedule_id,
            "employment_id": employment_id,
            "key_skills": ", ".join(selected_key_skills),
            "hard_skills": ", ".join(selected_hard_skills),
            "soft_skills": ", ".join(selected_soft_skills)
        }

        results = predict_all_cities(user_profile)

        results = results[results["city"].isin(final_selected_cities)]
        results = results.sort_values("predicted_salary", ascending=False).reset_index(drop=True)

        if results.empty:
            st.error("No city predictions available for the selected cities.")
            st.stop()

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
        st.markdown('<div class="section-title">Top Cities</div>', unsafe_allow_html=True)
        st.dataframe(results.head(10), use_container_width=True)

    with right:
        st.markdown('<div class="section-title">Lowest Cities</div>', unsafe_allow_html=True)
        st.dataframe(
            results.tail(10).sort_values("predicted_salary"),
            use_container_width=True
        )

    st.markdown('<div class="section-title">Salary Comparison by City</div>', unsafe_allow_html=True)

    chart_df = results.copy()

    fig = px.bar(
        chart_df,
        x="city",
        y="predicted_salary",
        text="predicted_salary",
        title="Predicted Salary by Selected City"
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
    results_display["predicted_salary"] = (
        results_display["predicted_salary"].round(0).astype(int)
    )

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
        Choose a position, role area, experience, schedule, employment type, skills, and cities.
        The system keeps the professional profile fixed and changes only the city.
        Then it compares predicted salaries across the selected locations.
        """
    )
