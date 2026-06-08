import os
import csv
from datetime import datetime

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
    experience_id_from_years,
)


# --------------------------------------------------
# App settings
# --------------------------------------------------
st.set_page_config(
    page_title="AI Salary Prediction Platform by Megatonn",
    page_icon="💼",
    layout="wide",
)

MODEL_MAPE = 0.243  # 24.3% validation MAPE
FEEDBACK_FILE = "developer_feedback.csv"


# --------------------------------------------------
# Helper functions
# --------------------------------------------------
def format_rub(value):
    return f"{int(round(value)):,.0f} ₽".replace(",", " ")


def append_feedback_to_csv(role, message):
    """
    Saves feedback messages locally in a CSV file.
    For a real production version, this can later be connected
    to email, Google Sheets, database, CRM, or GitHub Issues.
    """
    file_exists = os.path.exists(FEEDBACK_FILE)

    with open(FEEDBACK_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["timestamp", "role", "message"])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            role,
            message,
        ])


# --------------------------------------------------
# Session state
# --------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "feedback_messages" not in st.session_state:
    st.session_state.feedback_messages = []


# --------------------------------------------------
# Styling
# --------------------------------------------------
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        .main-title {
            font-size: 42px;
            font-weight: 800;
            color: #0f172a;
            margin-bottom: 0px;
        }

        .main-subtitle {
            font-size: 17px;
            color: #64748b;
            margin-top: 8px;
            margin-bottom: 24px;
        }

        .info-box {
            background: linear-gradient(135deg, #f8fafc, #eef2ff);
            border: 1px solid #e2e8f0;
            border-radius: 18px;
            padding: 18px 22px;
            color: #334155;
            margin-bottom: 24px;
        }

        .metric-card {
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 18px;
            padding: 20px;
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06);
            min-height: 130px;
        }

        .metric-label {
            color: #64748b;
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 10px;
        }

        .metric-value {
            color: #0f172a;
            font-size: 26px;
            font-weight: 800;
            line-height: 1.2;
        }

        .metric-note {
            color: #64748b;
            font-size: 13px;
            margin-top: 8px;
        }

        .section-title {
            font-size: 24px;
            font-weight: 800;
            color: #0f172a;
            margin-top: 30px;
            margin-bottom: 14px;
        }

        .insight-card {
            background: #f8fafc;
            border-left: 5px solid #4f46e5;
            border-radius: 16px;
            padding: 18px 22px;
            margin-top: 16px;
            margin-bottom: 18px;
            color: #334155;
        }

        .uncertainty-card {
            background: #fff7ed;
            border: 1px solid #fed7aa;
            border-radius: 16px;
            padding: 18px 22px;
            margin-top: 16px;
            margin-bottom: 24px;
            color: #7c2d12;
        }

        .sidebar-card {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            padding: 14px 16px;
            margin-bottom: 18px;
        }

        .sidebar-card-title {
            font-size: 16px;
            font-weight: 800;
            color: #0f172a;
            margin-bottom: 6px;
        }

        .sidebar-card-text {
            font-size: 13px;
            color: #64748b;
            line-height: 1.45;
        }

        .login-title {
            text-align: center;
            font-size: 34px;
            font-weight: 800;
            color: #0f172a;
            margin-bottom: 4px;
        }

        .login-subtitle {
            text-align: center;
            color: #64748b;
            margin-bottom: 22px;
        }

        div[data-testid="stForm"] {
            max-width: 440px;
            margin: 80px auto 0 auto;
            padding: 34px;
            border-radius: 24px;
            border: 1px solid #e5e7eb;
            box-shadow: 0 20px 60px rgba(15, 23, 42, 0.08);
            background: white;
        }

        .feedback-card {
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 18px;
            padding: 18px 22px;
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.05);
            margin-top: 28px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# Login page
# --------------------------------------------------
def login_page():
    app_dir = os.path.dirname(__file__)
    possible_logo_files = ["logo.png", "Logo.png", "LOGO.png"]

    logo_path = next(
        (
            os.path.join(app_dir, file_name)
            for file_name in possible_logo_files
            if os.path.exists(os.path.join(app_dir, file_name))
        ),
        None,
    )

    with st.form("login_form", clear_on_submit=False):
        logo_left, logo_center, logo_right = st.columns([1, 1, 1])

        with logo_center:
            if logo_path:
                st.image(logo_path, width=155)
            else:
                st.error("Logo file was not found. Save it as logo.png or Logo.png in the same folder as app.py.")

        st.markdown(
            """
            <div class="login-title">Welcome back</div>
            <div class="login-subtitle">AI Salary Prediction Platform</div>
            """,
            unsafe_allow_html=True,
        )

        username = st.text_input("Username", value="Admin", placeholder="Admin")
        password = st.text_input("Password", value="admin", type="password", placeholder="admin")

        submitted = st.form_submit_button("Sign in →")

        if submitted:
            if username == "Admin" and password == "admin":
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Incorrect username or password.")


