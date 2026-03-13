# SkillLens

**Intelligent Skill Gap Analyzer for Tech Roles**

SkillLens helps you understand exactly where you stand against any tech role — and gives you a clear, personalised path to get there.

---

## What it does

- **Skill Gap Analysis** — Select a target role, tap the skills you have, and instantly see your match score, matched skills, and what you're missing
- **30+ Tech Roles** — Data Scientist, ML Engineer, DevOps, Frontend, Backend, Blockchain, and more
- **Learning Roadmap** — Personalised step-by-step roadmap based on your skill gaps
- **Role Explorer** — Browse and filter all roles by difficulty, salary, and required skills
- **Role Comparison** — Compare two roles side-by-side
- **ML Recommendations** — Get role suggestions based on your existing skill profile
- **Reports** — Save and download your analysis reports as HTML files
- **Dashboard** — Track your saved reports, trending skills, and demand scores
- **Auth** — Secure sign up / sign in with Supabase

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit |
| Charts | Plotly |
| ML | scikit-learn (cosine similarity) |
| Auth & DB | Supabase (PostgreSQL + RLS) |
| Fonts | Fraunces + Inter (Google Fonts) |
| Deployment | Streamlit Cloud |

---

## Project Structure

```
skilllens/
├── streamlit_app.py          # Main app entry point + navbar
├── pages/
│   ├── auth.py               # Sign in / Create account
│   ├── home.py               # Landing + quick analysis
│   ├── analyze.py            # Skill tag cloud + gap analysis
│   ├── dashboard.py          # Reports overview + trending skills
│   ├── reports.py            # Saved reports + download
│   ├── roadmap.py            # Learning roadmap
│   ├── explorer.py           # Browse all roles
│   └── compare.py            # Side-by-side role comparison
├── modules/
│   ├── skill_analyzer.py     # Core analysis logic
│   ├── demand_score.py       # Skill demand scoring
│   ├── role_recommender.py   # ML-based role recommendations
│   └── roadmap_generator.py  # Roadmap generation
├── database/
│   └── supabase_client.py    # Auth + DB operations
├── data/
│   └── job_skills.csv        # Role → skills + salary + difficulty
├── fetch_onet_data.py        # Data fetch + SALARY_MAP (INR)
└── requirements.txt
```

---

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/MeEko0001/skilllens.git
cd skilllens
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up Supabase

Create a project at [supabase.com](https://supabase.com) and run these SQL statements:

```sql
-- Profiles table
create table profiles (
  id uuid references auth.users(id) primary key,
  name text,
  email text,
  experience_level text,
  target_role text,
  created_at timestamp default now()
);

-- Reports table
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

-- Enable RLS
alter table profiles enable row level security;
alter table skill_reports enable row level security;

create policy "Users manage own profile" on profiles for all using (auth.uid() = id) with check (true);
create policy "Users manage own reports" on skill_reports for all using (auth.uid() = user_id) with check (true);
```

### 5. Add your Supabase credentials

Create a `.streamlit/secrets.toml` file:

```toml
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your-anon-key"
```

### 6. Run the app

```bash
streamlit run streamlit_app.py
```

---

## Deployment

This app is deployed on **Streamlit Cloud**.

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo and set `streamlit_app.py` as the entry point
4. Add your Supabase secrets in the Streamlit Cloud dashboard under **Settings → Secrets**

---

## Design System

| Token | Value |
|-------|-------|
| Background | `#EDEADE` (warm cream) |
| Primary | `#1A3C23` (forest green) |
| Secondary | `#2A6B3A` |
| Headline font | Fraunces (serif) |
| Body font | Inter (sans-serif) |

---

## License

MIT
