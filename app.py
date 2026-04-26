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
    page_title="Megatonn Salary Prediction Platform",
    page_icon="💼",
    layout="wide"
)


# =========================
# LANGUAGE
# =========================

LANG = st.sidebar.selectbox("Language / Язык", ["English", "Русский"])

TEXT = {
    "English": {
        "title": "AI Salary Prediction Platform",
        "company": "for Megatonn",
        "subtitle": "Compare how the same professional profile is valued across different cities.",
        "profile_input": "Profile Input",
        "position": "Position",
        "write_position": "Write position",
        "role_area": "Role area",
        "write_role_area": "Write role area",
        "experience_years": "Experience years",
        "schedule": "Schedule",
        "employment_type": "Employment type",
        "key_skills": "Key skills",
        "hard_skills": "Hard skills",
        "soft_skills": "Soft skills",
        "cities": "Cities",
        "all_cities": "All cities",
        "predict": "Generate salary forecast",
        "info": "Forecast will be generated for {n} city/cities using one fixed profile.",
        "spinner": "Calculating salary predictions...",
        "error_position": "Please enter or select a position before predicting.",
        "error_skills": "Please select at least one skill before predicting.",
        "highest_city": "Best city",
        "highest_salary": "Highest salary",
        "average_salary": "Average salary",
        "city_gap": "Salary gap",
        "main_insight": "Main Insight",
        "insight": "For the same profile, the strongest salary forecast is in {top_city}: {top_salary:,.0f} ₽. The lowest forecast is in {bottom_city}: {bottom_salary:,.0f} ₽.",
        "top_cities": "Top Cities",
        "lowest_cities": "Lowest Cities",
        "salary_comparison": "Salary Comparison",
        "chart_title": "Predicted Salary by City",
        "full_ranking": "Full City Ranking",
        "download": "Download results as CSV",
        "how_it_works": "How it works",
        "how_text": "Select a position, skills, employment conditions and cities. The model keeps the profile fixed and changes only the city.",
        "other": "Other",
        "on_site": "On-site",
        "remote": "Remote",
        "hybrid": "Hybrid",
        "shift": "Shift",
        "full_time": "Full time",
        "part_time": "Part time",
        "project_contract": "Project contract"
    },
    "Русский": {
        "title": "AI-платформа прогнозирования зарплат",
        "company": "для Megatonn",
        "subtitle": "Сравните, как один и тот же профессиональный профиль оценивается в разных городах.",
        "profile_input": "Параметры профиля",
        "position": "Должность",
        "write_position": "Введите должность",
        "role_area": "Профессиональная область",
        "write_role_area": "Введите профессиональную область",
        "experience_years": "Опыт работы, лет",
        "schedule": "Формат работы",
        "employment_type": "Тип занятости",
        "key_skills": "Ключевые навыки",
        "hard_skills": "Профессиональные навыки",
        "soft_skills": "Гибкие навыки",
        "cities": "Города",
        "all_cities": "Все города",
        "predict": "Сформировать прогноз",
        "info": "Прогноз будет рассчитан для {n} городов с использованием одного фиксированного профиля.",
        "spinner": "Расчет прогнозов зарплаты...",
        "error_position": "Пожалуйста, выберите или введите должность перед расчетом.",
        "error_skills": "Пожалуйста, выберите хотя бы один навык перед расчетом.",
        "highest_city": "Лучший город",
        "highest_salary": "Максимальная зарплата",
        "average_salary": "Средняя зарплата",
        "city_gap": "Разница зарплат",
        "main_insight": "Главный вывод",
        "insight": "Для одного и того же профиля самый высокий прогноз зарплаты в городе {top_city}: {top_salary:,.0f} ₽. Самый низкий прогноз в городе {bottom_city}: {bottom_salary:,.0f} ₽.",
        "top_cities": "Топ городов",
        "lowest_cities": "Города с минимальной зарплатой",
        "salary_comparison": "Сравнение зарплат",
        "chart_title": "Прогноз зарплаты по городам",
        "full_ranking": "Полный рейтинг городов",
        "download": "Скачать результаты в CSV",
        "how_it_works": "Как это работает",
        "how_text": "Выберите должность, навыки, условия занятости и города. Модель фиксирует профиль и меняет только город.",
        "other": "Другое",
        "on_site": "Офис",
        "remote": "Удаленно",
        "hybrid": "Гибрид",
        "shift": "Сменный график",
        "full_time": "Полная занятость",
        "part_time": "Частичная занятость",
        "project_contract": "Проектный контракт"
    }
}

T = TEXT[LANG]


