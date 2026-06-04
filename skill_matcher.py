skills_db = [
    "python",
    "java",
    "c",
    "c++",
    "sql",
    "html",
    "css",
    "javascript",
    "flask",
    "django",

    "machine learning",
    "deep learning",
    "artificial intelligence",
    "data science",
    "nlp",
    "computer vision",

    "tensorflow",
    "keras",
    "pytorch",
    "scikit-learn",

    "pandas",
    "numpy",
    "matplotlib",
    "seaborn",

    "git",
    "github",

    "aws",
    "azure",
    "docker",

    "excel",
    "power bi",

    "mysql",
    "sqlite"
]

def extract_skills(text):
    text = text.lower()

    found_skills = []

    for skill in skills_db:
     if skill in text:
        found_skills.append(skill)

    return found_skills

def calculate_match(resume_skills, job_skills):

    if len(job_skills) == 0:
        return 0

    matched = set(resume_skills).intersection(set(job_skills))

    score = (len(matched) / len(job_skills)) * 100

    return round(score, 2)

def missing_skills(resume_skills, job_skills):
    return list(set(job_skills) - set(resume_skills))

def generate_recommendations(missing_skills_list):

    recommendations = []

    for skill in missing_skills_list:

        recommendations.append(
            f"Consider adding {skill} to your resume."
        )

    return recommendations