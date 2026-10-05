import os
import joblib, pandas as pd
from train_model import FEATURES

_MODEL = None


def _model():
    global _MODEL
    if _MODEL is None:
        path = "model/placement_model.joblib"
        if not os.path.exists(path):
            import train_model
            from sklearn.ensemble import RandomForestClassifier
            df = train_model.make_data()
            _MODEL = RandomForestClassifier(n_estimators=250, max_depth=8, random_state=1).fit(df[FEATURES], df.placed)
            joblib.dump(_MODEL, path)
        else:
            _MODEL = joblib.load(path)
    return _MODEL


def predict_placement(scores: dict, profile: dict) -> dict:
    row = {**scores, **profile}
    X = pd.DataFrame([[row[f] for f in FEATURES]], columns=FEATURES)
    prob = float(_model().predict_proba(X)[0][1]) * 100
    if prob >= 70:
        label, tier = "High chance", "Product / top service companies (e.g. TCS Digital, Infosys SP, startups)"
    elif prob >= 45:
        label, tier = "Moderate chance", "Mass recruiters (e.g. TCS, Wipro, Cognizant, Capgemini)"
    else:
        label, tier = "Low chance", "Focus on improving skills first; target support / training roles"
    weak = sorted(scores.items(), key=lambda t: t[1])[:2]
    tips = {"aptitude": "Practice quantitative & reasoning aptitude daily.",
            "technical": "Revise DSA, DBMS, OOP, OS and CN fundamentals.",
            "coding": "Solve 2-3 coding problems daily on LeetCode/HackerRank.",
            "logic": "Practice explaining your approach in words - step by step with complexity."}
    return {"probability": round(prob, 1), "label": label, "companies": tier,
            "weak_areas": [w[0] for w in weak], "tips": [tips[w[0]] for w in weak]}
