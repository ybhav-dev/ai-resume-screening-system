import pandas as pd
import os

def generate_report(results):
    report_data = []

    for i, result in enumerate(results, start=1):
        report_data.append({
            "Rank": i,
            "Candidate Resume": result["name"],
            "Match Score (%)": result["score"],
            "Skills": result["skills"]
        })

    df = pd.DataFrame(report_data)

    report_path = os.path.join("reports", "shortlist_report.csv")
    df.to_csv(report_path, index=False)

    return report_path