if not st.session_state.logged_in:
    login_page()
    st.stop()


# --------------------------------------------------
# Language and text
# --------------------------------------------------
LANG = st.sidebar.selectbox("Language / Язык", ["English", "Русский"])

TEXT = {
    "English": {
        "title": "AI Salary Prediction Platform",
        "company": "Megatonn",
        "subtitle": "Uncertainty-aware salary benchmarking based on machine learning and labor market data.",
        "resume_estimator": "Resume Salary Estimator",
        "resume_estimator_text": "Enter the candidate profile manually using resume information. The platform estimates salary across cities and displays a MAPE-based salary range.",
        "feedback_sidebar_title": "Developer Feedback",
        "feedback_sidebar_text": "Use the chatbot at the bottom of the page to send comments, bugs, or improvement ideas to the developers.",
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
        "model_mape": "Model MAPE",
        "city_gap": "Salary gap",
        "main_insight": "Main Insight",
        "insight": "For the same profile, the strongest salary forecast is in {top_city}: {top_salary}. The lowest forecast is in {bottom_city}: {bottom_salary}.",
        "uncertainty": "The salary range is calculated using the model validation MAPE of 24.3%. The point prediction is the model’s expected salary, while the interval shows the approximate error range. This output should be interpreted as a salary benchmarking range, not an exact final salary.",
        "salary_comparison": "Salary Comparison with MAPE-Based Range",
        "chart_title": "Predicted Salary by City with MAPE-Based Range",
        "full_ranking": "City Ranking",
        "download": "Download results as CSV",
        "how_it_works": "How it works",
        "how_text": "Select a position, skills, employment conditions and cities. The model keeps the profile fixed and changes only the city. After prediction, the platform shows a point estimate and a salary range based on MAPE.",
        "other": "Other",
        "on_site": "On-site",
        "remote": "Remote",
        "hybrid": "Hybrid",
        "shift": "Shift",
        "full_time": "Full time",
        "part_time": "Part time",
        "project_contract": "Project contract",
        "range": "Range",
        "lower_estimate": "Lower Salary Estimate, RUB",
        "upper_estimate": "Upper Salary Estimate, RUB",
        "predicted_salary": "Predicted Salary, RUB",
        "city": "City",
        "rank": "Rank",
        "feedback_title": "Developer Feedback Chatbot",
        "feedback_intro": "Send feedback, bugs, or suggestions directly from the prototype interface.",
        "feedback_placeholder": "Write feedback for the developers...",
        "feedback_welcome": "Hello! Send your feedback here. I will save it for the development team.",
        "feedback_ack": "Thank you! Your feedback was saved for the developers.",
        "download_feedback": "Download feedback log",
    },
    "Русский": {
        "title": "AI-платформа прогнозирования зарплат",
        "company": "Мегатонн",
        "subtitle": "Прогнозирование зарплат с учетом неопределенности модели на основе ML и данных рынка труда.",
        "resume_estimator": "Resume Salary Estimator",
        "resume_estimator_text": "Введите данные кандидата на основе резюме. Платформа оценит зарплату по городам и покажет диапазон на основе MAPE.",
        "feedback_sidebar_title": "Обратная связь разработчикам",
        "feedback_sidebar_text": "Используйте чат-бот внизу страницы, чтобы отправить комментарии, ошибки или идеи по улучшению.",
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
        "model_mape": "MAPE модели",
        "city_gap": "Разница зарплат",
        "main_insight": "Главный вывод",
        "insight": "Для одного и того же профиля самый высокий прогноз зарплаты в городе {top_city}: {top_salary}. Самый низкий прогноз в городе {bottom_city}: {bottom_salary}.",
        "uncertainty": "Диапазон зарплаты рассчитан на основе MAPE модели 24,3%. Точечный прогноз показывает ожидаемую зарплату по модели, а интервал отражает примерный диапазон ошибки. Результат следует интерпретировать как ориентир для salary benchmarking, а не как точную финальную зарплату.",
        "salary_comparison": "Сравнение зарплат с диапазоном на основе MAPE",
        "chart_title": "Прогноз зарплаты по городам с диапазоном на основе MAPE",
        "full_ranking": "Рейтинг городов",
        "download": "Скачать результаты в CSV",
        "how_it_works": "Как это работает",
        "how_text": "Выберите должность, навыки, условия занятости и города. Модель фиксирует профиль и меняет только город. После расчета платформа показывает точечный прогноз и диапазон зарплаты на основе MAPE.",
        "other": "Другое",
        "on_site": "Офис",
        "remote": "Удаленно",
        "hybrid": "Гибрид",
        "shift": "Сменный график",
        "full_time": "Полная занятость",
        "part_time": "Частичная занятость",
        "project_contract": "Проектный контракт",
        "range": "Диапазон",
        "lower_estimate": "Нижняя оценка зарплаты, руб.",
        "upper_estimate": "Верхняя оценка зарплаты, руб.",
        "predicted_salary": "Прогноз зарплаты, руб.",
        "city": "Город",
        "rank": "Ранг",
        "feedback_title": "Чат-бот обратной связи",
        "feedback_intro": "Отправьте комментарии, ошибки или предложения прямо из интерфейса прототипа.",
        "feedback_placeholder": "Напишите обратную связь для разработчиков...",
        "feedback_welcome": "Здравствуйте! Напишите обратную связь здесь. Я сохраню ее для команды разработки.",
        "feedback_ack": "Спасибо! Ваше сообщение сохранено для разработчиков.",
        "download_feedback": "Скачать журнал обратной связи",
    },
}

