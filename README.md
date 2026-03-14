# SkillLens 🌿
### An intelligent skill gap analyzer for tech careers

I built this because I was tired of not knowing where I stood. Every job description I read looked different — one asked for Python and TensorFlow, another asked for Docker and Kubernetes and I had no idea if I was even close to ready. So I built a tool that actually tells you.

**Live app →** [Add your Streamlit URL here]  
**GitHub →** [https://github.com/MeEko0001/skilllens](https://github.com/MeEko0001/skilllens)

---

## What it does

You pick a role, tap the skills you already have, and SkillLens tells you exactly where you stand and your match score, what you're missing, and a personalised roadmap to close the gap.

It covers 59 tech roles across data, engineering, security, design, and more. The skill requirements come from the O*NET occupational database (US Department of Labor), so it's not just made up but it reflects what these roles actually need.

---

## Features

**Analyze** - Pick a role from 59 options, select your skills from 150+ chips, get a match score with matched and missing skills broken down clearly.

**Roadmap** - A step-by-step learning roadmap built around your specific skill gaps. Not generic advice — tailored to what you're actually missing.

**Explorer** - Browse all 59 roles filtered by difficulty, salary, and required skills. Useful when you're not sure what to aim for yet.

**Compare** - Pick two roles side by side and see how they differ in skills, salary, and difficulty.

**ML Recommendations** - Based on your skill profile, the app suggests roles you're already a good fit for. Built using cosine similarity with scikit-learn.

**Reports** - Every analysis you run gets saved to your account. You can also download them as HTML files.

**Dashboard** - See your saved reports, track trending skills, and monitor demand scores across the tech landscape.

---

## Tech stack

| What | Why |
|------|-----|
| Python | Everything is Python end to end |
| Streamlit | UI framework - fast to build, easy to deploy |
| Supabase | Auth + PostgreSQL database with row-level security |
| scikit-learn | Cosine similarity for ML-based role recommendations |
| Pandas | Data processing and skill mapping |
| Plotly | Interactive charts and visualisations |
| O*NET Database | Real occupational skills data (US Dept. of Labor) |
| Google Fonts | Fraunces + Inter for typography |
| GitHub + Streamlit Cloud | Version control and deployment |

---

## Project structure

```
skilllens/
├── streamlit_app.py          # Entry point + navbar
├── pages/
│   ├── auth.py               # Sign in / Create account
│   ├── home.py               # Landing page
│   ├── analyze.py            # Skill gap analysis
│   ├── dashboard.py          # Reports + trending skills
│   ├── reports.py            # Saved reports + download
│   ├── roadmap.py            # Learning roadmap
│   ├── explorer.py           # Browse all roles
│   └── compare.py            # Side-by-side role comparison
├── modules/
│   ├── skill_analyzer.py     # Core analysis logic
│   ├── demand_score.py       # Skill demand scoring
│   ├── role_recommender.py   # ML recommendations
│   └── roadmap_generator.py  # Roadmap generation
├── database/
│   └── supabase_client.py    # Auth + DB operations
├── data/
│   └── job_skills.csv        # 59 roles with skills, salary, difficulty
└── requirements.txt
```

---

## Running it locally

**1. Clone the repo**
```bash
git clone https://github.com/MeEko0001/skilllens.git
cd skilllens
```

**2. Set up a virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**3. Set up Supabase**

Create a project at [supabase.com](https://supabase.com) and run this SQL:

```sql
create table profiles (
  id uuid references auth.users(id) primary key,
  name text,
  email text,
  experience_level text,
  target_role text,
  created_at timestamp default now()
);

create table skill_reports (
  id uuid default gen_random_uuid() primary key,
  user_id uuid references auth.users(id),
  report_name text,
  role text,
  score integer,
  matched_skills text[],
  missing_skills text[],
  readiness text,
  salary text,
  difficulty text,
  created_at timestamp default now()
);

alter table profiles enable row level security;
alter table skill_reports enable row level security;

create policy "Users manage own profile"
  on profiles for all using (auth.uid() = id) with check (true);

create policy "Users manage own reports"
  on skill_reports for all using (auth.uid() = user_id) with check (true);
```

**4. Add your credentials**

Create `.streamlit/secrets.toml`:
```toml
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your-anon-key"
```

**5. Run**
```bash
streamlit run streamlit_app.py
```

---

## Deploying

This runs on Streamlit Cloud.

1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo, set `streamlit_app.py` as the entry point
4. Add your Supabase credentials under Settings → Secrets

---

## Design

The UI was designed from scratch — no templates. The colour palette is forest green (`#1A3C23`) on warm cream (`#EDEADE`), with Fraunces for headlines and Inter for body text. Every detail was intentional.

---

## Data

Skill requirements come from the **O*NET database** (release 29.0), published by the US Department of Labor's Employment and Training Administration. Salary ranges reflect Indian market figures for each role.

---
