"""
fetch_onet_data.py
==================
Downloads real skill data from O*NET (US Dept of Labor) and reformats it
into SkillLens's job_skills.csv format.

Run once from your project root:
    cd ~/Desktop/skilllens
    source venv/bin/activate
    pip install requests pandas --break-system-packages
    python fetch_onet_data.py

Output: data/job_skills.csv  (replaces your existing file)
Source: O*NET 30.2 Database — US Department of Labor (CC BY 4.0)
"""

import requests
import pandas as pd
import zipfile
import io
import os

# ── O*NET direct download URL (no login needed) ───────
ONET_ZIP_URL = "https://www.onetcenter.org/dl_files/database/db_30_2_text.zip"

# ── Tech roles we care about → O*NET-SOC codes ────────
# Source: https://www.onetonline.org/
ROLE_MAP = {
    "Data Scientist":            ["15-2051.00", "15-2051.01", "15-2051.02"],
    "Data Analyst":              ["15-2041.00", "13-2098.01"],
    "Data Engineer":             ["15-1243.00", "15-1299.08"],
    "Machine Learning Engineer": ["15-2051.02", "15-1299.09"],
    "AI Engineer":               ["15-1299.09", "15-2051.02"],
    "Backend Developer":         ["15-1252.00", "15-1253.00"],
    "Frontend Developer":        ["15-1254.00", "15-1255.00"],
    "Full Stack Developer":      ["15-1256.00", "15-1254.00"],
    "DevOps Engineer":           ["15-1244.00", "15-1299.07"],
    "Cloud Engineer":            ["15-1241.00", "15-1244.00"],
    "Cybersecurity Analyst":     ["15-1212.00", "15-1299.05"],
    "Software Engineer":         ["15-1252.00", "15-1253.00"],
    "Mobile Developer":          ["15-1257.00", "15-1254.00"],
    "Database Administrator":    ["15-1242.00"],
    "Network Engineer":          ["15-1211.00", "15-1241.00"],
    "Site Reliability Engineer":  ["15-1244.00", "15-1299.07"],
    "Product Manager":           ["11-2021.00", "15-1299.01"],
    "Business Analyst":          ["13-1111.00", "15-1299.02"],
    "UX Designer":               ["15-1255.00", "27-1021.00"],
    "NLP Engineer":              ["15-2051.02", "15-1299.09"],
    "Computer Vision Engineer":  ["15-2051.02", "15-1299.09"],
    "Embedded Systems Engineer": ["17-2061.00", "15-1299.03"],
    "Data Architect":            ["15-1243.00", "15-1299.08"],
    "Blockchain Developer":      ["15-1299.06", "15-1252.00"],
    "Game Developer":            ["15-1251.00", "15-1252.00"],
    "IT Support Specialist":     ["15-1231.00", "15-1232.00"],
    "Technical Writer":          ["27-3042.00"],
    "Scrum Master":              ["15-1299.01", "11-9199.09"],
    "Quantitative Analyst":      ["15-2031.00", "13-2099.01"],
    "Prompt Engineer":           ["15-1299.09", "15-2051.02"],
}

# ── Salary ranges (from BLS Occupational Outlook Handbook) ────
SALARY_MAP = {
    "Data Scientist":            "₹80L–₹134L",
    "Data Analyst":              "₹50L–₹92L",
    "Data Engineer":             "₹84L–₹134L",
    "Machine Learning Engineer": "₹101L–₹151L",
    "AI Engineer":               "₹101L–₹160L",
    "Backend Developer":         "₹80L–₹130L",
    "Frontend Developer":        "₹71L–₹122L",
    "Full Stack Developer":      "₹76L–₹130L",
    "DevOps Engineer":           "₹84L–₹139L",
    "Cloud Engineer":            "₹88L–₹139L",
    "Cybersecurity Analyst":     "₹76L–₹126L",
    "Software Engineer":         "₹84L–₹139L",
    "Mobile Developer":          "₹80L–₹130L",
    "Database Administrator":    "₹67L–₹109L",
    "Network Engineer":          "₹63L–₹109L",
    "Site Reliability Engineer":  "₹97L–₹147L",
    "Product Manager":           "₹80L–₹139L",
    "Business Analyst":          "₹55L–₹92L",
    "UX Designer":               "₹63L–₹113L",
    "NLP Engineer":              "₹97L–₹147L",
    "Computer Vision Engineer":  "₹97L–₹147L",
    "Embedded Systems Engineer": "₹71L–₹118L",
    "Data Architect":            "₹92L–₹147L",
    "Blockchain Developer":      "₹84L–₹143L",
    "Game Developer":            "₹63L–₹113L",
    "IT Support Specialist":     "₹34L–₹63L",
    "Technical Writer":          "₹46L–₹80L",
    "Scrum Master":              "₹71L–₹118L",
    "Quantitative Analyst":      "₹92L–₹168L",
    "Prompt Engineer":           "₹76L–₹134L",
}

