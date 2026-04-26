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
        "uncertainty": "The salary range reflects model uncertainty. The predicted salary is the expected value, while the interval shows realistic variation depending on company, seniority interpretation, and market conditions.",
        "salary_comparison": "Salary Comparison with Estimated Range",
        "chart_title": "Predicted Salary by City with Uncertainty Range",
        "full_ranking": "City Ranking",
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
        "project_contract": "Project contract",
        "range": "Range",
        "selected": "Selected"
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
        "uncertainty": "Диапазон зарплаты отражает неопределенность модели. Прогноз зарплаты является ожидаемым значением, а интервал показывает реалистичную вариацию в зависимости от компании, интерпретации уровня опыта и рыночных условий.",
        "salary_comparison": "Сравнение зарплат с диапазоном",
        "chart_title": "Прогноз зарплаты по городам с диапазоном неопределенности",
        "full_ranking": "Рейтинг городов",
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
        "project_contract": "Проектный контракт",
        "range": "Диапазон",
        "selected": "Выбрано"
    }
}

T = TEXT[LANG]


st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(99,102,241,0.18), transparent 32%),
            radial-gradient(circle at top right, rgba(20,184,166,0.14), transparent 30%),
            linear-gradient(135deg, #f8fafc 0%, #eef2ff 45%, #f8fafc 100%);
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 4rem;
        max-width: 1480px;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #111827 0%, #172033 55%, #0f172a 100%);
        border-right: 1px solid rgba(255,255,255,0.08);
        width: 360px !important;
        min-width: 360px !important;
    }

    section[data-testid="stSidebar"] > div {
        width: 360px !important;
        min-width: 360px !important;
    }

    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #f8fafc !important;
    }

    section[data-testid="stSidebar"] input,
    section[data-testid="stSidebar"] textarea {
        color: #111827 !important;
        background-color: #ffffff !important;
        border-radius: 14px !important;
    }

    section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border-radius: 14px !important;
        color: #111827 !important;
        min-height: 46px !important;
        padding-left: 12px !important;
    }

    section[data-testid="stSidebar"] div[data-baseweb="select"] span {
        color: #111827 !important;
        font-weight: 650 !important;
    }

    section[data-testid="stSidebar"] div[data-baseweb="select"] input {
        color: #111827 !important;
    }

/* Make all select containers stop clipping content */
section[data-testid="stSidebar"] div[data-baseweb="select"],
section[data-testid="stSidebar"] div[data-baseweb="select"] * {
    overflow: visible !important;
}

/* Main select input box */
section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    border-radius: 14px !important;
    color: #111827 !important;
    min-height: 46px !important;
    padding-left: 18px !important;
    padding-right: 12px !important;
}

/* Selected tags */
section[data-testid="stSidebar"] [data-baseweb="tag"] {
    background-color: #e0f2fe !important;
    border: 1px solid #60a5fa !important;
    border-radius: 999px !important;
    color: #0f172a !important;

    margin-left: 12px !important;
    padding-left: 14px !important;
    padding-right: 8px !important;

    max-width: 245px !important;
    min-width: fit-content !important;

    display: inline-flex !important;
    align-items: center !important;

    transform: translateX(8px) !important;
}

/* Tag text */
section[data-testid="stSidebar"] [data-baseweb="tag"] span,
section[data-testid="stSidebar"] [data-baseweb="tag"] div {
    color: #0f172a !important;
    font-weight: 800 !important;
    white-space: nowrap !important;
    overflow: visible !important;
    text-overflow: clip !important;
}

