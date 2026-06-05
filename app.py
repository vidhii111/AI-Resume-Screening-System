from flask import (
    Flask,
    render_template,
    request,
    redirect,
    send_file
)

from resume_parser import (
    extract_text,
    extract_email,
    extract_phone,
    extract_name
)
from skill_matcher import (
    extract_skills,
    calculate_match,
    missing_skills,
    generate_recommendations
)

from database import (
    create_database,
    save_result,
    get_all_results,
    get_statistics,
    get_chart_data,
    get_top_candidates,
    update_status,
    search_candidates,
    get_candidate_by_id
)

import os

from pdf_generator import generate_pdf

app = Flask(__name__)
latest_report = {}
create_database()

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():

    resume = request.files["resume"]

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        resume.filename
    )

    resume.save(filepath)

    text = extract_text(filepath)

    email = extract_email(text)

    phone = extract_phone(text)

    name = extract_name(text)

    resume_skills = extract_skills(text)

    job_description = request.form["job_description"]
    job_skills = extract_skills(job_description)

    print("Resume Skills:", resume_skills)
    print("Job Skills:", job_skills)

    score = calculate_match(
        resume_skills,
        job_skills
    )

    def get_rating(score):
     if score >= 80:
        return "A+ (Excellent)"
     elif score >= 60:
        return "A (Good)"
     elif score >= 40:
        return "B (Average)"
     elif score >= 20:
        return "C (Below Average)"
     else:
        return "D (Poor)"

    rating = get_rating(score)

    save_result(
       resume.filename,
       name,
       email,
       phone,
       score,
       rating
)

    missing = missing_skills(
        resume_skills,
        job_skills
)
       
    recommendations = generate_recommendations(
        missing
)
    
    global latest_report

    latest_report = {
    "filename": resume.filename,
    "name": name,
    "email": email,
    "phone": phone,
    "score": score,
    "rating": rating,
    "missing": missing,
    "recommendations": recommendations
}
    

    return render_template(
        "result.html",
        skills=resume_skills,
        job_skills=job_skills,
        score=score,
        rating=rating,
        missing=missing,
        email=email,
        phone=phone,
        name=name,
        recommendations=recommendations,
    )

@app.route("/dashboard")
def dashboard():

    results = get_all_results()

    stats = get_statistics()

    chart_data = get_chart_data()

    top_candidates = get_top_candidates()

    labels = [row[0] for row in chart_data]

    scores = [row[1] for row in chart_data]

    return render_template(
        "dashboard.html",
        results=results,
        stats=stats,
        labels=labels,
        scores=scores,
        top_candidates=top_candidates,
    )

@app.route("/candidates")
def candidates():

    keyword = request.args.get(
        "search",
        ""
    )

    if keyword:

        results = search_candidates(
            keyword
        )

    else:

        results = get_all_results()

    return render_template(
        "candidates.html",
        results=results
    )

@app.route("/rankings")
def rankings():

    top_candidates = get_top_candidates()

    return render_template(
        "rankings.html",
        top_candidates=top_candidates
    )

@app.route("/analytics")
def analytics():

    stats = get_statistics()

    return render_template(
        "analytics.html",
        stats=stats
    )

@app.route("/settings")
def settings():

    return render_template(
        "settings.html"
    )

@app.route(
    "/update_status/<int:id>/<status>"
)
def change_status(id, status):

    update_status(id, status)

    return redirect("/candidates")

@app.route("/download_report")
def download_report():

    pdf_file = generate_pdf(
        latest_report["filename"],
        latest_report["name"],
        latest_report["email"],
        latest_report["phone"],
        latest_report["score"],
        latest_report["rating"],
        latest_report["missing"],
        latest_report["recommendations"]
    )

    return send_file(
        pdf_file,
        as_attachment=True
    )

@app.route("/candidate/<int:id>")
def candidate_details(id):

    candidate = get_candidate_by_id(id)

    return render_template(
        "candidate_details.html",
        candidate=candidate
    )

import os

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )