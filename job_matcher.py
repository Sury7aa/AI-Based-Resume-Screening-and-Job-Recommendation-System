
import pandas as pd
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from skill_extractor import extract_skills

BASE_DIR = Path(__file__).resolve().parent
JOBS_FILE = BASE_DIR / "data" / "jobs.csv"


def match_jobs(resume_text):

    # Load job dataset
    jobs = pd.read_csv(JOBS_FILE)

    # Extract skills from resume
    resume_skills = extract_skills(resume_text)
    resume_skill_set = {
        skill.lower() for skill in resume_skills
    }

    # Prepare job descriptions
    job_texts = (
        jobs["job_title"].fillna("") + " " +
        jobs["description"].fillna("") + " " +
        jobs["skills"].fillna("")
    ).tolist()

    # Calculate TF-IDF text similarity
    all_texts = [resume_text] + job_texts

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    tfidf_matrix = vectorizer.fit_transform(all_texts)

    similarity_scores = cosine_similarity(
        tfidf_matrix[0:1],
        tfidf_matrix[1:]
    )[0]

    # Store text similarity
    jobs["text_similarity"] = similarity_scores * 100

    # Calculate skill coverage
    skill_coverages = []
    matching_lists = []
    missing_lists = []

    for _, job in jobs.iterrows():

        required_skills = [
            skill.strip()
            for skill in str(job["skills"]).split(",")
            if skill.strip()
        ]

        matching = [
            skill for skill in required_skills
            if skill.lower() in resume_skill_set
        ]

        missing = [
            skill for skill in required_skills
            if skill.lower() not in resume_skill_set
        ]

        if required_skills:
            coverage = (
                len(matching) / len(required_skills)
            ) * 100
        else:
            coverage = 0

        skill_coverages.append(coverage)
        matching_lists.append(matching)
        missing_lists.append(missing)

    jobs["skill_coverage"] = skill_coverages
    jobs["matching_skills"] = matching_lists
    jobs["missing_skills"] = missing_lists

    # Calculate combined score
    jobs["match_score"] = (
        jobs["text_similarity"] * 0.4 +
        jobs["skill_coverage"] * 0.6
    )

    # Rank jobs by combined score
    jobs = jobs.sort_values(
        by="match_score",
        ascending=False
    ).reset_index(drop=True)

    return jobs


if __name__ == "__main__":

    sample_resume = """
    Cybersecurity student with knowledge of Python,
    Linux, Networking, SQL, Wireshark, Nmap,
    HTML, Machine Learning and AWS.
    """

    results = match_jobs(sample_resume)

    print("\nAI JOB RECOMMENDATIONS")
    print("=" * 60)

    print(
        results[
            [
                "job_title",
                "text_similarity",
                "skill_coverage",
                "match_score"
            ]
        ].head(10).to_string(
            index=False,
            formatters={
                "text_similarity": "{:.2f}%".format,
                "skill_coverage": "{:.2f}%".format,
                "match_score": "{:.2f}%".format
            }
        )
    )
