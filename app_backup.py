
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

from resume_parser import extract_resume_text
from skill_extractor import extract_skills
from job_matcher import match_jobs


# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="ResumeAI | Smart Recruitment",
    page_icon="📄",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parent
JOBS_FILE = BASE_DIR / "data" / "jobs.csv"


# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

.stApp {
    background-color: #0e1117;
}

[data-testid="stSidebar"] {
    background-color: #151a25;
}

.main-title {
    font-size: 34px;
    font-weight: 750;
    color: #ffffff;
}

.subtitle {
    color: #9ca3af;
    font-size: 15px;
}

.metric-card {
    background-color: #1b2333;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #293449;
}

.metric-label {
    color: #aab4c5;
    font-size: 14px;
}

.metric-value {
    color: #ffffff;
    font-size: 27px;
    font-weight: bold;
}

.section-title {
    color: #ffffff;
    font-size: 21px;
    font-weight: 650;
    margin-top: 15px;
}

div[data-testid="stMetric"] {
    background-color: #1b2333;
    padding: 15px;
    border-radius: 10px;
    border: 1px solid #293449;
}

</style>
""", unsafe_allow_html=True)


# ---------------- LOAD DATA ----------------

@st.cache_data
def load_jobs():
    return pd.read_csv(JOBS_FILE)


try:
    jobs_data = load_jobs()
except Exception as e:
    st.error(f"Could not load job dataset: {e}")
    st.stop()


# ---------------- SESSION STATE ----------------

if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = None

if "resume_skills" not in st.session_state:
    st.session_state.resume_skills = []

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""


# ---------------- SIDEBAR ----------------

st.sidebar.markdown("# 📄 ResumeAI")
st.sidebar.caption("AI-Powered Resume Screening")

st.sidebar.divider()

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Resume Analyzer",
        "Job Explorer",
        "About Project"
    ]
)

st.sidebar.divider()

st.sidebar.markdown("### Dataset Information")
st.sidebar.metric("Total Job Profiles", len(jobs_data))
st.sidebar.metric(
    "Job Categories",
    jobs_data["category"].nunique()
)

st.sidebar.caption("Academic AI recruitment prototype")


# ---------------- HEADER ----------------

st.markdown(
    '<div class="main-title">ResumeAI Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Smart resume analysis and job recommendations</div>',
    unsafe_allow_html=True
)

st.divider()


# ====================================================
# PAGE 1: RESUME ANALYZER
# ====================================================

if page == "Resume Analyzer":

    st.markdown("## 📋 Resume Analysis")

    st.write(
        "Upload your resume or paste its content to discover "
        "job profiles that align with your skills."
    )

    input_method = st.radio(
        "Choose resume input method",
        ["Upload PDF", "Enter Resume Text"],
        horizontal=True
    )

    resume_text = ""

    if input_method == "Upload PDF":

        uploaded_file = st.file_uploader(
            "Upload your resume",
            type=["pdf"]
        )

        if uploaded_file is not None:
            resume_text = extract_resume_text(uploaded_file)

    else:

        resume_text = st.text_area(
            "Paste your resume content",
            height=250,
            placeholder="Paste your education, technical skills, projects and experience..."
        )

    analyze_button = st.button(
        "🚀 Analyze My Resume",
        type="primary",
        use_container_width=True
    )

    if analyze_button:

        if not resume_text or not resume_text.strip():

            st.warning("Please upload a PDF or enter resume text.")

        elif resume_text.startswith("Error reading PDF:"):

            st.error(resume_text)

        else:

            with st.spinner("Analyzing your resume and matching jobs..."):

                try:

                    results = match_jobs(resume_text)
                    skills = extract_skills(resume_text)

                    st.session_state.analysis_results = results
                    st.session_state.resume_skills = skills
                    st.session_state.resume_text = resume_text

                    st.success("Resume analyzed successfully!")

                except Exception as e:

                    st.error(f"Analysis failed: {e}")


    # DISPLAY ANALYSIS RESULTS

    if st.session_state.analysis_results is not None:

        results = st.session_state.analysis_results
        skills = st.session_state.resume_skills

        st.divider()

        st.markdown("## 📊 Candidate Overview")

        # KPI CARDS

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Skills Detected",
            len(skills)
        )

        col2.metric(
            "Jobs Analyzed",
            len(results)
        )

        col3.metric(
            "Top Match",
            f"{results.iloc[0]['match_score']:.1f}%"
        )

        col4.metric(
            "Job Categories",
            jobs_data["category"].nunique()
        )

        # EXTRACTED SKILLS

        st.markdown('<div class="section-title">🧠 Detected Skills</div>',
                    unsafe_allow_html=True)

        if skills:

            st.write("  •  ".join(skills))

        else:

            st.info("No recognized skills were detected.")

        st.divider()

        # JOB RECOMMENDATIONS

        st.markdown("## 🎯 Job Recommendations")

        selected_categories = st.multiselect(
            "Filter by job category",
            options=sorted(results["category"].unique()),
            default=sorted(results["category"].unique())
        )

        filtered_results = results[
            results["category"].isin(selected_categories)
        ]

        if filtered_results.empty:

            st.warning("No jobs found for the selected categories.")

        else:

            display_results = filtered_results[
                [
                    "job_title",
                    "category",
                    "experience_level",
                    "text_similarity",
                    "skill_coverage",
                    "match_score"
                ]
            ].copy()

            display_results = display_results.rename(
                columns={
                    "job_title": "Job Title",
                    "category": "Category",
                    "experience_level": "Experience Level",
                    "text_similarity": "Text Similarity (%)",
                    "skill_coverage": "Skill Coverage (%)",
                    "match_score": "Combined Match (%)"
                }
            )

            st.dataframe(
                display_results.head(10).style.format({
                    "Text Similarity (%)": "{:.1f}%",
                    "Skill Coverage (%)": "{:.1f}%",
                    "Combined Match (%)": "{:.1f}%"
                }),
                use_container_width=True,
                hide_index=True
            )

            # RECOMMENDATION CHART

            st.markdown("### Job Match Comparison")

            chart_data = filtered_results.head(10)

            fig = px.bar(
                chart_data,
                x="match_score",
                y="job_title",
                orientation="h",
                color="category",
                labels={
                    "match_score": "Combined Match Score (%)",
                    "job_title": "Job Title",
                    "category": "Category"
                },
                title="Top 10 Matching Jobs"
            )

            fig.update_layout(
                template="plotly_dark",
                yaxis={"categoryorder": "total ascending"},
                xaxis={"range": [0, 100]}
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            st.divider()

            # DETAILED JOB ANALYSIS

            st.markdown("## 🔍 Detailed Job Analysis")

            selected_job = st.selectbox(
                "Select a job to inspect",
                filtered_results["job_title"].tolist()
            )

            job = filtered_results[
                filtered_results["job_title"] == selected_job
            ].iloc[0]

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Combined Match",
                f"{job['match_score']:.1f}%"
            )

            col2.metric(
                "Text Similarity",
                f"{job['text_similarity']:.1f}%"
            )

            col3.metric(
                "Skill Coverage",
                f"{job['skill_coverage']:.1f}%"
            )

            st.markdown("### Job Description")
            st.write(job["description"])

            st.markdown("### Required Skills")
            st.write(job["skills"])

            st.markdown("### Experience Information")
            st.write(
                f"Level: {job['experience_level']} | "
                f"Minimum experience: {job['min_experience']} years"
            )

            st.markdown("### Responsibilities")
            st.write(job["responsibilities"])

            # MATCHING AND MISSING SKILLS

            matching = job["matching_skills"]
            missing = job["missing_skills"]

            skill_col1, skill_col2 = st.columns(2)

            with skill_col1:

                st.markdown("### ✅ Matching Skills")

                if matching:
                    for skill in matching:
                        st.success(skill)
                else:
                    st.info("No matching skills found.")

            with skill_col2:

                st.markdown("### ⚠️ Missing Skills")

                if missing:
                    for skill in missing:
                        st.warning(skill)
                else:
                    st.success("All listed skills are covered!")

            # SKILL CHART

            skill_chart_data = pd.DataFrame({
                "Skill Type": ["Matching Skills", "Missing Skills"],
                "Count": [len(matching), len(missing)]
            })

            fig = px.pie(
                skill_chart_data,
                names="Skill Type",
                values="Count",
                hole=0.55,
                title="Skill Coverage Breakdown"
            )

            fig.update_layout(template="plotly_dark")

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        st.caption(
            "Scores indicate resume-to-job alignment, not hiring probability. "
            "Recommendations require human review."
        )


# ====================================================
# PAGE 2: JOB EXPLORER
# ====================================================

elif page == "Job Explorer":

    st.markdown("## 💼 Job Explorer")

    st.write(
        "Explore all job profiles available in the project's dataset."
    )

    category_filter = st.selectbox(
        "Select Job Category",
        ["All Categories"] + sorted(jobs_data["category"].unique())
    )

    level_filter = st.selectbox(
        "Select Experience Level",
        ["All Levels"] + sorted(jobs_data["experience_level"].unique())
    )

    explorer_data = jobs_data.copy()

    if category_filter != "All Categories":

        explorer_data = explorer_data[
            explorer_data["category"] == category_filter
        ]

    if level_filter != "All Levels":

        explorer_data = explorer_data[
            explorer_data["experience_level"] == level_filter
        ]

    st.metric("Available Job Profiles", len(explorer_data))

    st.dataframe(
        explorer_data[
            [
                "job_title",
                "category",
                "experience_level",
                "min_experience",
                "skills"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    selected_job = st.selectbox(
        "View Job Details",
        explorer_data["job_title"].tolist()
    )

    if selected_job:

        job = explorer_data[
            explorer_data["job_title"] == selected_job
        ].iloc[0]

        st.markdown(f"### {job['job_title']}")

        st.write("**Category:**", job["category"])
        st.write("**Experience Level:**", job["experience_level"])
        st.write("**Minimum Experience:**", job["min_experience"], "years")

        st.write("**Description:**", job["description"])
        st.write("**Required Skills:**", job["skills"])
        st.write("**Responsibilities:**", job["responsibilities"])


# ====================================================
# PAGE 3: ABOUT PROJECT
# ====================================================

elif page == "About Project":

    st.markdown("## 🤖 About ResumeAI")

    st.write("""
    ResumeAI is an academic AI-based resume screening and
    job recommendation prototype.

    It analyzes resume content, extracts technical skills
    and compares candidates against available job profiles.
    """)

    st.markdown("### Technologies Used")

    technologies = [
        "Python",
        "Pandas",
        "Scikit-learn",
        "TF-IDF Vectorization",
        "Cosine Similarity",
        "Streamlit",
        "Plotly",
        "PyPDF2"
    ]

    for technology in technologies:
        st.write(f"• {technology}")

    st.markdown("### How the System Works")

    st.write("""
    1. Candidate uploads a resume or enters resume text.
    2. The system extracts text from the resume.
    3. Technical skills are identified.
    4. Resume text is compared with job descriptions.
    5. Skill coverage is calculated.
    6. Jobs are ranked based on the combined score.
    7. Matching and missing skills are displayed.
    """)

    st.info(
        "This system is designed to assist human reviewers. "
        "It does not make automatic hiring or rejection decisions."
    )


# ---------------- FOOTER ----------------

st.divider()

st.caption(
    "ResumeAI | Academic Project | AI-Based Resume Screening "
    "and Job Recommendation System"
)
