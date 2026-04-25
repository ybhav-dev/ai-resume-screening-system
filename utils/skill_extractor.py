def extract_skills(text):
    skills_db = {
        "programming": [
            "python", "java", "c++", "c", "javascript", "typescript"
        ],
        "web": [
            "html", "css", "react", "angular", "vue", "node", "express", "flask", "django"
        ],
        "data": [
            "sql", "mysql", "postgresql", "mongodb", "data analysis",
            "pandas", "numpy", "excel", "power bi", "tableau"
        ],
        "ai_ml": [
            "machine learning", "deep learning", "nlp", "computer vision",
            "scikit-learn", "tensorflow", "keras", "pytorch"
        ],
        "tools": [
            "git", "github", "docker", "aws", "azure", "linux"
        ]
    }

    found_skills = []
    text = text.lower()

    for category in skills_db.values():
        for skill in category:
            if skill in text:
                found_skills.append(skill.title())

    return list(set(found_skills))