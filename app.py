import streamlit as st
import plotly.express as px

from inference import (
    predict_all_cities,
    get_available_cities,
    get_available_positions,
    get_available_role_areas,
    get_available_key_skills,
    get_available_hard_skills,
    get_available_soft_skills,
    experience_id_from_years
)

st.set_page_config(
    page_title="AI Salary Prediction Platform",
    page_icon="💼",
    layout="wide"
)

# -------------------------
# LANGUAGE
# -------------------------
LANG = st.sidebar.selectbox("Language / Язык", ["English", "Русский"])

TEXT = {
    "English": {
        "profile_input": "Profile Input",
        "position": "Position",
        "role_area": "Role area",
        "experience_years": "Experience years",
        "schedule": "Schedule",
        "employment_type": "Employment type",
        "key_skills": "Key skills",
        "hard_skills": "Hard skills",
        "soft_skills": "Soft skills",
        "cities": "Cities",
        "all_cities": "All cities",
        "predict": "Generate salary forecast",
        "info": "Predictions will be generated for {n} cities using the same profile.",
        "error_position": "Enter a position",
        "error_skills": "Select at least one skill",
        "highest_city": "Best city",
        "highest_salary": "Top salary",
        "average_salary": "Average",
        "city_gap": "Gap",
        "range": "Range"
    },
    "Русский": {
        "profile_input": "Параметры",
        "position": "Должность",
        "role_area": "Область",
        "experience_years": "Опыт",
        "schedule": "График",
        "employment_type": "Занятость",
        "key_skills": "Ключевые навыки",
        "hard_skills": "Hard навыки",
        "soft_skills": "Soft навыки",
        "cities": "Города",
        "all_cities": "Все города",
        "predict": "Сделать прогноз",
        "info": "Прогноз для {n} городов",
        "error_position": "Введите должность",
        "error_skills": "Выберите навыки",
        "highest_city": "Лучший город",
        "highest_salary": "Макс зарплата",
        "average_salary": "Средняя",
        "city_gap": "Разница",
        "range": "Диапазон"
    }
}

T = TEXT[LANG]

# -------------------------
# STYLE (GLASSMORPHISM)
# -------------------------
st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #0f172a, #1e293b);
}

/* HEADER */
.top-header {
    padding: 25px;
    border-radius: 20px;
    backdrop-filter: blur(14px);
    background: rgba(255,255,255,0.08);
    margin-bottom: 20px;
}

.top-title {
    font-size: 34px;
    font-weight: 900;
    color: white;
}

.top-sub {
    font-size: 16px;
    color: #cbd5f5;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: #020617;
}

/* FIX TAGS */
[data-baseweb="tag"] {
    background: #38bdf8 !important;
    color: black !important;
    border-radius: 20px !important;
    padding: 4px 10px !important;
}

/* CARDS */
.metric-card {
    padding: 20px;
    border-radius: 18px;
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(12px);
    color: white;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# HEADER
# -------------------------
st.markdown("""
<div class="top-header">
    <div class="top-title">AI Salary Prediction Platform</div>
    <div class="top-sub">by Megatonn</div>
</div>
""", unsafe_allow_html=True)

# -------------------------
# LOAD DATA
# -------------------------
cities = get_available_cities()
positions = get_available_positions()
areas = get_available_role_areas()

key_sk = get_available_key_skills()
hard_sk = get_available_hard_skills()
soft_sk = get_available_soft_skills()

# -------------------------
# SIDEBAR INPUTS
# -------------------------
st.sidebar.header(T["profile_input"])

role_name = st.sidebar.selectbox(T["position"], positions)
role_area = st.sidebar.selectbox(T["role_area"], areas)

years = st.sidebar.slider(T["experience_years"], 0, 15, 2)
exp_id = experience_id_from_years(years)

schedule = st.sidebar.selectbox(T["schedule"], ["fullDay", "remote", "flexible", "shift"])
employment = st.
sidebar.selectbox(T["employment_type"], ["full", "part", "project"])

k = st.sidebar.multiselect(T["key_skills"], key_sk)
h = st.sidebar.multiselect(T["hard_skills"], hard_sk)
s = st.sidebar.multiselect(T["soft_skills"], soft_sk)

selected_cities = st.sidebar.multiselect(
    T["cities"],
    [T["all_cities"]] + cities,
    default=[T["all_cities"]]
)

if T["all_cities"] in selected_cities:
    selected_cities = cities

predict = st.sidebar.button(T["predict"])

# -------------------------
# INFO
# -------------------------
st.info(T["info"].format(n=len(selected_cities)))

# -------------------------
# PREDICTION
# -------------------------
if predict:

    if not role_name:
        st.error(T["error_position"])
        st.stop()

    if not k and not h and not s:
        st.error(T["error_skills"])
        st.stop()

    profile = {
        "role_name": role_name,
        "role_area": role_area,
        "experience_years": years,
        "experience_id": exp_id,
        "schedule_id": schedule,
        "employment_id": employment,
        "key_skills": ", ".join(k),
        "hard_skills": ", ".join(h),
        "soft_skills": ", ".join(s),
        "selected_cities": selected_cities
    }

    df = predict_all_cities(profile)

    df["predicted_salary"] = df["predicted_salary"].astype(int)

    # RANGE
    df["min"] = (df["predicted_salary"] * 0.85).astype(int)
    df["max"] = (df["predicted_salary"] * 1.15).astype(int)

    # METRICS
    top = df.iloc[0]
    bottom = df.iloc[-1]

    c1, c2, c3, c4 = st.columns(4)

    c1.markdown(f'<div class="metric-card">{top["city"]}</div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="metric-card">{top["predicted_salary"]}</div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="metric-card">{df["predicted_salary"].mean():.0f}</div>', unsafe_allow_html=True)
    c4.markdown(f'<div class="metric-card">{top["predicted_salary"] - bottom["predicted_salary"]}</div>', unsafe_allow_html=True)

    # CHART
    fig = px.bar(
        df,
        x="city",
        y="predicted_salary",
        error_y=df["max"] - df["predicted_salary"],
        error_y_minus=df["predicted_salary"] - df["min"],
        color="predicted_salary"
    )

    st.plotly_chart(fig, use_container_width=True)

    # TABLE
    st.dataframe(df)