T = TEXT[LANG]


# --------------------------------------------------
# Sidebar inputs
# --------------------------------------------------
st.sidebar.markdown(
    f"""
    <div class="sidebar-card">
        <div class="sidebar-card-title">{T["resume_estimator"]}</div>
        <div class="sidebar-card-text">{T["resume_estimator_text"]}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown(
    f"""
    <div class="sidebar-card">
        <div class="sidebar-card-title">{T["feedback_sidebar_title"]}</div>
        <div class="sidebar-card-text">{T["feedback_sidebar_text"]}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.header(T["profile_input"])

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
    T["shift"]: "shift",
}

employment_label_to_value = {
    T["full_time"]: "full",
    T["part_time"]: "part",
    T["project_contract"]: "project",
}

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
    placeholder=T["key_skills"],
)

selected_hard_skills = st.sidebar.multiselect(
    T["hard_skills"],
    hard_skill_options,
    placeholder=T["hard_skills"],
)

selected_soft_skills = st.sidebar.multiselect(
    T["soft_skills"],
    soft_skill_options,
    placeholder=T["soft_skills"],
)

city_options = [T["all_cities"]] + available_cities
selected_cities = st.sidebar.multiselect(
    T["cities"],
    city_options,
    default=[T["all_cities"]],
    placeholder=T["cities"],
)

predict_button = st.sidebar.button(T["predict"])

if T["all_cities"] in selected_cities or len(selected_cities) == 0:
    final_selected_cities = available_cities
else:
    final_selected_cities = selected_cities


