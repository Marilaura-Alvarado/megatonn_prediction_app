import os
import re
import joblib
import numpy as np
import pandas as pd

from scipy.sparse import hstack, csr_matrix


BASE_PATH = "."



def load_file(filename):
    path = os.path.join(BASE_PATH, filename)

    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Missing file: {filename}. Make sure it is in the same folder as app.py"
        )

    return joblib.load(path)


model = load_file("best_salary_model.pkl")

scaler = load_file("scaler.pkl")

mlb_key = load_file("mlb_key.pkl")
mlb_hard = load_file("mlb_hard.pkl")
mlb_soft = load_file("mlb_soft.pkl")

train_meta = load_file("train_meta.pkl")

# Optional artifacts
try:
    tfidf_role_word = load_file("tfidf_role_word.pkl")
except Exception:
    tfidf_role_word = None

try:
    tfidf_role_char = load_file("tfidf_role_char.pkl")
except Exception:
    tfidf_role_char = None

try:
    freq_maps = load_file("freq_maps.pkl")
except Exception:
    freq_maps = {}

try:
    target_encoding_maps = load_file("target_encoding_maps.pkl")
except Exception:
    target_encoding_maps = {}

try:
    salary_anchor_maps = load_file("salary_anchor_maps.pkl")
except Exception:
    salary_anchor_maps = {}

try:
    numeric_cols = load_file("numeric_cols.pkl")
except Exception:
    numeric_cols = ["experience_years"]

try:
    small_cat_cols = load_file("small_cat_cols.pkl")
except Exception:
    small_cat_cols = ["experience_id", "schedule_id", "employment_id", "seniority"]

try:
    small_cat_ohe_columns = load_file("small_cat_ohe_columns.pkl")
except Exception:
    small_cat_ohe_columns = None



def get_available_cities():
    return sorted(train_meta["city"].dropna().astype(str).unique())


def parse_skills(text):
    if text is None:
        return []

    return [
        x.strip().lower()
        for x in str(text).split(",")
        if x.strip()
    ]


def clean_text(x):
    x = str(x).lower().strip()
    x = re.sub(r"[^0-9a-zA-Zа-яА-ЯёЁ\s\-/]+", " ", x)
    x = re.sub(r"\s+", " ", x).strip()
    return x


def get_seniority(years):
    if years <= 0:
        return "entry"
    elif years <= 2:
        return "junior"
    elif years <= 5:
        return "middle"
    return "senior"


def safe_mean_from_map(mapping, default=0):
    try:
        values = list(mapping.values())
        if len(values) == 0:
            return default
        return float(np.mean(values))
    except Exception:
        return default


def build_city_profile_dataframe(user_profile):
    cities = get_available_cities()

    key_skills_list = parse_skills(user_profile.get("key_skills", ""))
    hard_skills_list = parse_skills(user_profile.get("hard_skills", ""))
    soft_skills_list = parse_skills(user_profile.get("soft_skills", ""))

    experience_years = int(user_profile.get("experience_years", 0))
    experience_id = user_profile.get("experience_id", "unknown")
    schedule_id = user_profile.get("schedule_id", "unknown")
    employment_id = user_profile.get("employment_id", "unknown")

    rows = []

    for city in cities:
        rows.append({
            "role_name": clean_text(user_profile.get("role_name", "")),
            "role_area": clean_text(user_profile.get("role_area", "")),
            "city": city,

            "experience_years": experience_years,
            "experience_id": experience_id,
            "schedule_id": schedule_id,
            "employment_id": employment_id,

            "seniority": get_seniority(experience_years),
            "job_level": get_seniority(experience_years),

            "key_skills_list": key_skills_list,
            "hard_skills_list": hard_skills_list,
            "soft_skills_list": soft_skills_list,

            "hard_skills_count": len(hard_skills_list),
            "soft_skills_count": len(soft_skills_list),
            "skills_count": len(set(key_skills_list + hard_skills_list + soft_skills_list)),
            "hard_soft_ratio": len(hard_skills_list) / max(len(soft_skills_list), 1),

            "is_remote_schedule": int(schedule_id == "remote"),
            "is_full_day": int(schedule_id == "fullDay"),
            "is_flexible": int(schedule_id == "flexible"),
            "is_shift": int(schedule_id == "shift"),

            "is_full_employment": int(employment_id == "full"),
            "is_part_employment": int(employment_id == "part"),
            "is_project_employment": int(employment_id == "project"),
        })

    df = pd.DataFrame(rows)

    df["role_city"] = df["role_name"].astype(str) + "_" + df["city"].astype(str)
    df["role_exp_interaction"] = df["role_name"].astype(str) + "_" + df["experience_id"].astype(str)

    return df




def build_features(df):
    df = df.copy()

    # Frequency encoding
    for col, mapping in freq_maps.items():
        if col in df.columns:
            df[col + "_freq"] = df[col].astype(str).map(mapping).fillna(0)

    # Target encoding
    for col, mapping in target_encoding_maps.items():
        if col in df.columns:
            default_value = safe_mean_from_map(mapping)
            df[col + "_target_oof"] = df[col].astype(str).map(mapping).fillna(default_value)

    # Salary anchors
    anchor_name_map = {
        "city": "city_avg_salary",
        "role_name": "role_avg_salary",
        "role_city": "role_city_avg_salary"
    }

    for col, mapping in salary_anchor_maps.items():
        if col in df.columns:
            default_value = safe_mean_from_map(mapping)
            output_col = anchor_name_map.get(col, col + "_avg_salary")
            df[output_col] = df[col].astype(str).map(mapping).fillna(default_value)

    # Numeric columns
    for col in numeric_cols:
        if col not in df.columns:
            df[col] = 0

    X_numeric_df = df[numeric_cols].apply(pd.to_numeric, errors="coerce").fillna(0)
    X_numeric = csr_matrix(scaler.transform(X_numeric_df))

    # Small categorical columns
    for col in small_cat_cols:
        if col not in df.columns:
            df[col] = "unknown"

X_small_ohe = pd.get_dummies(df[small_cat_cols])

if small_cat_ohe_columns is not None:
    X_small_ohe = X_small_ohe.reindex(columns=small_cat_ohe_columns, fill_value=0)

X_small_ohe_sparse = csr_matrix(X_small_ohe.astype(float).values)


    # Skills
    X_key = csr_matrix(mlb_key.transform(df["key_skills_list"]))
    X_hard = csr_matrix(mlb_hard.transform(df["hard_skills_list"]))
    X_soft = csr_matrix(mlb_soft.transform(df["soft_skills_list"]))

    feature_blocks = [
        X_numeric,
        X_small_ohe_sparse,
        X_key,
        X_hard,
        X_soft
    ]


    if tfidf_role_word is not None:
        feature_blocks.append(tfidf_role_word.transform(df["role_name"]))

    if tfidf_role_char is not None:
        feature_blocks.append(tfidf_role_char.transform(df["role_name"]))

    X_final = hstack(feature_blocks).tocsr()

    return X_final



def predict_all_cities(user_profile):
    profile_df = build_city_profile_dataframe(user_profile)
    X_input = build_features(profile_df)

    pred_log = model.predict(X_input)
    pred_salary = np.expm1(pred_log)
    pred_salary = np.maximum(pred_salary, 0)

    results = pd.DataFrame({
        "city": profile_df["city"],
        "predicted_salary": pred_salary
    })

    results = results.sort_values("predicted_salary", ascending=False).reset_index(drop=True)

    return results