# ── Difficulty (based on O*NET Job Zone 1-5) ──────────
DIFFICULTY_MAP = {
    "Data Scientist":            "Advanced",
    "Data Analyst":              "Intermediate",
    "Data Engineer":             "Advanced",
    "Machine Learning Engineer": "Advanced",
    "AI Engineer":               "Advanced",
    "Backend Developer":         "Intermediate",
    "Frontend Developer":        "Intermediate",
    "Full Stack Developer":      "Advanced",
    "DevOps Engineer":           "Advanced",
    "Cloud Engineer":            "Advanced",
    "Cybersecurity Analyst":     "Advanced",
    "Software Engineer":         "Intermediate",
    "Mobile Developer":          "Intermediate",
    "Database Administrator":    "Intermediate",
    "Network Engineer":          "Intermediate",
    "Site Reliability Engineer":  "Advanced",
    "Product Manager":           "Intermediate",
    "Business Analyst":          "Beginner",
    "UX Designer":               "Intermediate",
    "NLP Engineer":              "Advanced",
    "Computer Vision Engineer":  "Advanced",
    "Embedded Systems Engineer": "Advanced",
    "Data Architect":            "Advanced",
    "Blockchain Developer":      "Advanced",
    "Game Developer":            "Intermediate",
    "IT Support Specialist":     "Beginner",
    "Technical Writer":          "Beginner",
    "Scrum Master":              "Intermediate",
    "Quantitative Analyst":      "Advanced",
    "Prompt Engineer":           "Intermediate",
}

# ── Skill name cleanup ────────────────────────────────
# Maps raw O*NET tech names → clean skill names for SkillLens
SKILL_CLEANUP = {
    "Python": "Python",
    "R": "R",
    "SQL": "SQL",
    "Structured query language SQL": "SQL",
    "Java": "Java",
    "JavaScript": "JavaScript",
    "C++": "C++",
    "C#": "C#",
    "TypeScript": "TypeScript",
    "Scala": "Scala",
    "Go": "Go",
    "Swift": "Swift",
    "Kotlin": "Kotlin",
    "Ruby": "Ruby",
    "PHP": "PHP",
    "Rust": "Rust",
    "MATLAB": "MATLAB",
    "TensorFlow": "TensorFlow",
    "PyTorch": "PyTorch",
    "scikit-learn": "Scikit-learn",
    "Apache Spark": "Spark",
    "Apache Hadoop": "Hadoop",
    "Apache Kafka": "Kafka",
    "Apache Airflow": "Airflow",
    "Docker": "Docker",
    "Kubernetes": "Kubernetes",
    "Terraform": "Terraform",
    "Amazon Web Services AWS": "AWS",
    "Microsoft Azure": "Azure",
    "Google Cloud": "GCP",
    "Git": "Git",
    "GitHub": "GitHub",
    "Linux": "Linux",
    "Tableau": "Tableau",
    "Microsoft Power BI": "Power BI",
    "Microsoft Excel": "Excel",
    "Microsoft SQL Server": "SQL Server",
    "PostgreSQL": "PostgreSQL",
    "MySQL": "MySQL",
    "MongoDB": "MongoDB",
    "Redis": "Redis",
    "Elasticsearch": "Elasticsearch",
    "React": "React",
    "Angular": "Angular",
    "Node.js": "Node.js",
    "Flask": "Flask",
    "Django": "Django",
    "FastAPI": "FastAPI",
    "Figma": "Figma",
    "Adobe XD": "Adobe XD",
    "Jira": "Jira",
    "Confluence": "Confluence",
    "Ansible": "Ansible",
    "Jenkins": "Jenkins",
}

def clean_skill_name(raw_name):
    """Clean up raw O*NET tech names to simple skill labels."""
    for raw, clean in SKILL_CLEANUP.items():
        if raw.lower() in raw_name.lower():
            return clean
    # Generic cleanup: take first meaningful word(s), max 25 chars
    name = raw_name.split("(")[0].strip()  # Remove parenthetical
    name = name.split("—")[0].strip()      # Remove em-dash descriptions
    if len(name) > 30:
        # Shorten long names
        words = name.split()
        name = " ".join(words[:3])
    return name.title() if name == name.upper() else name


def download_onet():
    print("📥 Downloading O*NET 30.2 database (~15MB)...")
    resp = requests.get(ONET_ZIP_URL, timeout=60)
    resp.raise_for_status()
    print("✅ Downloaded!")
    return zipfile.ZipFile(io.BytesIO(resp.content))


