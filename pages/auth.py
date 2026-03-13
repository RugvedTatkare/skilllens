import streamlit as st
from database.supabase_client import sign_in, sign_up, get_profile
from modules.skill_analyzer import get_all_roles

def show_auth():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,300;0,400;0,600;0,700;1,300;1,400;1,600;1,700&family=Inter:wght@300;400;500;600&display=swap');

* { font-family: 'Inter', sans-serif !important; }
.stApp { background: #EDEADE !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding-top: 0 !important; padding-bottom: 0 !important;
    padding-left: 0 !important; padding-right: 0 !important;
    max-width: 100% !important;
}

/* ── Inputs: white with green border ── */
div[data-baseweb="input"] {
    background: #ffffff !important;
    border-radius: 6px !important;
    border: none !important;
    box-shadow: 0 0 0 1.5px rgba(26,60,35,0.15) !important;
}
div[data-baseweb="input"] input {
    background: #ffffff !important;
    color: #1A3C23 !important;
    font-size: 0.9rem !important;
    font-family: 'Inter', sans-serif !important;
    border: none !important;
    border-radius: 6px !important;
}
div[data-baseweb="input"] input::placeholder {
    color: rgba(26,60,35,0.28) !important;
}
div[data-baseweb="input"]:focus-within {
    box-shadow: 0 0 0 2px rgba(26,60,35,0.5) !important;
}

/* ── Labels ── */
.stTextInput label, .stSelectbox label, [data-testid="stWidgetLabel"] p {
    color: rgba(26,60,35,0.45) !important;
    font-size: 0.6rem !important; font-weight: 500 !important;
    letter-spacing: 2px !important; text-transform: uppercase !important;
    font-family: 'Inter', sans-serif !important;
}