/* X icon */
section[data-testid="stSidebar"] [data-baseweb="tag"] svg {
    fill: #0f172a !important;
    color: #0f172a !important;
    margin-left: 6px !important;
}

    section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
        color: #dbeafe !important;
        font-weight: 700 !important;
        line-height: 1.5 !important;
        margin-top: -8px !important;
        margin-bottom: 14px !important;
        font-size: 13px !important;
    }

    div[role="listbox"] {
        background-color: #ffffff !important;
    }

    div[role="option"] {
        color: #111827 !important;
        background-color: #ffffff !important;
    }

    div[role="option"] span {
        color: #111827 !important;
    }

    .hero {
        position: relative;
        overflow: hidden;
        padding: 42px 44px;
        border-radius: 34px;
        background:
            radial-gradient(circle at 18% 20%, rgba(255,255,255,0.25), transparent 22%),
            linear-gradient(135deg, #0f172a 0%, #312e81 42%, #0f766e 100%);
        color: white;
        box-shadow: 0px 28px 70px rgba(30, 41, 59, 0.26);
        margin-bottom: 28px;
    }

    .hero-badge {
        display: inline-block;
        padding: 9px 16px;
        border-radius: 999px;
        background: rgba(255,255,255,0.14);
        border: 1px solid rgba(255,255,255,0.22);
        font-size: 13px;
        font-weight: 700;
        margin-bottom: 18px;
        letter-spacing: 0.3px;
    }

    .hero-title {
        font-size: 50px;
        font-weight: 900;
        letter-spacing: -1.4px;
        margin-bottom: 6px;
        line-height: 1.04;
    }

    .hero-company {
        font-size: 25px;
        font-weight: 750;
        color: rgba(255,255,255,0.88);
        margin-bottom: 16px;
    }

    .hero-subtitle {
        font-size: 18px;
        max-width: 850px;
        color: rgba(255,255,255,0.84);
        line-height: 1.65;
    }

    .info-card {
        background: rgba(255,255,255,0.78);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(148, 163, 184, 0.28);
        border-radius: 22px;
        padding: 19px 23px;
        color: #334155;
        font-weight: 650;
        box-shadow: 0px 14px 34px rgba(15, 23, 42, 0.07);
        margin-bottom: 24px;
    }

    .metric-card {
        background: linear-gradient(180deg, rgba(255,255,255,0.98), rgba(255,255,255,0.88));
        border: 1px solid rgba(226,232,240,0.95);
        padding: 25px 24px;
        border-radius: 26px;
        box-shadow: 0px 18px 42px rgba(15,23,42,0.08);
        text-align: left;
        min-height: 142px;
    }

    .metric-title {
        font-size: 12px;
        color: #64748b;
        margin-bottom: 12px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.65px;
    }

    .metric-value {
        font-size: 29px;
        font-weight: 900;
        color: #111827;
        line-height: 1.14;
    }

    .metric-sub {
        font-size: 13px;
        color: #64748b;
        margin-top: 8px;
        font-weight: 700;
    }

    .section-title {
        font-size: 29px;
        font-weight: 900;
        color: #111827;
        margin-top: 36px;
        margin-bottom: 15px;
        letter-spacing: -0.55px;
    }

    .insight-card {
        padding: 23px 25px;
        background: linear-gradient(135deg, rgba(236,253,245,0.95) 0%, rgba(238,242,255,0.95) 100%);
        border: 1px solid rgba(20,184,166,0.24);
        border-radius: 24px;
        color: #064e3b;
        font-size: 16px;
        font-weight: 700;
        line-height: 1.65;
        box-shadow: 0px 16px 38px rgba(15,23,42,0.07);
    }

    .note-card {
        margin-top: 12px;
        padding: 17px 20px;
        background: rgba(255,255,255,0.72);
        border: 1px solid rgba(148,163,184,0.25);
        border-radius: 20px;
        color: #475569;
        font-size: 14px;
        font-weight: 600;
        line-height: 1.6;
    }

    .table-card {
        background: rgba(255,255,255,0.85);
        padding: 18px;
        border-radius: 26px;
        border: 1px solid rgba(226,232,240,0.95);
        box-shadow: 0px 18px 40px rgba(15,23,42,0.07);
    }

    .stButton>button {
        width: 100%;
        border-radius: 18px;
        height: 54px;
        font-weight: 850;
        background: linear-gradient(135deg, #4f46e5 0%, #0f766e 100%);
        color: white;
        border: none;
        box-shadow: 0px 14px 28px rgba(79,70,229,0.32);
    }

    .stButton>button:hover {
        background: linear-gradient(135deg, #4338ca 0%, #0d9488 100%);
        color: white;
        transform: translateY(-1px);
    }

    div[data-testid="stDataFrame"] {
        border-radius: 18px;
        overflow: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True
)


def show_selected(label, values):
    if values:
        st.sidebar.caption(f"{label}: " + ", ".join(values))


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

selected_key_skills = st.sidebar.multiselect(
    T["key_skills"],
    key_skill_options,
    placeholder=T["key_skills"]
)

selected_hard_skills = st.sidebar.multiselect(
    T["hard_skills"],
    hard_skill_options,
    placeholder=T["hard_skills"]
)


selected_soft_skills = st.sidebar.multiselect(
    T["soft_skills"],
    soft_skill_options,
    placeholder=T["soft_skills"]
)


city_options = [T["all_cities"]] + available_cities
selected_cities = st.sidebar.multiselect(
    T["cities"],
    city_options,
    default=[T["all_cities"]],
    placeholder=T["cities"]
)


predict_button = st.sidebar.button(T["predict"])

if T["all_cities"] in selected_cities or len(selected_cities) == 0:
    final_selected_cities = available_cities
else:
    final_selected_cities = selected_cities


st.markdown(
    f"""
    <div class="hero">
        <div class="hero-badge">AI Powered Market Salary Intelligence</div>
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

        UNCERTAINTY_RATE = 0.15

        results["predicted_salary"] = results["predicted_salary"].round(0).astype(int)
        results["salary_min"] = (results["predicted_salary"] * (1 - UNCERTAINTY_RATE)).round(0).astype(int)
        results["salary_max"] = (results["predicted_salary"] * (1 + UNCERTAINTY_RATE)).round(0).astype(int)
        results["error_plus"] = results["salary_max"] - results["predicted_salary"]
        results["error_minus"] = results["predicted_salary"] - results["salary_min"]

        results = results.sort_values("predicted_salary", ascending=False).reset_index(drop=True)

        top_city = results.iloc[0]
        bottom_city = results.iloc[-1]
        avg_salary = int(results["predicted_salary"].mean().round(0))
        salary_gap = int(top_city["predicted_salary"] - bottom_city["predicted_salary"])

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
                <div class="metric-sub">
                    {T["range"]}: {top_city["salary_min"]:,.0f} ₽ to {top_city["salary_max"]:,.0f} ₽
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        avg_min = int(avg_salary * 0.85)
        avg_max = int(avg_salary * 1.15)

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">{T["average_salary"]}</div>
                <div class="metric-value">{avg_salary:,.0f} ₽</div>
                <div class="metric-sub">
                    {T["range"]}: {avg_min:,.0f} ₽ to {avg_max:,.0f} ₽
                </div>
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

    st.markdown(
        f"""
        <div class="note-card">
            {T["uncertainty"]}
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
        color_continuous_scale=[
            [0.00, "#99f6e4"],
            [0.35, "#5eead4"],
            [0.65, "#818cf8"],
            [1.00, "#4f46e5"]
        ],
        error_y="error_plus",
        error_y_minus="error_minus"
    )

    fig.update_traces(
        texttemplate="%{text:,.0f} ₽",
        textposition="outside",
        marker_line_width=0,
        error_y=dict(
            thickness=1.6,
            width=7,
            color="#334155"
        ),
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Predicted: %{y:,.0f} ₽<br>"
            "Estimated range: %{customdata[0]:,.0f} ₽ to %{customdata[1]:,.0f} ₽"
            "<extra></extra>"
        ),
        customdata=results[["salary_min", "salary_max"]]
    )

    fig.update_layout(
        height=600,
        plot_bgcolor="rgba(255,255,255,0)",
        paper_bgcolor="rgba(255,255,255,0)",
        font=dict(family="Inter", size=14, color="#334155"),
        title=dict(font=dict(size=22, color="#111827")),
        xaxis=dict(title="", tickangle=-25, gridcolor="rgba(148,163,184,0.13)"),
        yaxis=dict(title="Predicted Salary, RUB", gridcolor="rgba(148,163,184,0.25)"),
        coloraxis_showscale=False,
        margin=dict(l=30, r=30, t=75, b=95),
        bargap=0.28
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f'<div class="section-title">{T["full_ranking"]}</div>', unsafe_allow_html=True)

    results_display = results[["city", "predicted_salary", "salary_min", "salary_max"]].copy()
    results_display.insert(0, "Rank", range(1, len(results_display) + 1))

    if LANG == "English":
        results_display = results_display.rename(columns={
            "city": "City",
            "predicted_salary": "Predicted Salary, RUB",
            "salary_min": "Estimated Min, RUB",
            "salary_max": "Estimated Max, RUB"
        })
    else:
        results_display = results_display.rename(columns={
            "city": "Город",
            "predicted_salary": "Прогноз зарплаты, руб.",
            "salary_min": "Минимальная оценка, руб.",
            "salary_max": "Максимальная оценка, руб."
        })

    st.markdown('<div class="table-card">', unsafe_allow_html=True)

    st.dataframe(
        results_display,
        use_container_width=True,
        hide_index=True
    )

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
