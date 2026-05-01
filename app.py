from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "bca-demo-secret-key"

CAREER_SKILLS = {
    "Data Analyst": ["Python", "SQL", "Excel", "Statistics", "Power BI"],
    "Web Developer": ["HTML", "CSS", "JavaScript", "React", "Git"],
    "Cyber Security": ["Networking", "Linux", "Python", "OWASP", "SIEM"],
}

COURSE_SUGGESTIONS = {
    "Python": "Python for Everybody (Coursera)",
    "SQL": "SQL Basics (Khan Academy)",
    "Excel": "Excel Skills for Business",
    "Statistics": "Intro to Statistics (Udacity)",
    "Power BI": "Microsoft Power BI Learning Path",
    "HTML": "Responsive Web Design (freeCodeCamp)",
    "CSS": "Advanced CSS and Sass",
    "JavaScript": "JavaScript Algorithms (freeCodeCamp)",
    "React": "React Official Tutorial",
    "Git": "Git and GitHub Crash Course",
    "Networking": "Cisco Networking Basics",
    "Linux": "Linux Essentials",
    "OWASP": "OWASP Top 10 Course",
    "SIEM": "SIEM Fundamentals",
}


def analyze_skill_gap(current_skills: list[str], target_career: str) -> dict:
    required = CAREER_SKILLS.get(target_career, [])
    current_set = {s.strip().title() for s in current_skills if s.strip()}
    missing = [skill for skill in required if skill not in current_set]
    matched = [skill for skill in required if skill in current_set]

    roadmap = {
        "30_days": missing[:2],
        "60_days": missing[2:4],
        "90_days": missing[4:],
    }

    courses = {skill: COURSE_SUGGESTIONS.get(skill, "Search on YouTube/Udemy") for skill in missing}

    return {
        "required": required,
        "matched": matched,
        "missing": missing,
        "roadmap": roadmap,
        "courses": courses,
    }


@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if name:
            session["name"] = name
            return redirect(url_for("skills"))
    return render_template("login.html")


@app.route("/skills", methods=["GET", "POST"])
def skills():
    if "name" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        target_career = request.form.get("career", "Data Analyst")
        skills_raw = request.form.get("skills", "")
        current_skills = [s for s in skills_raw.split(",")]

        analysis = analyze_skill_gap(current_skills, target_career)
        session["report"] = {
            "name": session["name"],
            "career": target_career,
            **analysis,
        }
        return redirect(url_for("report"))

    return render_template("skills.html", careers=CAREER_SKILLS.keys(), name=session["name"])


@app.route("/report")
def report():
    if "name" not in session:
        return redirect(url_for("login"))

    report_data = session.get("report")
    if not report_data:
        return redirect(url_for("skills"))

    return render_template("report.html", report=report_data)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
