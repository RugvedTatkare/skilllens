import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
from modules.demand_score import get_demand_score
from modules.role_recommender import get_similar_roles, get_skill_clusters

# ── GUARD ─────────────────────────────────────────────
if "result" not in st.session_state or not st.session_state.result:
    st.markdown("""
    <div style="text-align:center; padding:5rem 2rem;">
        <div style="font-family:'Fraunces',serif; font-size:2rem; font-weight:300;
                    color:rgba(26,60,35,0.4); margin-bottom:1rem;">No analysis yet</div>
        <div style="font-size:0.85rem; color:rgba(26,60,35,0.35); font-family:'Inter',sans-serif;
                    margin-bottom:2rem;">Run an analysis first to see your dashboard.</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Go to Analyze →", type="primary"):
        st.session_state.current_page = "Analyze"
        st.rerun()
    st.stop()

result      = st.session_state.result
role        = st.session_state.get("role", "Unknown Role")
user_skills = st.session_state.get("user_skills", [])
score       = result["score"]
matched     = result["matched"]
missing     = result["missing"]
readiness   = result["readiness"]
salary      = result.get("salary", "N/A")
difficulty  = result.get("difficulty", "N/A")
score_color = "#2A6B3A" if score >= 70 else "#7A5C10" if score >= 40 else "#7A2A2A"

# ── REPORT BANNER ─────────────────────────────────────
loaded_report = st.session_state.pop("loaded_from_report", None)
if loaded_report:
    banner = (
        '<div style="background:rgba(26,60,35,0.06); border:1px solid rgba(26,60,35,0.15); '
        'border-radius:3px; padding:0.7rem 1.2rem; margin-bottom:1.5rem; '
        'display:flex; align-items:center; gap:0.8rem;">'
        ''
        '<span style="font-size:0.78rem; font-family:Inter,sans-serif; color:rgba(26,60,35,0.6);">Viewing saved report: </span>'
        '<span style="font-family:Fraunces,serif; font-weight:600; color:#1A3C23; font-size:0.85rem;">'
        + loaded_report +
        '</span></div>'
    )
    st.markdown(banner, unsafe_allow_html=True)

# ── HEADER ────────────────────────────────────────────
st.markdown(f"""
<div style="margin-bottom:2rem;">
    <div style="font-size:0.68rem; font-weight:500; letter-spacing:3px; text-transform:uppercase;
                color:rgba(26,60,35,0.35); margin-bottom:0.6rem; font-family:'Inter',sans-serif;">Dashboard</div>
    <div style="font-family:'Fraunces',serif; font-size:2.8rem; font-weight:300; color:#1A3C23;
                letter-spacing:-0.5px; line-height:1.1;">
        Your results for <em style="font-weight:600;">{role}</em>
    </div>
</div>
<div style="height:1px; background:rgba(26,60,35,0.08); margin-bottom:2.5rem;"></div>
""", unsafe_allow_html=True)

# ── SCORE HERO ROW ────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns([1.8, 1, 1, 1, 1], gap="medium")
with c1:
    st.markdown(f"""
    <div style="background:rgba(255,255,255,0.45); border:1px solid rgba(26,60,35,0.1);
                border-radius:3px; padding:1.8rem 2rem;">
        <div style="font-size:0.6rem; letter-spacing:2px; text-transform:uppercase;
                    color:rgba(26,60,35,0.35); font-family:Inter,sans-serif; margin-bottom:0.5rem;">Match Score</div>
        <div style="font-family:'Fraunces',serif; font-size:4rem; font-weight:700;
                    color:{score_color}; line-height:1; letter-spacing:-2px;">{score}%</div>
        <div style="background:rgba(26,60,35,0.08); border-radius:2px; height:4px; margin-top:1rem;">
            <div style="background:{score_color}; width:{score}%; height:4px; border-radius:2px;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

for col, val, lbl in [(c2, len(matched), "Matched"), (c3, len(missing), "Missing"),
                      (c4, salary, "Avg Salary"), (c5, readiness, "Readiness")]:
    with col:
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.45); border:1px solid rgba(26,60,35,0.1);
                    border-radius:3px; padding:1.8rem 1.2rem; height:100%;">
            <div style="font-size:0.6rem; letter-spacing:2px; text-transform:uppercase;
                        color:rgba(26,60,35,0.35); font-family:Inter,sans-serif; margin-bottom:0.5rem;">{lbl}</div>
            <div style="font-family:'Fraunces',serif; font-size:1.8rem; font-weight:600;
                        color:#1A3C23; line-height:1;">{val}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<div style="height:1px; background:rgba(26,60,35,0.08); margin:2.5rem 0;"></div>', unsafe_allow_html=True)