# --------------------------------------------------
# Header
# --------------------------------------------------
st.markdown(
    f"""
    <div class="main-title">{T["title"]}</div>
    <div class="main-subtitle">{T["subtitle"]}</div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="info-box">
        {T["info"].format(n=len(final_selected_cities))}
    </div>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# Prediction results
# --------------------------------------------------
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
            "selected_cities": final_selected_cities,
        }

        results = predict_all_cities(user_profile)

        if results.empty:
            st.error("No predictions available.")
            st.stop()

        # MAPE-based salary range
        results["predicted_salary"] = results["predicted_salary"].round(0).astype(int)

        results["salary_min"] = (
            results["predicted_salary"] * (1 - MODEL_MAPE)
        ).clip(lower=0).round(0).astype(int)

        results["salary_max"] = (
            results["predicted_salary"] * (1 + MODEL_MAPE)
        ).round(0).astype(int)

        results["error_plus"] = results["salary_max"] - results["predicted_salary"]
        results["error_minus"] = results["predicted_salary"] - results["salary_min"]
        results["mape_used"] = "24.3%"

        results = results.sort_values("predicted_salary", ascending=False).reset_index(drop=True)

        top_city = results.iloc[0]
        bottom_city = results.iloc[-1]

        avg_salary = int(results["predicted_salary"].mean().round(0))
        avg_min = int(avg_salary * (1 - MODEL_MAPE))
        avg_max = int(avg_salary * (1 + MODEL_MAPE))

        salary_gap = int(top_city["predicted_salary"] - bottom_city["predicted_salary"])

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{T["highest_city"]}</div>
                    <div class="metric-value">{top_city["city"]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{T["highest_salary"]}</div>
                    <div class="metric-value">{format_rub(top_city["predicted_salary"])}</div>
                    <div class="metric-note">
                        {T["range"]}: {format_rub(top_city["salary_min"])} – {format_rub(top_city["salary_max"])}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col3:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{T["average_salary"]}</div>
                    <div class="metric-value">{format_rub(avg_salary)}</div>
                    <div class="metric-note">
                        {T["range"]}: {format_rub(avg_min)} – {format_rub(avg_max)}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col4:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{T["model_mape"]}</div>
                    <div class="metric-value">24.3%</div>
                    <div class="metric-note">Used for salary range</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col5:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{T["city_gap"]}</div>
                    <div class="metric-value">{format_rub(salary_gap)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown(
            f"""
            <div class="insight-card">
                <strong>{T["main_insight"]}</strong><br><br>
                {T["insight"].format(
                    top_city=top_city["city"],
                    top_salary=format_rub(top_city["predicted_salary"]),
                    bottom_city=bottom_city["city"],
                    bottom_salary=format_rub(bottom_city["predicted_salary"]),
                )}
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="uncertainty-card">
                <strong>MAPE-based uncertainty:</strong><br><br>
                {T["uncertainty"]}
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f'<div class="section-title">{T["salary_comparison"]}</div>',
            unsafe_allow_html=True,
        )

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
                [1.00, "#4f46e5"],
            ],
            error_y="error_plus",
            error_y_minus="error_minus",
        )

        fig.update_traces(
            texttemplate="%{text:,.0f} ₽",
            textposition="outside",
            marker_line_width=0,
            error_y=dict(thickness=1.6, width=7, color="#334155"),
            customdata=results[["salary_min", "salary_max"]],
            hovertemplate=(
                "%{x}<br>"
                "Predicted: %{y:,.0f} ₽<br>"
                "MAPE-based range: %{customdata[0]:,.0f} ₽ to %{customdata[1]:,.0f} ₽"
                "<extra></extra>"
            ),
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
            bargap=0.28,
        )

        st.plotly_chart(fig, use_container_width=True)

        st.markdown(
            f'<div class="section-title">{T["full_ranking"]}</div>',
            unsafe_allow_html=True,
        )

        results_display = results[["city", "predicted_salary", "salary_min", "salary_max", "mape_used"]].copy()
        results_display.insert(0, "Rank", range(1, len(results_display) + 1))

        if LANG == "English":
            results_display = results_display.rename(
                columns={
                    "Rank": T["rank"],
                    "city": T["city"],
                    "predicted_salary": T["predicted_salary"],
                    "salary_min": T["lower_estimate"],
                    "salary_max": T["upper_estimate"],
                    "mape_used": "MAPE Used",
                }
            )
        else:
            results_display = results_display.rename(
                columns={
                    "Rank": T["rank"],
                    "city": T["city"],
                    "predicted_salary": T["predicted_salary"],
                    "salary_min": T["lower_estimate"],
                    "salary_max": T["upper_estimate"],
                    "mape_used": "Использованный MAPE",
                }
            )

        st.dataframe(results_display, use_container_width=True, hide_index=True)

        csv_results = results_display.to_csv(index=False).encode("utf-8")

        st.download_button(
            label=T["download"],
            data=csv_results,
            file_name="salary_predictions_by_city.csv",
            mime="text/csv",
        )

else:
    st.markdown(
        f"""
        <div class="insight-card">
            <strong>{T["how_it_works"]}</strong><br><br>
            {T["how_text"]}
        </div>
        """,
        unsafe_allow_html=True,
    )


# --------------------------------------------------
# Developer feedback chatbot
# --------------------------------------------------
st.markdown(
    f"""
    <div class="feedback-card">
        <div class="section-title" style="margin-top:0px;">{T["feedback_title"]}</div>
        <p style="color:#64748b; margin-top:-8px;">{T["feedback_intro"]}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if len(st.session_state.feedback_messages) == 0:
    st.session_state.feedback_messages.append(
        {"role": "assistant", "content": T["feedback_welcome"]}
    )

for message in st.session_state.feedback_messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

feedback_prompt = st.chat_input(T["feedback_placeholder"])

if feedback_prompt:
    st.session_state.feedback_messages.append(
        {"role": "user", "content": feedback_prompt}
    )
    append_feedback_to_csv("user", feedback_prompt)

    st.session_state.feedback_messages.append(
        {"role": "assistant", "content": T["feedback_ack"]}
    )
    append_feedback_to_csv("assistant", T["feedback_ack"])

    st.rerun()

if os.path.exists(FEEDBACK_FILE):
    with open(FEEDBACK_FILE, "rb") as file:
        st.download_button(
            label=T["download_feedback"],
            data=file,
            file_name="developer_feedback.csv",
            mime="text/csv",
        )
