from flask import Flask, render_template, request, send_file
import os
import matplotlib.pyplot as plt

from utils.parser import extract_text_from_pdf
from utils.matcher import rank_resumes
from utils.report_generator import generate_report

app = Flask(__name__)

UPLOAD_FOLDER = "resumes"
GRAPH_FOLDER = "static"
REPORT_FOLDER = "reports"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)

# Store latest results globally
latest_results = []


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")
    


@app.route("/analyze", methods=["POST"])
def analyze():
    global latest_results

    job_description = request.form["job_description"]
    uploaded_files = request.files.getlist("resumes")

    resume_texts = []

    for file in uploaded_files:
        if file.filename.endswith(".pdf"):
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)

            extracted_text = extract_text_from_pdf(filepath)
            resume_texts.append({
                "name": file.filename,
                "text": extracted_text
            })

    ranked_results = rank_resumes(job_description, resume_texts)
    latest_results = ranked_results

    # ---------------- GRAPH GENERATION ----------------
    names = [
        result["display_name"].split()[0] + (
            " " + result["display_name"].split()[1]
            if len(result["display_name"].split()) > 1 else ""
        )
        for result in ranked_results
    ]

    scores = [result["score"] for result in ranked_results]

    plt.figure(figsize=(10, 5), facecolor="#0f172a")
    ax = plt.gca()
    ax.set_facecolor("#0f172a")

    bars = plt.bar(
        names,
        scores,
        color="#8b5cf6",
        edgecolor="#c084fc",
        linewidth=1.5
    )

    # Titles and labels
    plt.title(
        "Candidate Match Score Overview",
        color="white",
        fontsize=14,
        fontweight="bold",
        pad=12
    )
    plt.xlabel("Candidates", color="#cbd5e1", fontsize=11)
    plt.ylabel("Match Score (%)", color="#cbd5e1", fontsize=11)

    # Axis styling
    plt.xticks(rotation=20, color="white", fontsize=10)
    plt.yticks(color="white", fontsize=10)

    # Remove top/right borders
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Style remaining borders
    ax.spines["left"].set_color("#475569")
    ax.spines["bottom"].set_color("#475569")

    # Grid
    ax.yaxis.grid(True, linestyle="--", alpha=0.25, color="#94a3b8")
    ax.set_axisbelow(True)

    # Add value labels on bars
    for bar, score in zip(bars, scores):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.5,
            f"{score}%",
            ha="center",
            va="bottom",
            color="white",
            fontsize=10,
            fontweight="bold"
        )

    plt.tight_layout()

    graph_path = os.path.join(GRAPH_FOLDER, "graph.png")
    plt.savefig(
        graph_path,
        transparent=False,
        facecolor="#0f172a",
        bbox_inches="tight"
    )
    plt.close()
    # ---------------- END GRAPH ----------------

    return render_template(
        "results.html",
        results=ranked_results,
        graph_url="graph.png"
    )


@app.route("/download_report")
def download_report():
    global latest_results

    report_path = generate_report(latest_results)
    return send_file(report_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)