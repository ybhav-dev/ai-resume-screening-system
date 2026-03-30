from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils.skill_extractor import extract_skills
import os

def clean_resume_name(filename):
    name = os.path.splitext(filename)[0]   # remove .pdf
    name = name.replace("_", " ").replace("-", " ")
    return name

def rank_resumes(job_description, resumes):
    documents = [job_description] + [resume["text"] for resume in resumes]

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

    ranked_results = []

    for i, score in enumerate(similarity_scores):
        skills = extract_skills(resumes[i]["text"])

        ranked_results.append({
            "name": resumes[i]["name"],  # original file name
            "display_name": clean_resume_name(resumes[i]["name"]),  # clean UI name
            "score": round(score * 100, 2),
            "skills": ", ".join(skills) if skills else "No major skills found"
        })

    ranked_results = sorted(ranked_results, key=lambda x: x["score"], reverse=True)
    return ranked_results