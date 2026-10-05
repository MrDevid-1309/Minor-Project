import json
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from database import get_db, init_db
from questions import MCQS, CODING
from logic_analyzer import analyze_logic, consistency_flag
from code_runner import run_code
from predictor import predict_placement

app = Flask(__name__)
app.secret_key = "change-this-secret-key"
init_db()


def login_required(f):
    @wraps(f)
    def wrapper(*a, **k):
        if "uid" not in session:
            return redirect(url_for("login"))
        return f(*a, **k)
    return wrapper


def admin_required(f):
    @wraps(f)
    def wrapper(*a, **k):
        if session.get("role") != "admin":
            flash("Admin access only.", "error")
            return redirect(url_for("dashboard"))
        return f(*a, **k)
    return wrapper


@app.route("/")
def index():
    return redirect(url_for("dashboard") if "uid" in session else url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        f = request.form
        try:
            conn = get_db()
            conn.execute("INSERT INTO users(username,password,name,cgpa,projects,internships,communication) "
                         "VALUES(?,?,?,?,?,?,?)",
                         (f["username"].strip(), generate_password_hash(f["password"]), f["name"].strip(),
                          float(f["cgpa"]), int(f["projects"]), int(f["internships"]), int(f["communication"])))
            conn.commit()
            flash("Registered! Please login.", "ok")
            return redirect(url_for("login"))
        except Exception:
            flash("Username already exists or invalid data.", "error")
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = get_db().execute("SELECT * FROM users WHERE username=?", (request.form["username"].strip(),)).fetchone()
        if u and check_password_hash(u["password"], request.form["password"]):
            session.update(uid=u["id"], name=u["name"], role=u["role"])
            return redirect(url_for("dashboard"))
        flash("Invalid username or password.", "error")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    rows = get_db().execute("SELECT * FROM attempts WHERE user_id=? ORDER BY id DESC", (session["uid"],)).fetchall()
    return render_template("dashboard.html", attempts=rows)


@app.route("/test")
@login_required
def test():
    return render_template("test.html", mcqs=MCQS, coding=CODING)


@app.route("/api/analyze_logic", methods=["POST"])
@login_required
def api_analyze_logic():
    """Live feedback while the student types in the logic box."""
    d = request.get_json(force=True)
    prob = next((c for c in CODING if c["id"] == int(d.get("qid", 0))), None)
    if not prob:
        return jsonify(error="bad question"), 400
    return jsonify(analyze_logic(d.get("logic", ""), prob))


@app.route("/submit", methods=["POST"])
@login_required
def submit():
    f = request.form
    # ---- MCQ scoring (aptitude / technical) ----
    tot = {"aptitude": 0, "technical": 0}
    ok = {"aptitude": 0, "technical": 0}
    for q in MCQS:
        tot[q["cat"]] += 1
        if f.get(f"mcq_{q['id']}") == str(q["ans"]):
            ok[q["cat"]] += 1
    aptitude = 100 * ok["aptitude"] / tot["aptitude"]
    technical = 100 * ok["technical"] / tot["technical"]

    # ---- Coding + Logic ----
    code_pcts, logic_scores, details = [], [], []
    for p in CODING:
        code = f.get(f"code_{p['id']}", "")
        logic_text = f.get(f"logic_{p['id']}", "")
        res = run_code(code, p)
        code_pct = 100 * res["passed"] / res["total"]
        lg = analyze_logic(logic_text, p, code)
        code_pcts.append(code_pct)
        logic_scores.append(lg["score"])
        details.append({"title": p["title"], "code": code, "logic_text": logic_text,
                        "run": res, "code_pct": round(code_pct, 1), "logic": lg,
                        "insight": consistency_flag(code_pct, lg["score"])})
    coding = sum(code_pcts) / len(code_pcts)
    logic = sum(logic_scores) / len(logic_scores)

    # ---- Placement prediction ----
    u = get_db().execute("SELECT * FROM users WHERE id=?", (session["uid"],)).fetchone()
    scores = {"aptitude": aptitude, "technical": technical, "coding": coding, "logic": logic}
    profile = {"cgpa": u["cgpa"], "projects": u["projects"], "internships": u["internships"],
               "communication": u["communication"]}
    pred = predict_placement(scores, profile)

    conn = get_db()
    cur = conn.execute("INSERT INTO attempts(user_id,aptitude,technical,coding,logic,probability,label,details) "
                       "VALUES(?,?,?,?,?,?,?,?)",
                       (session["uid"], aptitude, technical, coding, logic, pred["probability"], pred["label"],
                        json.dumps({"problems": details, "pred": pred})))
    conn.commit()
    return redirect(url_for("result", aid=cur.lastrowid))


@app.route("/result/<int:aid>")
@login_required
def result(aid):
    a = get_db().execute("SELECT * FROM attempts WHERE id=?", (aid,)).fetchone()
    if not a or (a["user_id"] != session["uid"] and session.get("role") != "admin"):
        flash("Result not found.", "error")
        return redirect(url_for("dashboard"))
    return render_template("result.html", a=a, d=json.loads(a["details"]))


@app.route("/admin")
@login_required
@admin_required
def admin():
    rows = get_db().execute("""SELECT a.*, u.name, u.username FROM attempts a
                               JOIN users u ON u.id=a.user_id ORDER BY a.probability DESC""").fetchall()
    return render_template("admin.html", rows=rows)


if __name__ == "__main__":
    app.run(debug=True)
