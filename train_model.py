"""
Trains the placement prediction model.
Since real placement data is private, a realistic SYNTHETIC dataset is generated
(replace data/placement_data.csv with your college's real data if available).

Features: aptitude, technical, coding, logic (all %), cgpa, projects, internships, communication
Target  : placed (0/1)
"""
import os
import joblib, numpy as np, pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

FEATURES = ["aptitude", "technical", "coding", "logic", "cgpa", "projects", "internships", "communication"]
os.makedirs("model", exist_ok=True)
os.makedirs("data", exist_ok=True)


def make_data(n=2000, seed=42):
    r = np.random.default_rng(seed)
    ability = r.normal(0, 1, n)                         # hidden "talent" factor
    clip = lambda x, a, b: np.clip(x, a, b)
    df = pd.DataFrame({
        "aptitude": clip(60 + 18 * ability + r.normal(0, 10, n), 0, 100),
        "technical": clip(58 + 20 * ability + r.normal(0, 12, n), 0, 100),
        "coding": clip(55 + 22 * ability + r.normal(0, 14, n), 0, 100),
        "logic": clip(52 + 20 * ability + r.normal(0, 12, n), 0, 100),
        "cgpa": clip(7.0 + 1.0 * ability + r.normal(0, 0.6, n), 4, 10),
        "projects": clip(np.round(2 + 1.2 * ability + r.normal(0, 1, n)), 0, 6),
        "internships": clip(np.round(0.8 + 0.7 * ability + r.normal(0, 0.8, n)), 0, 3),
        "communication": clip(np.round(6 + 1.5 * ability + r.normal(0, 1.2, n)), 1, 10),
    }).round(2)
    z = (0.025 * df.aptitude + 0.03 * df.technical + 0.035 * df.coding + 0.04 * df.logic
         + 0.35 * df.cgpa + 0.25 * df.projects + 0.5 * df.internships + 0.2 * df.communication)
    z = (z - z.mean()) / z.std() * 1.6 + r.normal(0, 0.5, n)
    df["placed"] = (r.random(n) < 1 / (1 + np.exp(-z))).astype(int)
    return df


if __name__ == "__main__":
    df = make_data()
    df.to_csv("data/placement_data.csv", index=False)
    X_train, X_test, y_train, y_test = train_test_split(df[FEATURES], df.placed, test_size=0.2,
                                                        random_state=1, stratify=df.placed)
    rf = RandomForestClassifier(n_estimators=250, max_depth=8, random_state=1).fit(X_train, y_train)
    lr = LogisticRegression(max_iter=2000).fit(X_train, y_train)
    print("Random Forest accuracy :", round(accuracy_score(y_test, rf.predict(X_test)), 3))
    print("Logistic Reg. accuracy :", round(accuracy_score(y_test, lr.predict(X_test)), 3))
    print(classification_report(y_test, rf.predict(X_test)))
    imp = sorted(zip(FEATURES, rf.feature_importances_), key=lambda t: -t[1])
    print("Feature importance:", [(f, round(i, 3)) for f, i in imp])
    joblib.dump(rf, "model/placement_model.joblib")
    print("Model saved -> model/placement_model.joblib")
