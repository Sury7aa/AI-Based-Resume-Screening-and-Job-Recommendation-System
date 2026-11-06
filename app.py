import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from html import escape

from resume_parser import extract_resume_text
from skill_extractor import extract_skills
from job_matcher import match_jobs

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="ResumeAI | Talent Intelligence",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).resolve().parent
JOBS_FILE = BASE_DIR / "data" / "jobs.csv"

# ---------------------------------------------------------
# PROFESSIONAL DARK UI
# ---------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #0b1020;
    --panel: #111a2e;
    --panel2: #151f35;
    --border: #25324b;
    --muted: #91a0b8;
    --text: #edf3ff;
    --accent: #7c8cff;
    --accent2: #39d6bd;
}
.stApp {
    background:
      radial-gradient(ellipse at 15% 0%, rgba(91,111,255,.13), transparent 34%),
      radial-gradient(ellipse at 95% 10%, rgba(57,214,189,.07), transparent 28%),
      var(--bg);
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
}
[data-testid="stSidebar"] {
    background: #0e1729;
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] > div { padding-top: 1.5rem; }
.block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 1500px; }
h1, h2, h3, h4 { color: var(--text) !important; letter-spacing: -.4px; }
p, label, .stMarkdown { color: #c4cee0; }
.small-muted { color: var(--muted); font-size: 13px; }
.brand {
    font-size: 25px; font-weight: 800; letter-spacing: -.8px;
    color: #f5f7ff; margin-bottom: 2px;
}
.brand-mark {
    display:inline-flex; align-items:center; justify-content:center;
    width:34px; height:34px; border-radius:11px; margin-right:9px;
    background: linear-gradient(135deg,#7888ff,#43d8c3);
    color:#08101d; font-weight:900;
}
.hero {
    padding: 27px 30px; border-radius: 20px; margin-bottom: 25px;
    background: linear-gradient(115deg, rgba(34,48,82,.96), rgba(17,30,51,.94));
    border: 1px solid #304263;
    box-shadow: 0 14px 45px rgba(0,0,0,.18);
}
.hero-kicker {
    color: #9eafff; text-transform: uppercase; letter-spacing: 1.7px;
    font-size: 11px; font-weight: 800; margin-bottom: 9px;
}
.hero-title { color:#fff; font-size:31px; font-weight:800; line-height:1.15; }
.hero-sub { color:#b3c0d6; font-size:14px; margin-top:9px; }
.section-head { font-size:19px; font-weight:750; color:#f0f4ff; margin: 8px 0 3px; }
.section-sub { color:var(--muted); font-size:13px; margin-bottom:15px; }
.metric-card {
    background: linear-gradient(145deg,#17233b,#111a2d);
    border:1px solid #293956; border-radius:16px;
    padding:18px 19px; min-height:112px;
}
.metric-label { color:#9eacc4; font-size:12px; font-weight:600; }
.metric-value { color:#f5f7ff; font-size:27px; font-weight:800; margin-top:7px; }
.metric-note { color:#7f91ae; font-size:11px; margin-top:2px; }
.job-card {
    background: linear-gradient(145deg,#15223a,#111a2c);
    border:1px solid #2a3a57; border-radius:15px;
    padding:17px 19px; margin-bottom:12px;
}
.job-title { font-size:16px; color:#f3f6ff; font-weight:750; }
.job-meta { color:#93a3bd; font-size:12px; margin-top:4px; }
.score {
    display:inline-block; padding:6px 10px; border-radius:9px;
    background:rgba(57,214,189,.12); color:#5de4ce;
    border:1px solid rgba(57,214,189,.25); font-weight:800; font-size:14px;
}
.tag {
    display:inline-block; padding:5px 9px; margin:3px 4px 3px 0;
    border-radius:8px; background:#1c2a43; border:1px solid #30415f;
    color:#c9d5eb; font-size:12px;
}
.tag-good { background:rgba(57,214,189,.09); border-color:rgba(57,214,189,.25); color:#70e4d2; }
.tag-missing { background:rgba(255,174,92,.08); border-color:rgba(255,174,92,.22); color:#ffc17e; }
.info-panel {
    background:#121e33; border:1px solid #293956; border-radius:14px;
    padding:17px 19px; margin:8px 0 14px;
}
div[data-testid="stMetric"] {
    background:#15223a; border:1px solid #2a3a57;
    padding:13px 15px; border-radius:13px;
}
.stButton > button {
    border-radius:10px; border:1px solid #6477e9;
    background:linear-gradient(100deg,#6879ed,#5668d8);
    color:white; font-weight:700; min-height:43px;
}
.stButton > button:hover { border-color:#9eabff; color:white; }
div[data-baseweb="select"] > div, .stTextArea textarea, .stTextInput input {
    background:#111c30 !important; border-color:#2b3b58 !important;
}
hr { border-color:#263650 !important; }
[data-testid="stDataFrame"] { border:1px solid #263650; border-radius:12px; }
footer {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# HELPERS
# ---------------------------------------------------------
def metric_card(label, value, note=""):
    st.markdown(
        f"""<div class="metric-card">
        <div class="metric-label">{escape(str(label))}</div>
        <div class="metric-value">{escape(str(value))}</div>
        <div class="metric-note">{escape(str(note))}</div>
        </div>""",
        unsafe_allow_html=True
    )

def render_tags(items, style=""):
    if not items:
        st.caption("None identified.")
        return
    class_name = "tag"
    if style == "good":
        class_name += " tag-good"
    elif style == "missing":
        class_name += " tag-missing"
    markup = "".join(
        f'<span class="{class_name}">{escape(str(item))}</span>'
        for item in items
    )
    st.markdown(markup, unsafe_allow_html=True)

def section(title, subtitle=None):
    st.markdown(f'<div class="section-head">{title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="section-sub">{subtitle}</div>', unsafe_allow_html=True)

def score_label(value):
    if value >= 70:
        return "Strong alignment"
    if value >= 40:
        return "Moderate alignment"
    return "Explore and improve"

# ---------------------------------------------------------
# DATA
# ---------------------------------------------------------
@st.cache_data
def load_jobs():
    return pd.read_csv(JOBS_FILE)

try:
    jobs_data = load_jobs()
except Exception as exc:
    st.error(f"Could not load the job dataset: {exc}")
    st.stop()

required_columns = {
    "job_title", "category", "description", "skills",
    "experience_level", "min_experience", "responsibilities"
}
missing_columns = required_columns - set(jobs_data.columns)
if missing_columns:
    st.error(
        "Your jobs.csv is missing these columns: "
        + ", ".join(sorted(missing_columns))
        + ". Please regenerate the expanded job dataset."
    )
    st.stop()

if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = None
if "resume_skills" not in st.session_state:
    st.session_state.resume_skills = []
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
with st.sidebar:
    st.markdown(
        '<div class="brand"><span class="brand-mark">R</span>ResumeAI</div>',
        unsafe_allow_html=True
    )
    st.caption("TALENT INTELLIGENCE PLATFORM")
    st.divider()

    page = st.radio(
        "WORKSPACE",
        ["Resume Analyzer", "Job Explorer", "About Project"],
        label_visibility="visible"
    )

    st.divider()
    st.markdown("**DATASET OVERVIEW**")
    st.metric("Job profiles", len(jobs_data))
    st.metric("Categories", jobs_data["category"].nunique())
    st.caption("Academic prototype • Human-reviewed recommendations")

    st.divider()
    st.markdown(
        '<div class="small-muted">RESUMEAI<br>Smart screening. Better discovery.</div>',
        unsafe_allow_html=True
    )

# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
st.markdown(
    """<div class="hero">
    <div class="hero-kicker">AI-powered recruitment workspace</div>
    <div class="hero-title">Find the roles that fit your skills.</div>
    <div class="hero-sub">Analyze resume content, understand skill coverage, and explore relevant job profiles.</div>
    </div>""",
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# PAGE 1 — RESUME ANALYZER
# ---------------------------------------------------------
if page == "Resume Analyzer":
    section("Resume analysis", "Upload a PDF resume or paste the resume text to begin.")

    input_col, guide_col = st.columns([1.55, 1], gap="large")

    with input_col:
        st.markdown('<div class="info-panel">', unsafe_allow_html=True)
        input_method = st.radio(
            "Resume input method",
            ["Upload PDF", "Paste resume text"],
            horizontal=True
        )
        resume_text = ""

        if input_method == "Upload PDF":
            uploaded_file = st.file_uploader(
                "Choose a PDF resume",
                type=["pdf"],
                help="Text-based PDFs work best. Scanned image-only PDFs may not extract correctly."
            )
            if uploaded_file is not None:
                resume_text = extract_resume_text(uploaded_file)
                if resume_text and not resume_text.startswith("Error reading PDF:"):
                    st.success(f"PDF loaded • {len(resume_text.split())} words extracted")
        else:
            resume_text = st.text_area(
                "Paste your resume content",
                height=190,
                placeholder="Include your education, technical skills, projects, certifications and experience..."
            )
        analyze = st.button("✦  Analyze resume", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with guide_col:
        st.markdown(
            """<div class="info-panel">
            <div class="section-head">What you'll get</div>
            <p class="small-muted">A structured view of how your resume aligns with the available job profiles.</p>
            <p>✦ &nbsp; Detected technical skills</p>
            <p>✦ &nbsp; Ranked job recommendations</p>
            <p>✦ &nbsp; Matching and missing skills</p>
            <p>✦ &nbsp; Job requirements and responsibilities</p>
            </div>""",
            unsafe_allow_html=True
        )

    if analyze:
        if not resume_text or not resume_text.strip():
            st.warning("Please upload a PDF or paste your resume text first.")
        elif resume_text.startswith("Error reading PDF:"):
            st.error(resume_text)
        else:
            with st.spinner("Analyzing resume and comparing job profiles..."):
                try:
                    results = match_jobs(resume_text)
                    skills = extract_skills(resume_text)
                    st.session_state.analysis_results = results
                    st.session_state.resume_skills = skills
                    st.session_state.resume_text = resume_text
                    st.success("Analysis completed successfully.")
                except Exception as exc:
                    st.error(f"Analysis failed: {exc}")

    if st.session_state.analysis_results is not None:
        results = st.session_state.analysis_results.copy()
        skills = st.session_state.resume_skills

        st.divider()
        section("Candidate overview", "A quick snapshot of the submitted resume.")
        top_score = float(results.iloc[0]["match_score"]) if not results.empty else 0
        k1, k2, k3, k4 = st.columns(4, gap="medium")
        with k1:
            metric_card("SKILLS DETECTED", len(skills), "Recognized technical skills")
        with k2:
            metric_card("JOBS ANALYZED", len(results), "Profiles compared")
        with k3:
            metric_card("TOP MATCH SCORE", f"{top_score:.1f}%", score_label(top_score))
        with k4:
            metric_card("JOB CATEGORIES", jobs_data["category"].nunique(), "Areas represented")

        st.markdown("")
        section("Detected skills", "Skills recognized from the resume text.")
        if skills:
            render_tags(skills, "good")
        else:
            st.info("No skills from the current skill dictionary were detected.")

        st.divider()
        section("Recommended job profiles", "Ranked using text similarity and required-skill coverage.")

        filter_col, sort_col = st.columns([2, 1])
        with filter_col:
            categories = st.multiselect(
                "Filter categories",
                sorted(results["category"].dropna().unique().tolist()),
                default=sorted(results["category"].dropna().unique().tolist())
            )
        with sort_col:
            number_to_show = st.selectbox("Profiles to display", [5, 10, 20, "All"], index=1)

        filtered = results[results["category"].isin(categories)].copy()
        if number_to_show != "All":
            visible = filtered.head(int(number_to_show))
        else:
            visible = filtered

        if filtered.empty:
            st.warning("No profiles match the selected categories.")
        else:
            for _, job in visible.iterrows():
                score = float(job["match_score"])
                st.markdown(
                    f"""<div class="job-card">
                    <div style="display:flex;justify-content:space-between;gap:12px;align-items:center;">
                      <div>
                        <div class="job-title">{escape(str(job['job_title']))}</div>
                        <div class="job-meta">{escape(str(job['category']))} &nbsp;•&nbsp; {escape(str(job['experience_level']))}</div>
                      </div>
                      <div class="score">{score:.1f}% match</div>
                    </div>
                    </div>""",
                    unsafe_allow_html=True
                )

            chart_data = filtered.head(10).sort_values("match_score", ascending=True)
            fig = px.bar(
                chart_data,
                x="match_score",
                y="job_title",
                orientation="h",
                color="category",
                labels={
                    "match_score": "Combined alignment score (%)",
                    "job_title": "Job profile",
                    "category": "Category"
                },
                title="Top matching roles"
            )
            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=390,
                margin=dict(l=10, r=15, t=55, b=15),
                xaxis=dict(range=[0, 100], gridcolor="#263650"),
                yaxis=dict(title="")
            )
            st.plotly_chart(fig, use_container_width=True)

            csv_data = filtered.to_csv(index=False).encode("utf-8")
            st.download_button(
                "⬇ Download recommendations (CSV)",
                data=csv_data,
                file_name="resumeai_job_recommendations.csv",
                mime="text/csv"
            )

            st.divider()
            section("Role intelligence", "Select a recommendation to inspect its requirements.")
            selected_job = st.selectbox(
                "Choose a job profile",
                filtered["job_title"].tolist()
            )
            job = filtered[filtered["job_title"] == selected_job].iloc[0]

            a, b, c = st.columns(3)
            a.metric("Combined alignment", f"{job['match_score']:.1f}%")
            b.metric("Text similarity", f"{job['text_similarity']:.1f}%")
            c.metric("Skill coverage", f"{job['skill_coverage']:.1f}%")

            left, right = st.columns([1.2, 1], gap="large")
            with left:
                st.markdown('<div class="info-panel">', unsafe_allow_html=True)
                st.markdown("**Role description**")
                st.write(job["description"])
                st.markdown("**Key responsibilities**")
                st.write(job["responsibilities"])
                st.markdown("**Experience requirement**")
                st.write(
                    f"{job['experience_level']} • Minimum {job['min_experience']} year(s)"
                )
                st.markdown('</div>', unsafe_allow_html=True)

            with right:
                st.markdown('<div class="info-panel">', unsafe_allow_html=True)
                st.markdown("**Required skills**")
                required = [x.strip() for x in str(job["skills"]).split(",") if x.strip()]
                render_tags(required)
                st.markdown('</div>', unsafe_allow_html=True)

            skill_left, skill_right = st.columns(2, gap="large")
            with skill_left:
                section("Skills you have", "Required skills detected in your resume.")
                render_tags(job["matching_skills"], "good")
            with skill_right:
                section("Skills to develop", "Required skills not detected in your resume.")
                render_tags(job["missing_skills"], "missing")

            breakdown = pd.DataFrame({
                "Skill status": ["Matching", "Not detected"],
                "Count": [len(job["matching_skills"]), len(job["missing_skills"])]
            })
            if breakdown["Count"].sum() > 0:
                fig = px.pie(
                    breakdown, names="Skill status", values="Count",
                    hole=0.62, title="Selected role: skill coverage"
                )
                fig.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(l=10, r=10, t=55, b=10),
                    height=300
                )
                st.plotly_chart(fig, use_container_width=True)

        st.caption(
            "Important: Scores represent resume-to-job alignment within this project's dataset. "
            "They are not a probability of being hired. Recommendations should be reviewed by a human."
        )

# ---------------------------------------------------------
# PAGE 2 — JOB EXPLORER
# ---------------------------------------------------------
elif page == "Job Explorer":
    section("Job explorer", "Browse the job profiles included in the project dataset.")

    f1, f2, f3 = st.columns([1.2, 1.2, 1.5])
    with f1:
        category_filter = st.selectbox(
            "Category",
            ["All categories"] + sorted(jobs_data["category"].dropna().unique().tolist())
        )
    with f2:
        level_filter = st.selectbox(
            "Experience level",
            ["All levels"] + sorted(jobs_data["experience_level"].dropna().unique().tolist())
        )
    with f3:
        search_term = st.text_input("Search job titles", placeholder="e.g. Python, analyst, cloud")

    explorer = jobs_data.copy()
    if category_filter != "All categories":
        explorer = explorer[explorer["category"] == category_filter]
    if level_filter != "All levels":
        explorer = explorer[explorer["experience_level"] == level_filter]
    if search_term.strip():
        explorer = explorer[
            explorer["job_title"].str.contains(search_term, case=False, na=False)
        ]

    m1, m2 = st.columns(2)
    m1.metric("Profiles found", len(explorer))
    m2.metric("Categories shown", explorer["category"].nunique() if not explorer.empty else 0)

    if explorer.empty:
        st.info("No job profiles match these filters.")
    else:
        st.dataframe(
            explorer[[
                "job_title", "category", "experience_level",
                "min_experience", "skills"
            ]],
            use_container_width=True,
            hide_index=True
        )

        st.divider()
        section("Explore a role", "Open a profile to review its description and requirements.")
        selected = st.selectbox("Select a role", explorer["job_title"].tolist())
        job = explorer[explorer["job_title"] == selected].iloc[0]

        st.markdown(
            f"""<div class="job-card">
            <div class="job-title" style="font-size:21px">{escape(str(job['job_title']))}</div>
            <div class="job-meta">{escape(str(job['category']))} &nbsp;•&nbsp;
            {escape(str(job['experience_level']))} &nbsp;•&nbsp;
            {escape(str(job['min_experience']))} year(s) minimum experience</div>
            </div>""",
            unsafe_allow_html=True
        )
        l, r = st.columns(2, gap="large")
        with l:
            st.markdown("**Role description**")
            st.write(job["description"])
            st.markdown("**Responsibilities**")
            st.write(job["responsibilities"])
        with r:
            st.markdown("**Required skills**")
            required = [x.strip() for x in str(job["skills"]).split(",") if x.strip()]
            render_tags(required)

# ---------------------------------------------------------
# PAGE 3 — ABOUT
# ---------------------------------------------------------
elif page == "About Project":
    section("About ResumeAI", "Project overview and technical workflow.")

    st.markdown(
        """<div class="info-panel">
        <div class="section-head">AI-based resume screening and job recommendation</div>
        <p class="small-muted">
        ResumeAI is an academic prototype that reads resume content, identifies
        technical skills, and compares the resume with job profiles in a local dataset.
        It helps users understand role alignment and identify skills they may want to develop.
        </p>
        </div>""",
        unsafe_allow_html=True
    )

    st.markdown("### Technology stack")
    tech = [
        "Python", "Pandas", "Scikit-learn", "TF-IDF Vectorization",
        "Cosine Similarity", "Streamlit", "Plotly", "PyPDF2"
    ]
    render_tags(tech)

    st.markdown("### System workflow")
    workflow = [
        ("01", "Resume input", "Upload a PDF or paste resume text."),
        ("02", "Text extraction", "Extract readable text from the resume."),
        ("03", "Skill identification", "Identify skills using the project's skill dictionary."),
        ("04", "Text comparison", "Use TF-IDF and cosine similarity to compare resume and job text."),
        ("05", "Skill coverage", "Calculate the proportion of listed job skills found in the resume."),
        ("06", "Job ranking", "Combine text similarity (40%) and skill coverage (60%) to rank roles."),
        ("07", "Recommendations", "Display matching skills, missing skills, and role information.")
    ]
    for number, title, description in workflow:
        st.markdown(
            f"""<div class="job-card" style="display:flex;gap:16px;align-items:flex-start;">
            <div class="score">{number}</div>
            <div><div class="job-title">{title}</div>
            <div class="job-meta">{description}</div></div></div>""",
            unsafe_allow_html=True
        )

    st.info(
        "This is a decision-support prototype, not an automated hiring system. "
        "Its skill dictionary and job dataset have limitations, and all recommendations "
        "require human review."
    )

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.divider()
st.markdown(
    '<div class="small-muted" style="text-align:center;">ResumeAI • Academic Project • AI-Based Resume Screening & Job Recommendation System</div>',
    unsafe_allow_html=True
)