/* ── Selectbox ── */
div[data-baseweb="select"] > div:first-child {
    background: #ffffff !important;
    border: none !important;
    border-radius: 6px !important;
    box-shadow: 0 0 0 1.5px rgba(26,60,35,0.15) !important;
    min-height: 46px !important;
}
div[data-baseweb="select"] span { color: #1A3C23 !important; font-size: 0.9rem !important; }
div[data-baseweb="select"] svg { fill: rgba(26,60,35,0.5) !important; }
[data-baseweb="popover"] { z-index: 999999 !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid rgba(26,60,35,0.1) !important;
    gap: 0 !important; margin-bottom: 1.4rem !important;
}
.stTabs [data-baseweb="tab"] {
    font-size: 0.65rem !important; letter-spacing: 2px !important;
    text-transform: uppercase !important; color: rgba(26,60,35,0.3) !important;
    padding: 0.8rem 1.6rem !important; background: transparent !important;
    font-family: 'Inter', sans-serif !important; font-weight: 500 !important;
}
.stTabs [aria-selected="true"] {
    color: #1A3C23 !important; font-weight: 600 !important;
    background: transparent !important;
}
.stTabs [data-baseweb="tab-highlight"] {
    background-color: #1A3C23 !important; height: 2px !important;
}
.stTabs [data-baseweb="tab-border"] { background: transparent !important; }

/* ── Button ── */
.stButton > button[kind="primary"] {
    background: #1A3C23 !important; border: none !important;
    color: #EDEADE !important; font-weight: 600 !important;
    font-size: 0.72rem !important; letter-spacing: 2px !important;
    text-transform: uppercase !important; border-radius: 6px !important;
    padding: 0.8rem !important; font-family: 'Inter', sans-serif !important;
}
.stButton > button[kind="primary"]:hover {
    background: #2C5E38 !important; transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(26,60,35,0.2) !important;
}
.stAlert { border-radius: 6px !important; }

/* ── Fix password eye button ── */
[data-testid="stTextInputRootElement"] button,
div[data-baseweb="input"] button {
    background: #ffffff !important;
    border: none !important;
    border-left: none !important;
    box-shadow: none !important;
    color: rgba(26,60,35,0.45) !important;
    margin: 0 !important;
    padding: 0 12px !important;
}
div[data-baseweb="input"] button svg {
    fill: rgba(26,60,35,0.45) !important;
    width: 18px !important;
    height: 18px !important;
}
div[data-baseweb="input"] button:hover svg {
    fill: rgba(26,60,35,0.75) !important;
}
/* Remove the separator line */
div[data-baseweb="input"] > div {
    border: none !important;
    box-shadow: none !important;
}
</style>
""", unsafe_allow_html=True)

    _, mid, _ = st.columns([1, 1.2, 1])

    with mid:
        st.markdown("<div style='height:8vh'></div>", unsafe_allow_html=True)

        # Headline
        st.markdown("""
<div style="text-align:center; margin-bottom:2.8rem;">
    <div style="font-family:'Fraunces',serif; font-style:italic; font-size:1rem;
                color:rgba(26,60,35,0.3); letter-spacing:1px; margin-bottom:1.8rem;">
        — SkillLens —
    </div>
    <div style="font-family:'Fraunces',serif; font-size:3.2rem; font-weight:300;
                color:#1A3C23; line-height:1.05; letter-spacing:-1.5px; margin-bottom:1rem;">
        Know exactly<br>where you <em style="font-weight:700; font-style:italic;">stand.</em>
    </div>
    <div style="font-size:0.68rem; color:rgba(26,60,35,0.3); font-family:'Inter',sans-serif;
                letter-spacing:2px; text-transform:uppercase;">
        Map your skills &nbsp;·&nbsp; Find your gaps &nbsp;·&nbsp; Get there faster
    </div>
</div>
""", unsafe_allow_html=True)

        # Divider
        st.markdown("""
<div style="display:flex; align-items:center; gap:1rem; margin-bottom:2rem;">
    <div style="flex:1; height:1px; background:rgba(26,60,35,0.08);"></div>
    <div style="font-size:0.55rem; letter-spacing:3px; text-transform:uppercase;
                color:rgba(26,60,35,0.2); font-family:'Inter',sans-serif;">your account</div>
    <div style="flex:1; height:1px; background:rgba(26,60,35,0.08);"></div>
</div>
""", unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["Sign In", "Create Account"])

        with tab1:
            email    = st.text_input("Email",    placeholder="you@example.com", key="si_email")
            password = st.text_input("Password", type="password", placeholder="min 6 characters", key="si_pass")
            st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
            if st.button("Sign In →", type="primary", use_container_width=True, key="si_btn"):
                if not email or not password:
                    st.error("Please fill in all fields.")
                else:
                    with st.spinner(""):
                        res, err = sign_in(email, password)
                    if err or not res or not res.user:
                        st.error("Invalid email or password.")
                    else:
                        profile = get_profile(res.user.id)
                        st.session_state.user          = res.user
                        st.session_state.user_id       = res.user.id
                        st.session_state.user_name     = profile["name"] if profile else email
                        st.session_state.user_email    = email
                        st.session_state.logged_in     = True
                        st.session_state.current_page  = "Home"
                        st.session_state.access_token  = res.session.access_token
                        st.session_state.refresh_token = res.session.refresh_token
                        st.rerun()

        with tab2:
            roles       = get_all_roles()
            name        = st.text_input("Full Name", placeholder="your name",       key="su_name")
            email_su    = st.text_input("Email",     placeholder="you@example.com", key="su_email")
            password_su = st.text_input("Password",  type="password",
                                        placeholder="min 6 characters",             key="su_pass")
            exp         = st.selectbox("Experience",
                            ["Student", "Fresher", "1-2 yrs", "3-5 yrs", "5+ yrs"], key="su_exp")
            target      = st.selectbox("Target Role", roles,                        key="su_role")
            st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
            if st.button("Create Account →", type="primary", use_container_width=True, key="su_btn"):
                if not all([name, email_su, password_su]):
                    st.error("Please fill in all fields.")
                elif len(password_su) < 6:
                    st.error("Password must be at least 6 characters.")
                else:
                    with st.spinner(""):
                        res, err = sign_up(email_su, password_su, name, exp, target)
                    if err:
                        st.error(f"Error: {err}")
                    elif res and res.user:
                        st.success("Account created! Please sign in.")
                    else:
                        st.error("Something went wrong.")

        st.markdown("<div style='height:8vh'></div>", unsafe_allow_html=True)