import streamlit as st
import os, shutil, subprocess, re
from git import Repo

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="GitGrade AI", page_icon="🚀", layout="wide")

# ---------------- SESSION STATE ----------------
if "analyzed" not in st.session_state:
    st.session_state.analyzed = False
if "repo_url" not in st.session_state:
    st.session_state.repo_url = ""

# ---------------- CSS ----------------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #f0f7ff, #fdf2f8, #f0fdf4);
}
.card {
    background:#ffffff;
    padding:1.8rem;
    border-radius:18px;
    box-shadow:0 10px 24px rgba(0,0,0,0.08);
    margin-bottom:1.6rem;
}
.section-title {
    font-size:20px;
    font-weight:700;
    margin-bottom:0.6rem;
}
.subtle {
    color:#475569;
    font-size:14px;
}
.score-box {
    font-size:48px;
    font-weight:800;
    color:#2563eb;
    text-align:center;
}
.badge {
    padding:0.4rem 1.2rem;
    border-radius:999px;
    font-size:14px;
    font-weight:600;
    color:white;
    display:inline-block;
}
.beginner { background:#f97316; }
.intermediate { background:#22c55e; }
.advanced { background:#6366f1; }
.roadmap-item {
    background:#eef2ff;
    padding:0.9rem 1.1rem;
    border-radius:14px;
    margin-bottom:0.6rem;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
c1, c2 = st.columns([0.08, 0.92])
with c1:
    st.image("https://cdn-icons-png.flaticon.com/512/733/733553.png", width=55)
with c2:
    st.markdown("""
    <h1 style="margin-bottom:4px;">GitGrade AI</h1>
    <h4 style="margin-top:0; color:#334155;">
        Turn GitHub Repositories into Recruiter-Ready Projects
    </h4>
    <p class="subtle">
        Explainable • Deterministic • Engineering-Focused Repository Evaluation
    </p>
    """, unsafe_allow_html=True)

# ---------------- INPUT ----------------
repo_url = st.text_input(
    "GitHub Repository URL",
    placeholder="https://github.com/username/repository",
    key="repo_url"
)

if st.button("✨ Analyze Repository"):
    st.session_state.analyzed = True

# ======================================================
# ================= FRONT PAGE =========================
# ======================================================
if not st.session_state.analyzed:

    st.markdown("""
    <div class="card">
    <div class="section-title">📘 About GitGrade AI</div>
    GitGrade AI evaluates GitHub repositories the same way recruiters and senior engineers do —
    focusing on code quality, documentation, Git discipline, testing, and project maturity.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
    <div class="section-title">🧠 Technical Approaches & Engineering Methods</div>
    • Static code analysis (cyclomatic complexity)<br>
    • Deterministic rubric-based scoring model<br>
    • Git commit & branching analysis<br>
    • README & documentation parsing<br>
    • Test coverage heuristics<br>
    • CI/CD pipeline detection<br>
    • Explainable parameter-wise scoring
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
    <div class="section-title">❓ Frequently Asked Questions</div>
    <b>Is this AI generated?</b><br>No. Scores are deterministic and reproducible.<br><br>
    <b>Will the score change?</b><br>Only if the repository changes.<br><br>
    <b>Who is this for?</b><br>Students, developers, mentors, recruiters.
    </div>
    """, unsafe_allow_html=True)

# ======================================================
# ================= ANALYSIS LOGIC =====================
# ======================================================
REPO_DIR = "temp_repo"

def clone_repo(url):
    if os.path.exists(REPO_DIR):
        shutil.rmtree(REPO_DIR)
    Repo.clone_from(url, REPO_DIR)

def complexity_score(path):
    try:
        o = subprocess.check_output(["radon","cc",path,"-a"], stderr=subprocess.DEVNULL).decode()
        return 20 if "A" in o else 15 if "B" in o else 10
    except:
        return 10

def readme_score(path):
    for f in os.listdir(path):
        if f.lower().startswith("readme"):
            return 10
    return 0

def has_tests(path):
    return any("test" in r.lower() for r,_,_ in os.walk(path))

def commit_score(repo):
    return min(len(list(repo.iter_commits())), 10)

def commit_message_score(repo):
    good = 0
    for c in repo.iter_commits(max_count=20):
        if re.search(r"(add|fix|update|refactor|remove)", c.message.lower()):
            good += 1
    return min(good, 10)

def branch_score(repo):
    return 5 if len(repo.branches) > 1 else 0

def ci_cd_score(path):
    return 5 if os.path.exists(os.path.join(path, ".github", "workflows")) else 0

# ======================================================
# ================= RESULTS DASHBOARD ==================
# ======================================================
if st.session_state.analyzed and st.session_state.repo_url:

    with st.spinner("Analyzing repository..."):
        clone_repo(st.session_state.repo_url)
        repo = Repo(REPO_DIR)

        scores = {
            "Code Quality": complexity_score(REPO_DIR),
            "Documentation": readme_score(REPO_DIR),
            "Testing": 10 if has_tests(REPO_DIR) else 0,
            "Commits": commit_score(repo),
            "Commit Messages": commit_message_score(repo),
            "Branches": branch_score(repo),
            "CI/CD": ci_cd_score(REPO_DIR)
        }

        max_scores = {
            "Code Quality": 20,
            "Documentation": 10,
            "Testing": 10,
            "Commits": 10,
            "Commit Messages": 10,
            "Branches": 5,
            "CI/CD": 5
        }

        total_score = min(sum(scores.values()), 100)

    # Badge
    if total_score < 50:
        badge, cls = "Beginner", "beginner"
    elif total_score < 80:
        badge, cls = "Intermediate", "intermediate"
    else:
        badge, cls = "Advanced", "advanced"

    st.success("🎉 Repository successfully evaluated!")

    left, right = st.columns(2)

    with left:
        st.markdown(f"""
        <div class="card">
            <div class="score-box">{total_score} / 100</div>
            <div style="text-align:center;margin-top:8px;">
                <span class="badge {cls}">{badge}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown("<div class='card'><div class='section-title'>📊 Score Analysis</div>", unsafe_allow_html=True)
        for k, v in scores.items():
            st.write(f"**{k}** — {v} / {max_scores[k]}")
            st.progress(v / max_scores[k])
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'><div class='section-title'>🛣️ Personalized Roadmap</div>", unsafe_allow_html=True)
    for k, v in scores.items():
        if v < max_scores[k]:
            st.markdown(f"<div class='roadmap-item'>Improve {k}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p class='subtle'>Built with ❤️ for GitGrade Hackathon | UnsaidTalks</p>", unsafe_allow_html=True)