# ── ML RECOMMENDATIONS (moved up — before charts) ─────
if user_skills:
    with st.spinner("Finding similar roles..."):
        recommendations = get_similar_roles(user_skills, role, top_n=3)
        clusters        = get_skill_clusters(user_skills)

    if recommendations:
        st.markdown("""
        <div style="margin-bottom:1.2rem;">
            <div style="font-size:0.65rem; letter-spacing:2px; text-transform:uppercase;
                        color:rgba(26,60,35,0.35); font-family:Inter,sans-serif; margin-bottom:0.3rem;">
                Powered by ML · Cosine Similarity
            </div>
            <div style="font-family:'Fraunces',serif; font-size:1.6rem; font-weight:600; color:#1A3C23;">
                You might also fit these roles
            </div>
            <div style="font-size:0.82rem; color:rgba(26,60,35,0.45); font-family:Inter,sans-serif; margin-top:0.3rem;">
                Based on your skill profile — ranked by similarity to your expertise.
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Build all card HTML as ONE string, rendered in ONE components.html call
        # This completely bypasses the Streamlit columns + unsafe_allow_html bug
        cards_html = """
        <link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,300;0,600;0,700;1,600&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
        <div style="display:grid; grid-template-columns: repeat(""" + str(len(recommendations)) + """, 1fr); gap:1rem; font-family:'Inter',sans-serif;">
        """

        for rec in recommendations:
            rec_role    = rec["role"]
            rec_match   = rec["match_pct"]
            rec_sim     = rec["similarity"]
            rec_salary  = rec["salary"]
            rec_diff    = rec["difficulty"]
            rec_read    = rec["readiness"]
            rec_missing = ", ".join(rec["missing"][:3]) + ("..." if len(rec["missing"]) > 3 else "") or "You have all key skills!"

            d_color = "#2A6B3A" if rec_diff == "Beginner" else "#7A5C10" if rec_diff == "Intermediate" else "#7A2A2A"
            d_bg    = "rgba(42,107,58,0.08)" if rec_diff == "Beginner" else "rgba(122,92,16,0.08)" if rec_diff == "Intermediate" else "rgba(122,42,42,0.08)"
            r_color = "#2A6B3A" if rec_read == "Ready" else "#7A5C10" if rec_read == "Almost Ready" else "#1A3C23" if rec_read == "Good Fit" else "rgba(26,60,35,0.5)"

            cards_html += """
            <div style="background:rgba(255,255,255,0.45); border:1px solid rgba(26,60,35,0.1); border-radius:3px; overflow:hidden;">
                <div style="padding:1.2rem 1.3rem 0.8rem;">
                    <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:0.9rem;">
                        <div style="font-family:'Fraunces',serif; font-weight:600; font-size:1rem; color:#1A3C23; line-height:1.3; flex:1; padding-right:0.5rem;">""" + rec_role + """</div>
                        <div style="background:""" + d_bg + """; color:""" + d_color + """; font-size:0.55rem; letter-spacing:1px; text-transform:uppercase; font-weight:600; padding:0.2rem 0.5rem; border-radius:2px; white-space:nowrap;">""" + rec_diff + """</div>
                    </div>
                    <div style="display:flex; gap:0.5rem;">
                        <div style="flex:1; background:rgba(26,60,35,0.04); border-radius:2px; padding:0.6rem; text-align:center;">
                            <div style="font-family:'Fraunces',serif; font-weight:700; color:#1A3C23; font-size:1.3rem; line-height:1;">""" + str(rec_match) + """%</div>
                            <div style="font-size:0.57rem; color:rgba(26,60,35,0.38); text-transform:uppercase; letter-spacing:1px; margin-top:0.2rem;">Match</div>
                        </div>
                        <div style="flex:1; background:rgba(26,60,35,0.04); border-radius:2px; padding:0.6rem; text-align:center;">
                            <div style="font-family:'Fraunces',serif; font-weight:700; color:#1A3C23; font-size:1.3rem; line-height:1;">""" + str(rec_sim) + """%</div>
                            <div style="font-size:0.57rem; color:rgba(26,60,35,0.38); text-transform:uppercase; letter-spacing:1px; margin-top:0.2rem;">Similarity</div>
                        </div>
                    </div>
                </div>
                <div style="border-top:1px solid rgba(26,60,35,0.07); padding:0.55rem 1.3rem;">
                    <div style="font-size:0.58rem; text-transform:uppercase; letter-spacing:1.5px; color:rgba(26,60,35,0.35); margin-bottom:0.2rem;">Readiness</div>
                    <div style="font-family:'Fraunces',serif; font-weight:600; color:""" + r_color + """; font-size:0.9rem;">""" + rec_read + """</div>
                </div>
                <div style="border-top:1px solid rgba(26,60,35,0.07); padding:0.55rem 1.3rem;">
                    <div style="font-size:0.58rem; text-transform:uppercase; letter-spacing:1.5px; color:rgba(26,60,35,0.35); margin-bottom:0.2rem;">Salary</div>
                    <div style="font-family:'Fraunces',serif; font-weight:600; color:#1A3C23; font-size:0.88rem;">""" + rec_salary + """</div>
                </div>
                <div style="border-top:1px solid rgba(26,60,35,0.07); padding:0.55rem 1.3rem 1rem;">
                    <div style="font-size:0.58rem; text-transform:uppercase; letter-spacing:1.5px; color:rgba(26,60,35,0.35); margin-bottom:0.2rem;">Top skills to learn</div>
                    <div style="font-size:0.75rem; color:rgba(26,60,35,0.55); line-height:1.5;">""" + rec_missing + """</div>
                </div>
            </div>
            """

        cards_html += "</div>"
        components.html(cards_html, height=320, scrolling=False)

        # Analyze buttons below cards using real Streamlit columns
        btn_cols = st.columns(len(recommendations), gap="medium")
        for i, rec in enumerate(recommendations):
            with btn_cols[i]:
                if st.button(f"Analyze → {rec['role']}", key=f"rec_{rec['role']}", use_container_width=True):
                    st.session_state.prefill_role = rec["role"]
                    st.session_state.current_page = "Analyze"
                    st.rerun()

        st.markdown('<div style="height:1px; background:rgba(26,60,35,0.08); margin:2.5rem 0;"></div>', unsafe_allow_html=True)

# ── CHARTS ROW ────────────────────────────────────────
col_chart1, col_chart2 = st.columns([1, 1.4], gap="large")

with col_chart1:
    st.markdown('<div style="font-size:0.65rem; letter-spacing:2px; text-transform:uppercase; color:rgba(26,60,35,0.35); font-family:Inter,sans-serif; margin-bottom:1rem;">Coverage</div>', unsafe_allow_html=True)
    fig_donut = go.Figure(go.Pie(
        values=[len(matched), len(missing)], labels=["Matched", "Missing"], hole=0.72,
        marker=dict(colors=["#1A3C23", "rgba(26,60,35,0.1)"], line=dict(color="#EDEADE", width=3)),
        textinfo="none", hovertemplate="%{label}: %{value}<extra></extra>"
    ))
    fig_donut.add_annotation(text=f"<b>{score}%</b>", x=0.5, y=0.5, showarrow=False,
        font=dict(size=28, color="#1A3C23", family="Fraunces"), xanchor="center")
    fig_donut.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0),
        height=220, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_donut, use_container_width=True, config={"displayModeBar": False})