def load_tech_skills(zf):
    """Load Technology_Skills.txt from the O*NET zip."""
    # Try both possible filenames
    candidates = [n for n in zf.namelist() if "Technology Skills" in n or "Technology_Skills" in n]
    if not candidates:
        raise FileNotFoundError(f"Technology Skills file not found in zip. Files: {zf.namelist()[:20]}")

    fname = candidates[0]
    print(f"📂 Reading: {fname}")
    with zf.open(fname) as f:
        df = pd.read_csv(f, sep="\t", dtype=str)

    print(f"   Columns: {list(df.columns)}")
    print(f"   Rows: {len(df)}")
    return df


def load_occupation_data(zf):
    """Load Occupation Data.txt for titles."""
    candidates = [n for n in zf.namelist() if "Occupation Data" in n]
    if not candidates:
        return {}

    fname = candidates[0]
    with zf.open(fname) as f:
        df = pd.read_csv(f, sep="\t", dtype=str)

    return dict(zip(df["O*NET-SOC Code"], df["Title"]))


def build_job_skills(tech_df, occupation_titles):
    """Build the SkillLens job_skills.csv from O*NET data."""

    # O*NET 30.2 exact column names:
    # 'O*NET-SOC Code', 'Example', 'Commodity Code', 'Commodity Title', 'Hot Technology', 'In Demand'
    exact_map = {
        "O*NET-SOC Code": "soc_code",
        "Example":        "tech_name",
        "Hot Technology": "hot_tech",
        "In Demand":      "in_demand",
    }
    tech_df = tech_df.rename(columns=exact_map)

    # Keep only needed columns — drop Commodity Code/Title to avoid duplicates
    keep = [c for c in ["soc_code", "tech_name", "hot_tech", "in_demand"] if c in tech_df.columns]
    tech_df = tech_df[keep].copy()

    print(f"   Normalized columns: {list(tech_df.columns)}")

    rows = []
    for role_name, soc_codes in ROLE_MAP.items():
        # Get all tech skills for this role's SOC codes
        mask     = tech_df["soc_code"].isin(soc_codes)
        role_df  = tech_df[mask].copy()

        if role_df.empty:
            print(f"   ⚠️  No O*NET data found for: {role_name} ({soc_codes})")
            continue

        # Clean skill names and deduplicate
        skills = role_df["tech_name"].dropna().tolist()
        skills = [clean_skill_name(s) for s in skills]
        skills = list(dict.fromkeys(skills))  # deduplicate preserving order

        # Prefer hot/in-demand skills first if column exists
        if "hot_tech" in tech_df.columns:
            hot_mask    = mask & (tech_df["hot_tech"].str.upper() == "Y")
            hot_skills  = tech_df[hot_mask]["tech_name"].dropna().tolist()
            hot_clean   = [clean_skill_name(s) for s in hot_skills]
            # Put hot skills first
            other       = [s for s in skills if s not in hot_clean]
            skills      = list(dict.fromkeys(hot_clean + other))

        # Cap at 18 skills per role for usability
        skills = skills[:18]

        if len(skills) < 3:
            print(f"   ⚠️  Too few skills for: {role_name} — skipping")
            continue

        rows.append({
            "role":             role_name,
            "required_skills":  ", ".join(skills),
            "salary":           SALARY_MAP.get(role_name, "N/A"),
            "difficulty":       DIFFICULTY_MAP.get(role_name, "Intermediate"),
        })

        print(f"   ✅ {role_name}: {len(skills)} skills")

    return pd.DataFrame(rows)


def main():
    os.makedirs("data", exist_ok=True)

    try:
        zf = download_onet()
    except Exception as e:
        print(f"❌ Download failed: {e}")
        print("   Check your internet connection and try again.")
        return

    try:
        tech_df = load_tech_skills(zf)
    except Exception as e:
        print(f"❌ Failed to load skills: {e}")
        return

    occupation_titles = load_occupation_data(zf)
    print(f"\n🔧 Building job_skills.csv for {len(ROLE_MAP)} roles...")
    result_df = build_job_skills(tech_df, occupation_titles)

    if result_df.empty:
        print("❌ No data was built. The O*NET file structure may have changed.")
        return

    out_path = "data/job_skills.csv"
    result_df.to_csv(out_path, index=False)

    print(f"\n✅ Done! Saved {len(result_df)} roles to {out_path}")
    print(f"\nPreview:")
    print(result_df[["role", "difficulty", "salary"]].to_string(index=False))
    print(f"\n📌 Attribution required: Data sourced from O*NET 30.2 Database,")
    print(f"   US Department of Labor — https://www.onetcenter.org/database.html")
    print(f"   Licensed under CC BY 4.0")


if __name__ == "__main__":
    main()