# 🚀 GitGrade AI

**GitGrade AI** is an explainable, engineering-focused system that evaluates GitHub repositories and converts them into a **Score, Technical Summary, and Personalized Improvement Roadmap**.

It mirrors how **recruiters and senior engineers** review projects — focusing on **code quality, documentation, Git practices, testing, and real-world readiness**.

---

## 🧠 Problem Statement

A GitHub repository is a developer’s strongest proof of skill, yet most students don’t know:
- how clean their code looks,
- whether their project is recruiter-ready,
- what exactly to improve next.

**GitGrade AI acts as a “Repository Mirror”** — reflecting real strengths and weaknesses using transparent technical metrics instead of vague AI judgments.

---

## ✨ Key Features

- 🔢 Repository Score (0–100)
- 🏅 Skill Level Badge (Beginner / Intermediate / Advanced)
- 📊 Visual Score Breakdown (parameter-wise progress bars)
- 📄 Technical Summary of the Repository
- 🛣️ Personalized Improvement Roadmap
- 🧠 Explainable Evaluation Framework
- 🌐 Live Web Interface (Streamlit)

---

## 🛠️ Technical Approaches Used

GitGrade AI is built using real-world software engineering and code-analysis techniques:

- **Static Code Analysis**  
  Cyclomatic complexity analysis using `radon` to assess readability and maintainability.

- **Deterministic Scoring Rubric**  
  A predefined, weighted scoring system ensures fairness and reproducibility.

- **Repository Structure Analysis**  
  Evaluates folder depth, modularity, and scalability.

- **Documentation Quality Evaluation**  
  Parses README files for setup instructions, usage clarity, and completeness.

- **Version Control Best Practices Analysis**  
  Analyzes commit frequency, commit message semantics, and branching strategy.

- **Test Coverage Heuristics**  
  Detects presence of unit and integration tests to assess reliability.

- **CI/CD Pipeline Detection**  
  Identifies GitHub Actions workflows to evaluate deployment readiness.

- **Explainable Scoring System**  
  Every score component is shown transparently with visual indicators.

---

## 📊 Evaluation Parameters

| Parameter | Description |
|--------|------------|
| Code Quality | Cyclomatic complexity & readability |
| Documentation | README completeness & clarity |
| Testing | Presence of unit/integration tests |
| Commits | Commit frequency & consistency |
| Commit Messages | Semantic and meaningful messages |
| Branching | Usage of multiple branches |
| CI/CD | Automated workflow detection |
| Structure | Folder organization & modularity |

---

## 🧑‍💻 Who Is This For?

- 🎓 Students & beginners
- 💼 Job-seeking developers
- 🧑‍🏫 Mentors & educators
- 🧑‍💼 Recruiters & hiring teams

---

## 🚀 Live Demo

👉 **Public App Link:**  
(Add your Streamlit app link here after deployment)
---

## ⚙️ How to Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