with col_chart2:
    st.markdown('<div style="font-size:0.65rem; letter-spacing:2px; text-transform:uppercase; color:rgba(26,60,35,0.35); font-family:Inter,sans-serif; margin-bottom:1rem;">Skill Breakdown</div>', unsafe_allow_html=True)
    top_missing   = missing[:8]
    demand_scores = [get_demand_score(s) for s in top_missing]
    fig_bar = go.Figure(go.Bar(
        x=demand_scores, y=top_missing, orientation="h",
        marker=dict(color=["#1A3C23" if d >= 80 else "rgba(26,60,35,0.4)" if d >= 60 else "rgba(26,60,35,0.2)" for d in demand_scores], line=dict(width=0)),
        hovertemplate="%{y}: demand %{x}<extra></extra>"
    ))
    fig_bar.update_layout(
        xaxis=dict(showgrid=False, showticklabels=False, range=[0, 110], zeroline=False),
        yaxis=dict(showgrid=False, tickfont=dict(family="Inter", size=11, color="rgba(26,60,35,0.7)")),
        margin=dict(t=0, b=0, l=0, r=40), height=220,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

st.markdown('<div style="height:1px; background:rgba(26,60,35,0.08); margin:2.5rem 0;"></div>', unsafe_allow_html=True)

# ── SKILLS DETAIL ─────────────────────────────────────
col_have, col_need = st.columns(2, gap="large")

with col_have:
    st.markdown('<div style="font-size:0.65rem; letter-spacing:2px; text-transform:uppercase; color:rgba(26,60,35,0.35); font-family:Inter,sans-serif; margin-bottom:1rem;">Skills You Have</div>', unsafe_allow_html=True)
    chips = "".join([
        f'<span style="background:rgba(42,107,58,0.09); color:#2A6B3A; border:1px solid rgba(42,107,58,0.18); '
        f'padding:0.35rem 0.9rem; border-radius:2px; font-size:0.78rem; font-family:Inter,sans-serif; '
        f'display:inline-block; margin:0.2rem;">{s}</span>' for s in matched
    ]) or '<span style="color:rgba(26,60,35,0.3); font-size:0.85rem;">None matched</span>'
    st.markdown(f'<div style="line-height:2.4;">{chips}</div>', unsafe_allow_html=True)

with col_need:
    st.markdown('<div style="font-size:0.65rem; letter-spacing:2px; text-transform:uppercase; color:rgba(26,60,35,0.35); font-family:Inter,sans-serif; margin-bottom:1rem;">Skills to Acquire</div>', unsafe_allow_html=True)
    chips = "".join([
        f'<span style="background:rgba(122,42,42,0.06); color:#7A2A2A; border:1px solid rgba(122,42,42,0.14); '
        f'padding:0.35rem 0.9rem; border-radius:2px; font-size:0.78rem; font-family:Inter,sans-serif; '
        f'display:inline-block; margin:0.2rem;">{s}</span>' for s in missing
    ]) or '<span style="color:rgba(26,60,35,0.3); font-size:0.85rem;">Nothing missing!</span>'
    st.markdown(f'<div style="line-height:2.4;">{chips}</div>', unsafe_allow_html=True)

st.markdown('<div style="height:1px; background:rgba(26,60,35,0.08); margin:2.5rem 0;"></div>', unsafe_allow_html=True)

# ── DEMAND CARDS ──────────────────────────────────────
if missing:
    st.markdown('<div style="font-size:0.65rem; letter-spacing:2px; text-transform:uppercase; color:rgba(26,60,35,0.35); font-family:Inter,sans-serif; margin-bottom:1.5rem;">Market Demand for Missing Skills</div>', unsafe_allow_html=True)
    cols = st.columns(4, gap="medium")
    for i, skill in enumerate(missing[:8]):
        d        = get_demand_score(skill)
        bar_c    = "#1A3C23" if d >= 80 else "rgba(26,60,35,0.4)" if d >= 60 else "rgba(26,60,35,0.2)"
        tier     = "High" if d >= 80 else "Medium" if d >= 60 else "Low"
        tier_col = "#2A6B3A" if d >= 80 else "#7A5C10" if d >= 60 else "rgba(26,60,35,0.35)"
        with cols[i % 4]:
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.4); border:1px solid rgba(26,60,35,0.09);
                        border-radius:3px; padding:1.2rem; margin-bottom:0.7rem;">
                <div style="font-family:'Fraunces',serif; font-weight:600; font-size:0.9rem;
                            color:#1A3C23; margin-bottom:0.6rem;">{skill}</div>
                <div style="background:rgba(26,60,35,0.08); border-radius:2px; height:3px; margin-bottom:0.5rem;">
                    <div style="background:{bar_c}; width:{d}%; height:3px; border-radius:2px;"></div>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div style="font-size:0.68rem; color:rgba(26,60,35,0.38); font-family:Inter,sans-serif;">{d}/100 demand</div>
                    <div style="font-size:0.6rem; font-weight:600; letter-spacing:1px; text-transform:uppercase;
                                color:{tier_col}; font-family:Inter,sans-serif;">{tier}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

