import streamlit as st
from modules.skill_analyzer import get_all_roles, get_role_info, analyze_skills

# Group accent colors
GROUP_ACCENTS = {
    "Languages":      "#2D6A4F",
    "Data & ML":      "#1A3C23",
    "Cloud & DevOps": "#386641",
    "Frameworks":     "#4A7C59",
    "Databases":      "#52796F",
    "Tools & Viz":    "#40916C",
    "Soft Skills":    "#74C69D",
    "Role-Specific":  "#8B6914",
}

def hex_to_rgb(h):
    h = h.lstrip("#")
    return int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)

# Build per-group CSS for chips
group_css = ""
for gname, color in GROUP_ACCENTS.items():
    r,g,b = hex_to_rgb(color)
    slug  = gname.lower().replace(" ","_").replace("&","and")
    group_css += f"""
/* {gname} — unselected */
[data-group="{slug}"] button[kind="secondary"] {{
    background: rgba({r},{g},{b},0.09) !important;
    color: rgba({r},{g},{b},0.9) !important;
    border: 1px solid rgba({r},{g},{b},0.22) !important;
}}
/* {gname} — selected */
[data-group="{slug}"] button[kind="primary"] {{
    background: {color} !important;
    color: #EDEADE !important;
    border: 1px solid {color} !important;
    box-shadow: 0 2px 8px rgba({r},{g},{b},0.3) !important;
}}"""

st.markdown(f"""
<style>
@keyframes slideUp {{
    from {{ opacity:0; transform:translateY(14px); }}
    to   {{ opacity:1; transform:translateY(0); }}
}}
.result-in {{ animation: slideUp 0.4s ease forwards; }}

/* ── All skill chip buttons ── */
div[data-testid="stHorizontalBlock"] button {{
    border-radius: 100px !important;
    font-size: 0.74rem !important;
    padding: 0.28rem 0.4rem !important;
    height: 30px !important;
    min-height: 30px !important;
    max-height: 30px !important;
    line-height: 1 !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    text-transform: none !important;
    font-weight: 400 !important;
    letter-spacing: 0 !important;
    width: 100% !important;
    transition: all 0.12s ease !important;
}}

{group_css}
</style>
""", unsafe_allow_html=True)

# ── SESSION ───────────────────────────────────────────
for k, v in [("selected_tags",[]),("last_role",None),("analysis_result",None)]:
    if k not in st.session_state: st.session_state[k] = v

if st.session_state.get("prefilled_skills"):
    for s in st.session_state.prefilled_skills:
        if s not in st.session_state.selected_tags:
            st.session_state.selected_tags.append(s)
    st.session_state.prefilled_skills = []

roles       = get_all_roles()
prefill     = st.session_state.pop("prefill_role", None)
default_idx = roles.index(prefill) if prefill and prefill in roles else 0

SKILL_GROUPS = {
    "Languages":      ["Python","JavaScript","TypeScript","R","C","C#","Swift","Kotlin","HTML","CSS"],
    "Data & ML":      ["SQL","Machine Learning","Deep Learning","Statistics","NLP","PyTorch","TensorFlow","OpenCV","Spark","Airflow"],
    "Cloud & DevOps": ["AWS","Azure","GCP","Docker","Kubernetes","Terraform","Linux","Git"],
    "Frameworks":     ["React","Node.js","Flask","FastAPI","APIs"],
    "Databases":      ["MongoDB","PostgreSQL","Redis","Kafka"],
    "Tools & Viz":    ["Excel","Tableau","Power BI","Figma"],
    "Soft Skills":    ["Agile","Scrum","Communication"],
}
all_categorised = [s for g in SKILL_GROUPS.values() for s in g]

