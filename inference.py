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
        "title": "AI Salary Prediction Platform for Megatonn",
        "subtitle": "Enter one profile once and compare predicted salary across selected cities.",
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
        "predict": "Predict salaries",
        "info": "The system will generate predictions for {n} city/cities using the same profile.",
        "spinner": "Calculating salary predictions...",
        "error_position": "Please enter or select a position before predicting.",
        "error_skills": "Please select at least one skill before predicting.",
        "error_no_predictions": "No predictions available for the selected cities.",
        "highest_city": "Highest city",
        "highest_salary": "Highest salary",
        "average_salary": "Average salary",
        "city_gap": "City salary gap",
        "main_insight": "Main Insight",
        "insight": "For the same profile, the highest predicted salary is in {top_city} with {top_salary:,.0f} ₽, while the lowest predicted salary is in {bottom_city} with {bottom_salary:,.0f} ₽.",
        "top_cities": "Top Cities",
        "lowest_cities": "Lowest Cities",
        "salary_comparison": "Salary Comparison by City",
        "chart_title": "Predicted Salary by Selected City",
        "xaxis": "City",
        "yaxis": "Predicted Salary, RUB",
        "full_ranking": "Full City Ranking",
        "download": "Download results as CSV",
        "how_it_works": "How it works",
        "how_text": "Choose a position, role area, experience, schedule, employment type, skills, and cities. The system keeps the professional profile fixed and changes only the city. Then it compares predicted salaries across the selected locations.",
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
        "title": "AI-платформа прогнозирования зарплат для Megatonn",
        "subtitle": "Введите профиль один раз и сравните прогноз зарплаты по выбранным городам.",
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
        "predict": "Рассчитать зарплаты",
        "info": "Система рассчитает прогноз для {n} городов с использованием одного и того же профиля.",
        "spinner": "Расчет прогнозов зарплаты...",
        "error_position": "Пожалуйста, выберите или введите должность перед расчетом.",
        "error_skills": "Пожалуйста, выберите хотя бы один навык перед расчетом.",
        "error_no_predictions": "Для выбранных городов нет доступных прогнозов.",
        "highest_city": "Город с максимумом",
        "highest_salary": "Максимальная зарплата",
        "average_salary": "Средняя зарплата",
        "city_gap": "Разница между городами",
        "main_insight": "Главный вывод",
        "insight": "Для одного и того же профиля самый высокий прогноз зарплаты в городе {top_city}: {top_salary:,.0f} ₽, а самый низкий прогноз в городе {bottom_city}: {bottom_salary:,.0f} ₽.",
        "top_cities": "Топ городов",
        "lowest_cities": "Города с минимальной зарплатой",
        "salary_comparison": "Сравнение зарплат по городам",
        "chart_title": "Прогноз зарплаты по выбранным городам",
        "xaxis": "Город",
        "yaxis": "Прогноз зарплаты, руб.",
        "full_ranking": "Полный рейтинг городов",
        "download": "Скачать результаты в CSV",
        "how_it_works": "Как это работает",
        "how_text": "Выберите должность, профессиональную область, опыт, формат работы, тип занятости, навыки и города. Система фиксирует профессиональный профиль и меняет только город. После этого она сравнивает прогноз зарплаты по выбранным локациям.",
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


# =========================
# HEADER
# =========================

st.markdown(
    f'<div class="big-title">{T["title"]}</div>',
    unsafe_allow_html=True
)

st.markdown(
    f'<div class="subtitle">{T["subtitle"]}</div>',
    unsafe_allow_html=True
)


# =========================
# LOAD OPTIONS FROM PKL
# =========================

available_cities = get_available_cities()
available_positions = get_available_positions()
available_role_areas = get_available_role_areas()

key_skill_options = get_available_key_skills()
hard_skill_options = get_available_hard_skills()
soft_skill_options = get_available_soft_skills()


# =========================
# INTERNAL VALUE MAPPINGS
# =========================

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


selected_schedule_label = st.sidebar.selectbox(
    T["schedule"],
    list(schedule_label_to_value.keys())
)
schedule_id = schedule_label_to_value[selected_schedule_label]


selected_employment_label = st.sidebar.selectbox(
    T["employment_type"],
    list(employment_label_to_value.keys())
)
employment_id = employment_label_to_value[selected_employment_label]


selected_key_skills = st.sidebar.multiselect(
    T["key_skills"],
    key_skill_options
)

selected_hard_skills = st.sidebar.multiselect(
    T["hard_skills"],
    hard_skill_options
)

selected_soft_skills = st.sidebar.multiselect(
    T["soft_skills"],
    soft_skill_options
)


city_options = [T["all_cities"]] + available_cities

selected_cities = st.sidebar.multiselect(
    T["cities"],
    city_options,
    default=[T["all_cities"]]
)


predict_button = st.sidebar.button(T["predict"])


# =========================
# CITY SELECTION
# =========================

if T["all_cities"] in selected_cities or len(selected_cities) == 0:
    final_selected_cities = available_cities
else:
    final_selected_cities = selected_cities


st.info(T["info"].format(n=len(final_selected_cities)))


# =========================
# PREDICTION
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
            st.error(T["error_no_predictions"])
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


    st.markdown(
        f'<div class="section-title">{T["main_insight"]}</div>',
        unsafe_allow_html=True
    )

    st.success(
        T["insight"].format(
            top_city=top_city["city"],
            top_salary=top_city["predicted_salary"],
            bottom_city=bottom_city["city"],
            bottom_salary=bottom_city["predicted_salary"]
        )
    )


    left, right = st.columns(2)

    with left:
        st.markdown(
            f'<div class="section-title">{T["top_cities"]}</div>',
            unsafe_allow_html=True
        )
        st.dataframe(results.head(10), use_container_width=True)

    with right:
        st.markdown(
            f'<div class="section-title">{T["lowest_cities"]}</div>',
            unsafe_allow_html=True
        )
        st.dataframe(
            results.tail(10).sort_values("predicted_salary"),
            use_container_width=True
        )


    st.markdown(
        f'<div class="section-title">{T["salary_comparison"]}</div>',
        unsafe_allow_html=True
    )

    fig = px.bar(
        results,
        x="city",
        y="predicted_salary",
        text="predicted_salary",
        title=T["chart_title"]
    )

    fig.update_traces(
        texttemplate="%{text:,.0f} ₽",
        textposition="outside"
    )

    fig.update_layout(
        xaxis_title=T["xaxis"],
        yaxis_title=T["yaxis"],
        height=550,
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)


    st.markdown(
        f'<div class="section-title">{T["full_ranking"]}</div>',
        unsafe_allow_html=True
    )

    results_display = results.copy()
    results_display["predicted_salary"] = (
        results_display["predicted_salary"].round(0).astype(int)
    )

    st.dataframe(results_display, use_container_width=True)

    csv = results_display.to_csv(index=False).encode("utf-8")

    st.download_button(
        label=T["download"],
        data=csv,
        file_name="salary_predictions_by_city.csv",
        mime="text/csv"
    )


else:
    st.markdown(
        f'<div class="section-title">{T["how_it_works"]}</div>',
        unsafe_allow_html=True
    )

    st.write(T["how_text"])
