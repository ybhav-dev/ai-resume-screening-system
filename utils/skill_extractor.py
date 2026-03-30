def extract_skills(text):
    skills_db = [
        "python", "java", "c++", "sql", "machine learning",
        "data analysis", "excel", "power bi", "flask",
        "html", "css", "javascript", "react", "django"
    ]

    found_skills = []

    text = text.lower()

    for skill in skills_db:
        if skill in text:
            found_skills.append(skill.title())

    return found_skills