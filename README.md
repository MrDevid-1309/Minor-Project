# AI Based Competency Assessment & Placement Prediction System

## Unique idea: "Logic Box"
In every coding question the student writes code AND explains the logic in a separate box.
NLP (TF-IDF + cosine similarity + concept coverage + reasoning-structure analysis) scores how well the student
understands the problem. This logic score is a feature of the ML placement model, and is compared with code
correctness to detect copied / memorised solutions.

## How to run
```
pip install -r requirements.txt
python train_model.py      # trains & saves the ML model (optional - auto-trains if missing)
python app.py              # open http://127.0.0.1:5000
```
Admin login: admin / admin123.  Students: register first.

## Files
| File | Purpose |
|---|---|
| app.py | Flask app: routes, scoring, result pipeline |
| questions.py | MCQs + coding problems (tests, reference logic, concepts) - add your own here |
| logic_analyzer.py | NLP analysis of the logic box (core idea) |
| code_runner.py | Runs student code against test cases (subprocess + timeout) |
| train_model.py | Generates synthetic data & trains RandomForest placement model |
| predictor.py | Placement probability, weak areas, suggestions |
| database.py | SQLite tables (users, attempts) |
| templates/, static/ | Frontend (HTML/CSS/JS) |

## Flow
Register (CGPA, projects...) -> Test (MCQ + code + logic box, live AI feedback, timer) ->
Scores: aptitude, technical, coding, logic -> RandomForest -> placement % + feedback -> Admin dashboard.

## Limitations / future scope
- Training data is synthetic; replace data/placement_data.csv with real college data.
- Code runner is not a hardened sandbox (use Docker in production).
- Upgrade logic analysis with sentence-transformers / LLM; add more questions & languages.