# =========================
# CSS
# =========================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #eef4ff 45%, #f8fafc 100%);
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #111827 100%);
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    section[data-testid="stSidebar"] * {
        color: #f9fafb;
    }

    section[data-testid="stSidebar"] input,
    section[data-testid="stSidebar"] textarea,
    section[data-testid="stSidebar"] div[data-baseweb="select"] {
        color: #111827 !important;
    }

    .hero {
        padding: 34px 36px;
        border-radius: 28px;
        background: linear-gradient(135deg, #111827 0%, #1e3a8a 55%, #2563eb 100%);
        color: white;
        box-shadow: 0px 22px 50px rgba(37, 99, 235, 0.24);
        margin-bottom: 28px;
    }

    .hero-badge {
        display: inline-block;
        padding: 8px 14px;
        border-radius: 999px;
        background: rgba(255,255,255,0.14);
        border: 1px solid rgba(255,255,255,0.20);
        font-size: 13px;
        font-weight: 600;
        margin-bottom: 16px;
    }

    .hero-title {
        font-size: 46px;
        font-weight: 850;
        letter-spacing: -1.2px;
        margin-bottom: 4px;
        line-height: 1.05;
    }

    .hero-company {
        font-size: 24px;
        font-weight: 700;
        opacity: 0.92;
        margin-bottom: 14px;
    }

    .hero-subtitle {
        font-size: 18px;
        max-width: 820px;
        color: rgba(255,255,255,0.86);
        line-height: 1.6;
    }

    .info-card {
        background: rgba(255,255,255,0.82);
        backdrop-filter: blur(14px);
        border: 1px solid rgba(148, 163, 184, 0.28);
        border-radius: 20px;
        padding: 18px 22px;
        color: #1e3a8a;
        font-weight: 600;
        box-shadow: 0px 12px 30px rgba(15, 23, 42, 0.06);
        margin-bottom: 24px;
    }

    .metric-card {
        background: rgba(255,255,255,0.92);
        border: 1px solid rgba(226,232,240,0.9);
        padding: 24px 22px;
        border-radius: 24px;
        box-shadow: 0px 18px 36px rgba(15,23,42,0.08);
        text-align: left;
        min-height: 126px;
    }

    .metric-title {
        font-size: 13px;
        color: #64748b;
        margin-bottom: 10px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.4px;
    }

    .metric-value {
        font-size: 28px;
        font-weight: 850;
        color: #0f172a;
        line-height: 1.15;
    }

    .section-title {
        font-size: 27px;
        font-weight: 850;
        color: #0f172a;
        margin-top: 34px;
        margin-bottom: 14px;
        letter-spacing: -0.4px;
    }

    .insight-card {
        padding: 22px 24px;
        background: linear-gradient(135deg, #ecfdf5 0%, #dbeafe 100%);
        border: 1px solid rgba(34,197,94,0.22);
        border-radius: 22px;
        color: #064e3b;
        font-size: 16px;
        font-weight: 600;
        box-shadow: 0px 14px 32px rgba(15,23,42,0.06);
    }

    .table-card {
        background: rgba(255,255,255,0.88);
        padding: 18px;
        border-radius: 24px;
        border: 1px solid rgba(226,232,240,0.9);
        box-shadow: 0px 16px 34px rgba(15,23,42,0.06);
    }

    .stButton>button {
        width: 100%;
        border-radius: 16px;
        height: 52px;
        font-weight: 800;
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: white;
        border: none;
        box-shadow: 0px 12px 24px rgba(37,99,235,0.32);
    }

    .stButton>button:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
        color: white;
        transform: translateY(-1px);
    }

    div[data-testid="stDataFrame"] {
        border-radius: 18px;
        overflow: hidden;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1450px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# =========================
# DATA OPTIONS
# =========================

available_cities = get_available_cities()
available_positions = get_available_positions()
available_role_areas = get_available_role_areas()

key_skill_options = get_available_key_skills()
hard_skill_options = get_available_hard_skills()
soft_skill_options = get_available_soft_skills()

schedule_label_to_value = {
    T["on_site"]: "fullDay",
    T["remote"]: "remote",
    T["hybrid"]: "flexible",
    T["shift"]: "shift"
}

employment_label_to_value = {
    T["full_time"]: "full",
    T["part_time"]: "part",
    T["project_contract"]: "project"
}


# =========================
# SIDEBAR
# =========================

st.sidebar.header(T["profile_input"])

position_options = available_positions + [T["other"]]
selected_position = st.sidebar.selectbox(T["position"], position_options)

if selected_position == T["other"]:
    role_name = st.sidebar.text_input(T["write_position"], "")
else:
    role_name = selected_position

role_area_options = available_role_areas + [T["other"]]
selected_role_area = st.sidebar.selectbox(T["role_area"], role_area_options)

if selected_role_area == T["other"]:
    role_area = st.sidebar.text_input(T["write_role_area"], "")
else:
    role_area = selected_role_area

experience_years = st.sidebar.slider(T["experience_years"], 0, 15, 2)
experience_id = experience_id_from_years(experience_years)

selected_schedule_label = st.sidebar.selectbox(T["schedule"], list(schedule_label_to_value.keys()))
schedule_id = schedule_label_to_value[selected_schedule_label]

selected_employment_label = st.sidebar.selectbox(T["employment_type"], list(employment_label_to_value.keys()))
employment_id = employment_label_to_value[selected_employment_label]

selected_key_skills = st.sidebar.multiselect(T["key_skills"], key_skill_options)
selected_hard_skills = st.sidebar.multiselect(T["hard_skills"], hard_skill_options)
selected_soft_skills = st.sidebar.multiselect(T["soft_skills"], soft_skill_options)

city_options = [T["all_cities"]] + available_cities

selected_cities = st.sidebar.multiselect(
    T["cities"],
    city_options,
    default=[T["all_cities"]]
)

predict_button = st.sidebar.button(T["predict"])

if T["all_cities"] in selected_cities or len(selected_cities) == 0:
    final_selected_cities = available_cities
else:
    final_selected_cities = selected_cities


# =========================
# HERO
# =========================

st.markdown(
    f"""
    <div class="hero">
        <div class="hero-badge">Machine Learning Salary Intelligence</div>
        <div class="hero-title">{T["title"]}</div>
        <div class="hero-company">{T["company"]}</div>
        <div class="hero-subtitle">{T["subtitle"]}</div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="info-card">
        {T["info"].format(n=len(final_selected_cities))}
    </div>
    """,
    unsafe_allow_html=True
)


# =========================
# MAIN
# =========================

if predict_button:

    with st.spinner(T["spinner"]):

        if not str(role_name).strip():
            st.error(T["error_position"])
            st.stop()

        if not selected_key_skills and not selected_hard_skills and not selected_soft_skills:
            st.error(T["error_skills"])
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
            "soft_skills": ", ".join(selected_soft_skills),
            "selected_cities": final_selected_cities
        }

        results = predict_all_cities(user_profile)

        if results.empty:
            st.error("No predictions available.")
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
                <div class="metric-title">{T["highest_city"]}</div>
                <div class="metric-value">{top_city["city"]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">{T["highest_salary"]}</div>
                <div class="metric-value">{top_city["predicted_salary"]:,.0f} ₽</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">{T["average_salary"]}</div>
                <div class="metric-value">{avg_salary:,.0f} ₽</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">{T["city_gap"]}</div>
                <div class="metric-value">{salary_gap:,.0f} ₽</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(f'<div class="section-title">{T["main_insight"]}</div>', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="insight-card">
            {T["insight"].format(
                top_city=top_city["city"],
                top_salary=top_city["predicted_salary"],
                bottom_city=bottom_city["city"],
                bottom_salary=bottom_city["predicted_salary"]
            )}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(f'<div class="section-title">{T["salary_comparison"]}</div>', unsafe_allow_html=True)

    fig = px.bar(
        results,
        x="city",
        y="predicted_salary",
        text="predicted_salary",
        title=T["chart_title"],
        color="predicted_salary",
        color_continuous_scale="Blues"
    )

    fig.update_traces(
        texttemplate="%{text:,.0f} ₽",
        textposition="outside",
        marker_line_width=0,
        hovertemplate="<b>%{x}</b><br>%{y:,.0f} ₽<extra></extra>"
    )

    fig.update_layout(
        height=560,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", size=14, color="#334155"),
        title=dict(font=dict(size=20, color="#0f172a")),
        xaxis=dict(title="", tickangle=-25, gridcolor="rgba(148,163,184,0.15)"),
        yaxis=dict(title="Predicted Salary, RUB", gridcolor="rgba(148,163,184,0.25)"),
        coloraxis_showscale=False,
        margin=dict(l=30, r=30, t=70, b=90)
    )

    st.plotly_chart(fig, use_container_width=True)

    left, right = st.columns(2)

    with left:
        st.markdown(f'<div class="section-title">{T["top_cities"]}</div>', unsafe_allow_html=True)
        st.markdown('<div class="table-card">', unsafe_allow_html=True)
        st.dataframe(
            results.head(10).round({"predicted_salary": 0}),
            use_container_width=True,
            hide_index=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        st.markdown(f'<div class="section-title">{T["lowest_cities"]}</div>', unsafe_allow_html=True)
        st.markdown('<div class="table-card">', unsafe_allow_html=True)
        st.dataframe(
            results.tail(10).sort_values("predicted_salary").round({"predicted_salary": 0}),
            use_container_width=True,
            hide_index=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="section-title">{T["full_ranking"]}</div>', unsafe_allow_html=True)

    results_display = results.copy()
    results_display["predicted_salary"] = results_display["predicted_salary"].round(0).astype(int)

    st.markdown('<div class="table-card">', unsafe_allow_html=True)
    st.dataframe(results_display, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

    csv = results_display.to_csv(index=False).encode("utf-8")

    st.download_button(
        label=T["download"],
        data=csv,
        file_name="salary_predictions_by_city.csv",
        mime="text/csv"
    )

else:
    st.markdown(f'<div class="section-title">{T["how_it_works"]}</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="insight-card">
            {T["how_text"]}
        </div>
        """,
        unsafe_allow_html=True
    )