st.markdown('<div style="height:1px; background:rgba(26,60,35,0.08); margin:2.5rem 0;"></div>', unsafe_allow_html=True)

# ── SKILL CLUSTERS ────────────────────────────────────
if user_skills and clusters:
    st.markdown('<div style="font-size:0.65rem; letter-spacing:2px; text-transform:uppercase; color:rgba(26,60,35,0.35); font-family:Inter,sans-serif; margin-bottom:1rem;">Your Skill Profile</div>', unsafe_allow_html=True)
    cluster_cols = st.columns(len(clusters), gap="medium")
    for col, c in zip(cluster_cols, clusters):
        c_name = c["cluster"]
        c_pct  = c["pct"]
        with col:
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.45); border:1px solid rgba(26,60,35,0.1);
                        border-radius:3px; padding:1.2rem 1.4rem;">
                <div style="font-family:'Fraunces',serif; font-weight:600; font-size:0.95rem;
                            color:#1A3C23; margin-bottom:0.8rem;">{c_name}</div>
                <div style="background:rgba(26,60,35,0.08); border-radius:2px; height:4px; margin-bottom:0.6rem;">
                    <div style="background:#1A3C23; height:4px; border-radius:2px; width:{c_pct}%;"></div>
                </div>
                <div style="display:flex; justify-content:space-between;">
                    <div style="font-size:0.72rem; color:rgba(26,60,35,0.45); font-family:Inter,sans-serif;">{c['overlap']}/{c['total']} skills</div>
                    <div style="font-family:'Fraunces',serif; font-weight:700; color:#1A3C23; font-size:0.9rem;">{c_pct}%</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('<div style="height:1px; background:rgba(26,60,35,0.08); margin:2.5rem 0;"></div>', unsafe_allow_html=True)

# ── CTA BUTTONS ───────────────────────────────────────
c1, c2, c3 = st.columns(3, gap="medium")
with c1:
    if st.button("View Roadmap →", type="primary", use_container_width=True):
        st.session_state.current_page = "Roadmap"
        st.rerun()
with c2:
    if st.button("Save Report", use_container_width=True):
        st.session_state.current_page = "Reports"
        st.rerun()
with c3:
    if st.button("New Analysis", use_container_width=True):
        st.session_state.current_page = "Analyze"
        st.rerun()