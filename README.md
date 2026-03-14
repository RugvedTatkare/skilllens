# SkillLens 🌿
### An intelligent skill gap analyzer for tech careers

I built this because I was tired of not knowing where I stood. Every job description I read looked different and I had no idea if I was even close to ready. So I built a tool that actually tells you.

**Live app →** [Add your Streamlit URL here]
**GitHub →** [https://github.com/MeEko0001/skilllens](https://github.com/MeEko0001/skilllens)

---

## What it does

You pick a role, tap the skills you already have, and SkillLens tells you your match score, what you're missing, and gives you a personalised roadmap to close the gap.

59 tech roles. 150+ skills. Real data.

---

## Features

**Analyze** - Pick a role, select your skills from 150+ chips, get a match score with matched and missing skills broken down clearly.

**Roadmap** - Step-by-step learning path built around your specific skill gaps.

**Explorer** - Browse all 59 roles filtered by difficulty, salary, and required skills.

**Compare** - Pick two roles side by side and see how they differ.

**ML Recommendations** - Suggests roles you're already a good fit for using cosine similarity.

**Reports** - Every analysis gets saved to your account. Download as HTML.

**Dashboard** - Track your saved reports, trending skills, and demand scores.

---

## Tech stack

| | |
|---|---|
| Python | Everything is Python end to end |
| Streamlit | UI framework, deployed on Streamlit Cloud |
| Supabase | Auth + PostgreSQL database with row-level security |
| scikit-learn | Cosine similarity for ML-based role recommendations |
| Pandas | Data processing and skill mapping |
| Plotly | Interactive charts and visualisations |
| Google Fonts | Fraunces + Inter for typography |

---

## Data

Three real datasets were used to build the skill and salary data:

- **O*NET Database** (US Department of Labor) — occupational skill requirements per role
- **Stack Overflow Developer Survey 2024** — real tools and languages used by developers per role
- **LinkedIn Job Postings Dataset** — Indian salary ranges extracted from real job postings

All three were processed and combined into a single clean dataset covering 59 tech roles.

---

## Project structure

```
skilllens/
├── streamlit_app.py
├── pages/
│   ├── auth.py
│   ├── home.py
│   ├── analyze.py
│   ├── dashboard.py
│   ├── reports.py
│   ├── roadmap.py
│   ├── explorer.py
│   └── compare.py
├── modules/
│   ├── skill_analyzer.py
│   ├── demand_score.py
│   ├── role_recommender.py
│   └── roadmap_generator.py
├── database/
│   └── supabase_client.py
├── data/
│   └── job_skills.csv
└── requirements.txt
```

---

## Running locally

```bash
git clone https://github.com/MeEko0001/skilllens.git
cd skilllens
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create `.streamlit/secrets.toml`:
```toml
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your-anon-key"
```

Set up your Supabase tables — run the SQL in `database/supabase_client.py` comments.

```bash
streamlit run streamlit_app.py
```

---

## Design

Built from scratch — no templates. Forest green (`#1A3C23`) on warm cream (`#EDEADE`), Fraunces for headlines, Inter for body text.

---