# ══════════════════════════════════════════════════════
# HEADER + ROLE PICKER
# ══════════════════════════════════════════════════════
h_l, h_r = st.columns([1.6, 2.4], gap="large")
with h_l:
    st.markdown("""
    <div style="margin-bottom:1.2rem;">
        <div style="font-size:0.6rem;letter-spacing:4px;text-transform:uppercase;
                    color:rgba(26,60,35,0.28);font-family:Inter,sans-serif;margin-bottom:0.5rem;">
            Skill Analysis
        </div>
        <div style="font-family:'Fraunces',serif;font-size:2.4rem;font-weight:300;
                    color:#1A3C23;line-height:1.1;letter-spacing:-0.5px;">
            Build your<br><em style="font-weight:700;">skill profile.</em>
        </div>
    </div>
    <div style="display:flex;flex-direction:column;gap:0.55rem;margin-bottom:1rem;">
        <div style="display:flex;align-items:center;gap:0.7rem;">
            <div style="width:22px;height:22px;border-radius:50%;background:#1A3C23;flex-shrink:0;
                        display:flex;align-items:center;justify-content:center;">
                <span style="font-size:0.6rem;color:#EDEADE;font-weight:700;font-family:Inter,sans-serif;">1</span>
            </div>
            <span style="font-size:0.78rem;color:#1A3C23;font-family:Inter,sans-serif;font-weight:500;">Choose your target role below</span>
        </div>
        <div style="display:flex;align-items:center;gap:0.7rem;">
            <div style="width:22px;height:22px;border-radius:50%;background:rgba(26,60,35,0.1);flex-shrink:0;
                        display:flex;align-items:center;justify-content:center;">
                <span style="font-size:0.6rem;color:rgba(26,60,35,0.5);font-weight:700;font-family:Inter,sans-serif;">2</span>
            </div>
            <span style="font-size:0.78rem;color:rgba(26,60,35,0.45);font-family:Inter,sans-serif;">Tap every skill you know in the list</span>
        </div>
        <div style="display:flex;align-items:center;gap:0.7rem;">
            <div style="width:22px;height:22px;border-radius:50%;background:rgba(26,60,35,0.1);flex-shrink:0;
                        display:flex;align-items:center;justify-content:center;">
                <span style="font-size:0.6rem;color:rgba(26,60,35,0.5);font-weight:700;font-family:Inter,sans-serif;">3</span>
            </div>
            <span style="font-size:0.78rem;color:rgba(26,60,35,0.45);font-family:Inter,sans-serif;">Hit Run Analysis → to see your score</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    selected_role = st.selectbox("", roles, index=default_idx,
                                  key="role_select", label_visibility="collapsed")

if selected_role != st.session_state.last_role:
    st.session_state.selected_tags   = []
    st.session_state.last_role       = selected_role
    st.session_state.analysis_result = None

role_info       = get_role_info(selected_role)
required_skills = role_info["required_skills"]
diff            = role_info["difficulty"]
diff_color      = "#2A6B3A" if diff=="Beginner" else "#8B6914" if diff=="Intermediate" else "#8B2020"
n_req           = len(required_skills)
n_sel_req       = len([s for s in st.session_state.selected_tags if s in required_skills])
n_total         = len(st.session_state.selected_tags)

with h_r:
    st.markdown(f"""
    <div style="margin-top:2.8rem;display:flex;gap:0;border:1px solid rgba(26,60,35,0.1);
                border-radius:10px;overflow:hidden;background:rgba(255,255,255,0.45);">
        <div style="flex:1.4;padding:0.9rem 1.2rem;border-right:1px solid rgba(26,60,35,0.08);">
            <div style="font-size:0.55rem;letter-spacing:1.8px;text-transform:uppercase;
                        color:rgba(26,60,35,0.3);font-family:Inter,sans-serif;margin-bottom:0.25rem;">Avg Salary</div>
            <div style="font-family:'Fraunces',serif;font-weight:600;color:#1A3C23;font-size:1rem;">{role_info["salary"]}</div>
        </div>
        <div style="flex:1;padding:0.9rem 1.2rem;border-right:1px solid rgba(26,60,35,0.08);">
            <div style="font-size:0.55rem;letter-spacing:1.8px;text-transform:uppercase;
                        color:rgba(26,60,35,0.3);font-family:Inter,sans-serif;margin-bottom:0.25rem;">Difficulty</div>
            <div style="font-family:'Fraunces',serif;font-weight:700;color:{diff_color};font-size:1rem;">{diff}</div>
        </div>
        <div style="flex:1;padding:0.9rem 1.2rem;border-right:1px solid rgba(26,60,35,0.08);">
            <div style="font-size:0.55rem;letter-spacing:1.8px;text-transform:uppercase;
                        color:rgba(26,60,35,0.3);font-family:Inter,sans-serif;margin-bottom:0.25rem;">Required</div>
            <div style="font-family:'Fraunces',serif;font-weight:700;color:#1A3C23;font-size:1rem;">{n_req} skills</div>
        </div>
        <div style="flex:0.8;padding:0.9rem 1.2rem;">
            <div style="font-size:0.55rem;letter-spacing:1.8px;text-transform:uppercase;
                        color:rgba(26,60,35,0.3);font-family:Inter,sans-serif;margin-bottom:0.25rem;">Selected</div>
            <div style="font-family:'Fraunces',serif;font-weight:700;color:#1A3C23;font-size:1rem;">{n_total}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# TAG CLOUD — one group per row
# ══════════════════════════════════════════════════════
st.markdown("""
<div style="height:1px;background:rgba(26,60,35,0.07);margin:1.8rem 0 1.2rem;"></div>
<div style="display:flex;align-items:center;gap:0.7rem;margin-bottom:1.2rem;">
    <div style="width:22px;height:22px;border-radius:50%;background:#1A3C23;flex-shrink:0;
                display:flex;align-items:center;justify-content:center;">
        <span style="font-size:0.6rem;color:#EDEADE;font-weight:700;font-family:Inter,sans-serif;">2</span>
    </div>
    <span style="font-size:0.78rem;color:#1A3C23;font-family:Inter,sans-serif;font-weight:500;">Tap every skill you know — selected chips turn green</span>
</div>
""", unsafe_allow_html=True)

ungrouped = [s for s in required_skills if s not in all_categorised]
groups_list = list(SKILL_GROUPS.items())
if ungrouped:
    groups_list.append(("Role-Specific", ungrouped))

for gname, gskills in groups_list:
    color    = GROUP_ACCENTS.get(gname, "#1A3C23")
    r,g,b    = hex_to_rgb(color)
    slug     = gname.lower().replace(" ","_").replace("&","and")
    sel_cnt  = len([s for s in gskills if s in st.session_state.selected_tags])

    # Group label row
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:0.65rem;margin:1rem 0 0.45rem;">
        <span style="width:10px;height:10px;border-radius:50%;background:{color};
                     flex-shrink:0;box-shadow:0 0 0 2px rgba(255,255,255,0.8);"></span>
        <span style="font-size:0.62rem;letter-spacing:2px;text-transform:uppercase;
                     color:rgba({r},{g},{b},0.75);font-family:Inter,sans-serif;
                     font-weight:600;">{gname}</span>
        <span style="font-size:0.6rem;color:rgba({r},{g},{b},0.45);
                     font-family:'Fraunces',serif;font-weight:600;">{sel_cnt}/{len(gskills)}</span>
        <div style="flex:1;height:1px;background:rgba({r},{g},{b},0.12);"></div>
    </div>
    """, unsafe_allow_html=True)

    # Chips — as many per row as fit, using st.columns dynamically
    # Wrap into rows of max 10
    # Render chips in rows of 10, padded to full width
    MAX_PER_ROW = 10
    rows = [gskills[i:i+MAX_PER_ROW] for i in range(0, len(gskills), MAX_PER_ROW)]
    for row in rows:
        # Always use MAX_PER_ROW columns so chips stay same size
        cols = st.columns(MAX_PER_ROW, gap="small")
        for i, col in enumerate(cols):
            with col:
                if i < len(row):
                    skill  = row[i]
                    is_sel = skill in st.session_state.selected_tags
                    label  = ("✓ " if is_sel else "") + skill
                    if st.button(label, key=f"sk_{skill}",
                                 use_container_width=True,
                                 type="primary" if is_sel else "secondary"):
                        if skill in st.session_state.selected_tags:
                            st.session_state.selected_tags.remove(skill)
                        else:
                            st.session_state.selected_tags.append(skill)
                        st.session_state.analysis_result = None
                        st.rerun()
                else:
                    st.empty()

    st.markdown('<div style="height:0.2rem;"></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# CUSTOM ADD + RUN
# ══════════════════════════════════════════════════════
st.markdown("""
<div style="height:1px;background:rgba(26,60,35,0.07);margin:1.2rem 0 0.8rem;"></div>
<div style="display:flex;align-items:center;gap:0.7rem;margin-bottom:0.9rem;">
    <div style="width:22px;height:22px;border-radius:50%;background:#1A3C23;flex-shrink:0;
                display:flex;align-items:center;justify-content:center;">
        <span style="font-size:0.6rem;color:#EDEADE;font-weight:700;font-family:Inter,sans-serif;">3</span>
    </div>
    <span style="font-size:0.78rem;color:#1A3C23;font-family:Inter,sans-serif;font-weight:500;">Add any missing skills manually, then run your analysis</span>
</div>
""", unsafe_allow_html=True)

if st.session_state.selected_tags:
    chips = "".join([
        f'<span style="background:#1A3C23;color:#EDEADE;padding:0.25rem 0.75rem;'
        f'border-radius:100px;font-size:0.75rem;font-family:Inter,sans-serif;'
        f'display:inline-block;margin:0.12rem;">{s}</span>'
        for s in st.session_state.selected_tags
    ])
    st.markdown(f"""
    <div style="background:rgba(26,60,35,0.03);border:1px solid rgba(26,60,35,0.08);
                border-radius:8px;padding:0.85rem 1.1rem;margin-bottom:1rem;">
        <div style="font-size:0.55rem;letter-spacing:2px;text-transform:uppercase;
                    color:rgba(26,60,35,0.3);font-family:Inter,sans-serif;
                    margin-bottom:0.5rem;">{n_total} skills selected</div>
        <div style="line-height:2.3;">{chips}</div>
    </div>
    """, unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns([2.8, 0.6, 1.2, 0.7], gap="small")
with c1:
    manual = st.text_input("", placeholder="Add a custom skill not listed...",
                           label_visibility="collapsed", key="manual_skill")
with c2:
    if st.button("+ Add", use_container_width=True):
        if manual:
            for s in [x.strip() for x in manual.split(",") if x.strip()]:
                if s not in st.session_state.selected_tags:
                    st.session_state.selected_tags.append(s)
            st.session_state.analysis_result = None
            st.rerun()
with c3:
    run_clicked = st.button("Run Analysis →", type="primary",
                             use_container_width=True, disabled=n_total == 0)
with c4:
    if st.button("Clear all", use_container_width=True):
        st.session_state.selected_tags   = []
        st.session_state.analysis_result = None
        st.rerun()

if run_clicked and st.session_state.selected_tags:
    with st.spinner("Analyzing..."):
        result = analyze_skills(st.session_state.selected_tags, selected_role)
    st.session_state.analysis_result = result
    st.session_state.result          = result
    st.session_state.role            = selected_role
    st.session_state.user_skills     = st.session_state.selected_tags.copy()
    st.rerun()

# ══════════════════════════════════════════════════════
# RESULTS
# ══════════════════════════════════════════════════════
result = st.session_state.analysis_result
if result:
    score     = result["score"]
    s_col     = "#2A6B3A" if score>=70 else "#8B6914" if score>=40 else "#8B2020"
    s_bg      = "rgba(42,107,58,0.04)" if score>=70 else "rgba(139,105,20,0.04)" if score>=40 else "rgba(139,32,32,0.04)"
    s_bdr     = "rgba(42,107,58,0.15)" if score>=70 else "rgba(139,105,20,0.15)" if score>=40 else "rgba(139,32,32,0.15)"
    readiness = result["readiness"]

    st.markdown(f"""
    <div style="height:1px;background:linear-gradient(90deg,{s_col}44,transparent);
                margin:0.5rem 0 2rem;"></div>
    """, unsafe_allow_html=True)

    rl, rr = st.columns([1, 1.7], gap="large")
    with rl:
        st.markdown(f"""
        <div class="result-in">
            <div style="font-size:0.57rem;letter-spacing:3px;text-transform:uppercase;
                        color:rgba(26,60,35,0.28);font-family:Inter,sans-serif;margin-bottom:0.4rem;">
                Your Score
            </div>
            <div style="font-family:'Fraunces',serif;font-size:6.5rem;font-weight:700;
                        color:{s_col};line-height:0.85;letter-spacing:-4px;">
                {score}<span style="font-size:2rem;opacity:0.35;font-weight:300;">%</span>
            </div>
            <div style="display:inline-block;background:{s_bg};border:1px solid {s_bdr};
                        border-radius:100px;padding:0.28rem 0.9rem;margin:0.6rem 0 1rem;">
                <span style="font-size:0.73rem;font-weight:600;color:{s_col};
                             font-family:Inter,sans-serif;">{readiness}</span>
            </div>
            <div style="height:3px;background:rgba(26,60,35,0.07);border-radius:2px;
                        overflow:hidden;margin-bottom:1.4rem;">
                <div style="height:100%;width:{score}%;background:{s_col};border-radius:2px;"></div>
            </div>
            <div style="display:flex;gap:2rem;margin-bottom:1.8rem;">
                <div>
                    <div style="font-family:'Fraunces',serif;font-size:1.5rem;
                                font-weight:700;color:#2A6B3A;">{len(result['matched'])}</div>
                    <div style="font-size:0.57rem;letter-spacing:1.5px;text-transform:uppercase;
                                color:rgba(26,60,35,0.32);font-family:Inter,sans-serif;">Matched</div>
                </div>
                <div>
                    <div style="font-family:'Fraunces',serif;font-size:1.5rem;
                                font-weight:700;color:#8B2020;">{len(result['missing'])}</div>
                    <div style="font-size:0.57rem;letter-spacing:1.5px;text-transform:uppercase;
                                color:rgba(26,60,35,0.32);font-family:Inter,sans-serif;">Missing</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View Dashboard →", type="primary", use_container_width=True, key="go_dash"):
            st.session_state.current_page = "Dashboard"
            st.rerun()
        st.markdown('<div style="height:0.4rem;"></div>', unsafe_allow_html=True)
        if st.button("Learning Roadmap →", use_container_width=True, key="go_road"):
            st.session_state.current_page = "Roadmap"
            st.rerun()

    with rr:
        m_chips = "".join([
            f'<span style="background:rgba(42,107,58,0.1);color:#2A6B3A;padding:0.22rem 0.75rem;'
            f'border-radius:100px;font-size:0.71rem;font-family:Inter,sans-serif;'
            f'display:inline-block;margin:0.13rem;">{s}</span>'
            for s in result["matched"]
        ]) or '<span style="font-size:0.75rem;color:rgba(26,60,35,0.25);font-style:italic;">None matched</span>'

        x_chips = "".join([
            f'<span style="background:rgba(139,32,32,0.08);color:#8B2020;padding:0.22rem 0.75rem;'
            f'border-radius:100px;font-size:0.71rem;font-family:Inter,sans-serif;'
            f'display:inline-block;margin:0.13rem;">{s}</span>'
            for s in result["missing"]
        ]) or '<span style="font-size:0.75rem;color:rgba(26,60,35,0.25);font-style:italic;">All matched 🎉</span>'

        st.markdown(f"""
        <div class="result-in" style="background:rgba(255,255,255,0.5);
                    border:1px solid rgba(26,60,35,0.1);border-radius:10px;overflow:hidden;">
            <div style="padding:1.1rem 1.4rem;border-bottom:1px solid rgba(26,60,35,0.07);
                        background:rgba(42,107,58,0.03);">
                <div style="font-size:0.57rem;letter-spacing:2px;text-transform:uppercase;
                            color:#2A6B3A;font-family:Inter,sans-serif;margin-bottom:0.55rem;">
                    ✓ Skills you have
                </div>
                <div style="line-height:2.3;">{m_chips}</div>
            </div>
            <div style="padding:1.1rem 1.4rem;">
                <div style="font-size:0.57rem;letter-spacing:2px;text-transform:uppercase;
                            color:#8B2020;font-family:Inter,sans-serif;margin-bottom:0.55rem;">
                    ✗ Skills to learn
                </div>
                <div style="line-height:2.3;">{x_chips}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        try:
            from modules.role_recommender import get_similar_roles
            recs = get_similar_roles(st.session_state.user_skills, selected_role, top_n=3)
            if recs:
                st.markdown("""
                <div style="margin-top:1.1rem;font-size:0.57rem;letter-spacing:2.5px;
                            text-transform:uppercase;color:rgba(26,60,35,0.28);
                            font-family:Inter,sans-serif;margin-bottom:0.6rem;">
                    Similar roles you'd also fit
                </div>
                """, unsafe_allow_html=True)
                for rec in recs:
                    rc = "#2A6B3A" if rec['match_pct']>=70 else "#8B6914" if rec['match_pct']>=40 else "#8B2020"
                    st.markdown(f"""
                    <div style="display:flex;justify-content:space-between;align-items:center;
                                padding:0.65rem 1rem;margin-bottom:0.35rem;
                                background:rgba(255,255,255,0.45);border:1px solid rgba(26,60,35,0.09);
                                border-radius:6px;">
                        <div>
                            <div style="font-family:'Fraunces',serif;font-weight:600;
                                        font-size:0.88rem;color:#1A3C23;">{rec['role']}</div>
                            <div style="font-size:0.67rem;color:rgba(26,60,35,0.38);
                                        font-family:Inter,sans-serif;margin-top:0.1rem;">{rec['readiness']}</div>
                        </div>
                        <div style="font-family:'Fraunces',serif;font-weight:700;
                                    font-size:1.2rem;color:{rc};">{rec['match_pct']}%</div>
                    </div>
                    """, unsafe_allow_html=True)
        except Exception:
            pass