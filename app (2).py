import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import base64, os

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Jeff Zhou · Portfolio",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Colour palette ────────────────────────────────────────────────────────────
DEEP_BLUE = "#1F3A5F"
LIGHT_GRAY = "#F5F7FA"
TEAL = "#2CB1BC"
WHITE = "#FFFFFF"
TEXT_DARK = "#1A2B3C"
TEXT_MID = "#4A6278"

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

/* ---------- global ---------- */
html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
    background-color: {LIGHT_GRAY};
    color: {TEXT_DARK};
}}

/* ---------- sidebar ---------- */
section[data-testid="stSidebar"] {{
    background-color: {DEEP_BLUE} !important;
    border-right: none;
}}
section[data-testid="stSidebar"] > div {{
    padding-top: 2rem;
}}
section[data-testid="stSidebar"] * {{
    color: #CBD5E1 !important;
}}
/* radio nav labels */
section[data-testid="stSidebar"] .stRadio label {{
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 500 !important;
    color: #CBD5E1 !important;
    padding: 0.6rem 0.8rem !important;
    border-radius: 8px !important;
    display: block !important;
    transition: background 0.2s;
}}
section[data-testid="stSidebar"] .stRadio label:hover {{
    background: rgba(44,177,188,0.15) !important;
    color: {TEAL} !important;
}}

/* ---------- card ---------- */
.card {{
    background: {WHITE};
    border-radius: 14px;
    padding: 1.6rem 1.8rem;
    box-shadow: 0 2px 12px rgba(31,58,95,0.07);
    margin-bottom: 1.2rem;
}}

/* ---------- section title ---------- */
.sec-title {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: {TEAL};
    margin-bottom: 0.5rem;
}}

/* ---------- hero ---------- */
.hero-name {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(2.2rem, 4vw, 3.2rem);
    font-weight: 700;
    color: {DEEP_BLUE};
    line-height: 1.1;
    margin: 0;
}}
.hero-role {{
    font-size: 1rem;
    font-weight: 500;
    color: {TEAL};
    margin-top: 0.35rem;
    letter-spacing: 0.04em;
}}
.hero-bio {{
    font-size: 0.95rem;
    color: {TEXT_MID};
    line-height: 1.7;
    margin-top: 0.9rem;
    max-width: 520px;
}}

/* ---------- contact pills ---------- */
.pill-row {{ display:flex; flex-wrap:wrap; gap:0.45rem; margin-top:1rem; }}
.pill {{
    font-size: 0.78rem;
    background: {LIGHT_GRAY};
    border: 1px solid #DDE3EB;
    border-radius: 999px;
    padding: 0.28rem 0.8rem;
    color: {TEXT_DARK};
    font-weight: 500;
}}

/* ---------- portrait ---------- */
.portrait-wrap {{
    display: flex;
    justify-content: center;
    align-items: center;
}}
.portrait-wrap img {{
    width: 200px;
    height: 200px;
    object-fit: cover;
    border-radius: 50%;
    border: 4px solid {TEAL};
    box-shadow: 0 4px 20px rgba(44,177,188,0.25);
}}

/* ---------- metric cards ---------- */
.metric-row {{ display:flex; gap:1rem; margin-top:0.5rem; flex-wrap:wrap; }}
.metric-box {{
    background: {LIGHT_GRAY};
    border-radius: 10px;
    padding: 0.9rem 1.1rem;
    text-align: center;
    flex: 1;
    min-width: 110px;
    border: 1px solid #DDE3EB;
}}
.metric-val {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: {DEEP_BLUE};
}}
.metric-lab {{
    font-size: 0.72rem;
    color: {TEXT_MID};
    margin-top: 0.15rem;
    font-weight: 500;
}}

/* ---------- skill tag ---------- */
.skill-tag {{
    display: inline-block;
    background: rgba(44,177,188,0.10);
    border: 1px solid rgba(44,177,188,0.35);
    color: {DEEP_BLUE};
    border-radius: 6px;
    padding: 0.25rem 0.65rem;
    font-size: 0.82rem;
    font-weight: 500;
    margin: 0.2rem;
}}

/* ---------- timeline ---------- */
.exp-card {{
    border-left: 3px solid {TEAL};
    padding: 1rem 1.3rem;
    background: {WHITE};
    border-radius: 0 10px 10px 0;
    margin-bottom: 1rem;
    box-shadow: 0 1px 8px rgba(31,58,95,0.06);
}}
.exp-company {{ font-family:'Space Grotesk',sans-serif; font-weight:600; font-size:1.02rem; color:{DEEP_BLUE}; }}
.exp-role    {{ font-size:0.82rem; font-weight:600; color:{TEAL}; margin:0.15rem 0; }}
.exp-sub     {{ font-size:0.78rem; color:{TEXT_MID}; font-style:italic; margin-bottom:0.35rem; }}
.exp-dates   {{ font-size:0.78rem; color:{TEXT_MID}; margin-bottom:0.5rem; }}
.exp-bullets {{ padding-left:1.1rem; margin:0; }}
.exp-bullets li {{ font-size:0.88rem; color:#334155; margin-bottom:0.3rem; line-height:1.55; }}

/* ---------- edu card ---------- */
.edu-card {{
    background: {WHITE};
    border-radius: 10px;
    padding: 1rem 1.3rem;
    border: 1px solid #DDE3EB;
    margin-bottom: 0.8rem;
}}
.edu-degree {{ font-family:'Space Grotesk',sans-serif; font-weight:600; font-size:0.95rem; color:{DEEP_BLUE}; }}
.edu-school {{ font-size:0.82rem; color:{TEAL}; font-weight:500; margin:0.15rem 0; }}
.edu-year   {{ font-size:0.78rem; color:{TEXT_MID}; }}

/* ---------- achievement ---------- */
.ach-item {{
    display: flex;
    align-items: flex-start;
    gap: 0.8rem;
    background: {WHITE};
    border-radius: 10px;
    padding: 0.85rem 1.1rem;
    margin-bottom: 0.7rem;
    border: 1px solid #DDE3EB;
    box-shadow: 0 1px 4px rgba(31,58,95,0.04);
}}
.ach-icon {{ font-size: 1.4rem; line-height:1; }}
.ach-text {{ font-size: 0.9rem; color: {TEXT_DARK}; line-height: 1.5; }}
.ach-label {{ font-size: 0.72rem; font-weight:600; color:{TEAL}; text-transform:uppercase; letter-spacing:0.07em; margin-bottom:0.1rem; }}

/* ---------- logo row ---------- */
.logo-row {{ display:flex; align-items:center; gap:0.8rem; margin-bottom:0.4rem; }}
.logo-row img {{ width:36px; height:36px; object-fit:contain; border-radius:6px; background:white; padding:2px; border:1px solid #DDE3EB; }}

/* ---------- radar toggle buttons ---------- */
div[data-testid="stHorizontalBlock"] .stButton > button {{
    background: {WHITE} !important;
    color: {DEEP_BLUE} !important;
    border: 2px solid #DDE3EB !important;
    border-radius: 8px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    padding: 0.5rem 1rem !important;
    transition: all 0.2s !important;
    width: 100% !important;
}}
div[data-testid="stHorizontalBlock"] .stButton > button:hover {{
    border-color: {TEAL} !important;
    color: {TEAL} !important;
    background: rgba(44,177,188,0.06) !important;
}}

/* ---------- page divider ---------- */
hr.custom {{ border: none; border-top: 1px solid #DDE3EB; margin: 1.5rem 0; }}

/* ---------- download button ---------- */
.stDownloadButton > button {{
    background: {DEEP_BLUE} !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    padding: 0.5rem 1.3rem !important;
}}
</style>
""", unsafe_allow_html=True)

# ── Helpers ───────────────────────────────────────────────────────────────────
def radar_chart(categories, values, color):
    cats = categories + [categories[0]]
    vals = values + [values[0]]
    fig = go.Figure(go.Scatterpolar(
        r=vals, theta=cats, fill="toself",
        fillcolor=f"rgba(44,177,188,0.15)",
        line=dict(color=color, width=2.5),
        marker=dict(size=6, color=color),
    ))
    fig.update_layout(
        polar=dict(
            bgcolor=WHITE,
            angularaxis=dict(tickfont=dict(size=11, family="Inter", color=TEXT_DARK)),
            radialaxis=dict(visible=True, range=[0, 100],
                            tickfont=dict(size=9, color=TEXT_MID),
                            gridcolor="#DDE3EB"),
        ),
        showlegend=False,
        paper_bgcolor=WHITE,
        margin=dict(l=50, r=50, t=40, b=40),
        height=360,
        font=dict(family="Inter"),
    )
    return fig

def img_to_b64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return None

# ── Try loading portrait ──────────────────────────────────────────────────────
portrait_b64 = img_to_b64("headshot.jpeg")

# ── Sidebar nav ───────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style='text-align:center; margin-bottom:2rem;'>
        <div style='font-family:Space Grotesk,sans-serif; font-size:1.1rem; font-weight:700;
                    color:white; letter-spacing:0.04em;'>Jeff Zhou</div>
        <div style='font-size:0.75rem; color:{TEAL}; margin-top:0.2rem;'>MMA Candidate · Rotman</div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "",
        options=["🏠  About Me", "🎓  Education & Skills", "💼  Experience & Projects", "🌟  Achievements"],
        label_visibility="collapsed",
    )
    st.markdown("<div style='height:3rem'></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size:0.7rem; color:#64748B; text-align:center;'>Built with Streamlit · 2025</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — ABOUT ME
# ══════════════════════════════════════════════════════════════════════════════
if "🏠  About Me" in page:

    # ── Hero row ──────────────────────────────────────────────────────────────
    col_info, col_portrait = st.columns([3, 1], gap="large")

    with col_portrait:
        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
        if portrait_b64:
            st.markdown(
                f'<div class="portrait-wrap"><img src="data:image/jpeg;base64,{portrait_b64}"/></div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="portrait-wrap" style="width:200px;height:200px;border-radius:50%;'
                f'background:{LIGHT_GRAY};border:4px solid {TEAL};display:flex;align-items:center;'
                f'justify-content:center;font-size:3rem;">👤</div>',
                unsafe_allow_html=True,
            )

    with col_info:
        st.markdown('<div class="sec-title">Portfolio</div>', unsafe_allow_html=True)
        st.markdown('<p class="hero-name">Jiefu (Jeff) Zhou</p>', unsafe_allow_html=True)
        st.markdown('<p class="hero-role">Marketing Data Analyst · MMA Candidate @ Rotman</p>', unsafe_allow_html=True)
        st.markdown(
            '<p class="hero-bio">Analytics professional at the intersection of finance and data science. '
            'I build predictive models, customer segmentation pipelines, and data-driven strategies that '
            'deliver measurable impact — currently scaling marketing analytics across a 5M+ customer base at BMO. '
            'Passionate about turning messy data into decisions that matter.</p>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="pill-row">'
            '<span class="pill">📍 Toronto, ON</span>'
            '<span class="pill">📞 (613) 854-2788</span>'
            '<span class="pill">✉️ jeffintp.zhou@rotman.utoronto.ca</span>'
            '</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="pill-row">'
            f'<a href="https://www.linkedin.com/in/rotman-mma/" target="_blank" '
            f'style="text-decoration:none;"><span class="pill">🔗 LinkedIn</span></a>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown("<hr class='custom'>", unsafe_allow_html=True)

    # ── Key metrics ───────────────────────────────────────────────────────────
    st.markdown('<div class="sec-title">Impact at a Glance</div>', unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    m1.markdown('<div class="metric-box"><div class="metric-val">$280M</div><div class="metric-lab">Project Analyzed at CITIC</div></div>', unsafe_allow_html=True)
    m2.markdown('<div class="metric-box"><div class="metric-val">5M+</div><div class="metric-lab">Customers Modeled at BMO</div></div>', unsafe_allow_html=True)
    m3.markdown('<div class="metric-box"><div class="metric-val">+9%</div><div class="metric-lab">Prediction Accuracy Gain</div></div>', unsafe_allow_html=True)
    m4.markdown('<div class="metric-box"><div class="metric-val">+15%</div><div class="metric-lab">Analysis Speed Increase</div></div>', unsafe_allow_html=True)

    st.markdown("<hr class='custom'>", unsafe_allow_html=True)

    # ── Skill radar section ───────────────────────────────────────────────────
    st.markdown('<div class="sec-title">Skill Profile</div>', unsafe_allow_html=True)
    st.markdown(
        '<p style="font-size:0.9rem;color:#4A6278;margin-bottom:1rem;">Select a domain to explore skill proficiency:</p>',
        unsafe_allow_html=True,
    )

    if "radar_domain" not in st.session_state:
        st.session_state.radar_domain = "Data Science"

    rb1, rb2, rb3 = st.columns(3)
    with rb1:
        if st.button("📊  Data Science", use_container_width=True):
            st.session_state.radar_domain = "Data Science"
    with rb2:
        if st.button("💹  Finance", use_container_width=True):
            st.session_state.radar_domain = "Finance"
    with rb3:
        if st.button("🧠  General", use_container_width=True):
            st.session_state.radar_domain = "General"

    RADAR_DATA = {
        "Data Science": {
            "cats": ["ML", "Python", "SQL", "R", "Power BI", "LLM"],
            "vals": [90, 90, 90, 60, 75, 60],
        },
        "Finance": {
            "cats": ["Financial Modeling", "Valuation", "Portfolio Theory", "Financial Markets", "Risk Analysis", "Excel / Financial Tools"],
            "vals": [90, 85, 75, 80, 70, 70],
        },
        "General": {
            "cats": ["Problem Solving", "Analytical Thinking", "Business Understanding", "Communication", "Learning Ability", "Project Execution"],
            "vals": [90, 95, 85, 70, 90, 80],
        },
    }

    domain = st.session_state.radar_domain
    d = RADAR_DATA[domain]

    col_radar, col_legend = st.columns([3, 2], gap="large")
    with col_radar:
        st.markdown(
            f'<div style="font-family:Space Grotesk,sans-serif;font-weight:600;font-size:1rem;'
            f'color:{DEEP_BLUE};margin-bottom:0.3rem;">{domain} Skills</div>',
            unsafe_allow_html=True,
        )
        fig = radar_chart(d["cats"], d["vals"], TEAL)
        st.plotly_chart(fig, use_container_width=True)

    with col_legend:
        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        st.markdown(f'<div style="font-family:Space Grotesk,sans-serif;font-weight:600;font-size:0.9rem;color:{DEEP_BLUE};margin-bottom:0.8rem;">Proficiency Breakdown</div>', unsafe_allow_html=True)
        df_skills = pd.DataFrame({"Skill": d["cats"], "Score": d["vals"]}).sort_values("Score", ascending=False)
        for _, row in df_skills.iterrows():
            pct = int(row["Score"])
            bar_color = TEAL if pct >= 80 else ("#6B9FBF" if pct >= 65 else "#94A3B8")
            st.markdown(f"""
            <div style='margin-bottom:0.65rem;'>
                <div style='display:flex;justify-content:space-between;margin-bottom:0.2rem;'>
                    <span style='font-size:0.83rem;font-weight:500;color:{TEXT_DARK};'>{row['Skill']}</span>
                    <span style='font-size:0.83rem;font-weight:600;color:{DEEP_BLUE};'>{pct}</span>
                </div>
                <div style='background:#DDE3EB;border-radius:999px;height:6px;'>
                    <div style='background:{bar_color};width:{pct}%;height:6px;border-radius:999px;'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — EDUCATION & SKILLS
# ══════════════════════════════════════════════════════════════════════════════
elif "🎓  Education & Skills" in page:
    st.markdown('<div class="sec-title">Education</div>', unsafe_allow_html=True)

    edu_data = [
        {
            "degree": "Master of Management Analytics (Candidate)",
            "school": "Rotman School of Management, University of Toronto",
            "year": "2025 – 2026",
            "logo": "https://logo.clearbit.com/rotman.utoronto.ca",
            "details": [
                "🏆 2nd Place — RBAC × Calian Ltd. Data Analytics Case Competition",
                "📌 Member — Rotman Business Analytics Club",
                "📌 Member — Rotman Business Technology Association",
            ],
        },
        {
            "degree": "Honors Bachelor of Commerce (Finance)",
            "school": "University of Ottawa",
            "year": "2021 – 2025",
            "logo": "https://logo.clearbit.com/uottawa.ca",
            "details": [],
        },
    ]

    for e in edu_data:
        logo_html = f'<img src="{e["logo"]}" style="width:40px;height:40px;object-fit:contain;border-radius:8px;border:1px solid #DDE3EB;padding:3px;background:white;" onerror="this.style.display=\'none\'">' if e["logo"] else ""
        details_html = "".join(f'<li style="font-size:0.85rem;color:{TEXT_MID};margin-bottom:0.2rem;">{d}</li>' for d in e["details"])
        details_block = f'<ul style="padding-left:1.1rem;margin-top:0.6rem;">{details_html}</ul>' if e["details"] else ""
        st.markdown(f"""
        <div class="edu-card">
            <div style="display:flex;align-items:center;gap:0.8rem;margin-bottom:0.3rem;">
                {logo_html}
                <div>
                    <div class="edu-degree">{e['degree']}</div>
                    <div class="edu-school">{e['school']}</div>
                    <div class="edu-year">📅 {e['year']}</div>
                </div>
            </div>
            {details_block}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='custom'>", unsafe_allow_html=True)
    st.markdown('<div class="sec-title">Technical Skills</div>', unsafe_allow_html=True)

    skill_groups = {
        "💻 Programming Languages": ["Python", "SQL", "R"],
        "📊 Analytics & BI Tools": ["Power BI", "IBM SPSS Modeler", "SAS Enterprise Guide"],
        "🤖 Machine Learning": ["Supervised Learning", "Customer Segmentation", "SMOTE", "XGBoost", "Sklearn", "LLMs"],
        "📈 Financial Tools": ["Excel / Financial Modeling", "DCF Valuation", "Risk Analysis", "Portfolio Analysis"],
        "🛠️ Other Software": ["Microsoft Word", "PowerPoint", "Tableau"],
    }

    for group, skills in skill_groups.items():
        st.markdown(f'<div style="font-family:Space Grotesk,sans-serif;font-weight:600;font-size:0.9rem;color:{DEEP_BLUE};margin:1rem 0 0.5rem;">{group}</div>', unsafe_allow_html=True)
        tags_html = " ".join(f'<span class="skill-tag">{s}</span>' for s in skills)
        st.markdown(f'<div style="line-height:2.2;">{tags_html}</div>', unsafe_allow_html=True)

    st.markdown("<hr class='custom'>", unsafe_allow_html=True)
    st.markdown('<div class="sec-title">Languages</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="metric-box" style="text-align:left;padding:1rem 1.2rem;">
            <div style="font-size:1.4rem;margin-bottom:0.3rem;">🇺🇸</div>
            <div style="font-family:Space Grotesk,sans-serif;font-weight:600;color:{DEEP_BLUE};">English</div>
            <div style="font-size:0.8rem;color:{TEAL};font-weight:500;">Fluent</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="metric-box" style="text-align:left;padding:1rem 1.2rem;">
            <div style="font-size:1.4rem;margin-bottom:0.3rem;">🇨🇳</div>
            <div style="font-family:Space Grotesk,sans-serif;font-weight:600;color:{DEEP_BLUE};">Mandarin</div>
            <div style="font-size:0.8rem;color:{TEAL};font-weight:500;">Fluent (Native)</div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — EXPERIENCE & PROJECTS
# ══════════════════════════════════════════════════════════════════════════════
elif "💼  Experience & Projects" in page:
    st.markdown('<div class="sec-title">Professional Experience</div>', unsafe_allow_html=True)

    EXPERIENCE = [
        {
            "company": "Bank of Montreal (BMO)",
            "logo": "https://logo.clearbit.com/bmo.com",
            "sub": "Toronto, Canada",
            "role": "Marketing Data Analyst Intern",
            "dates": "Jan 2026 – Present",
            "bullets": [
                "Developed predictive models to estimate 12-month revenue across a 5M+ U.S. customer base, enabling identification of high lifetime value segments.",
                "Built customer segmentation models to define high-value personas and improve targeting precision for marketing campaigns.",
                "Analyzed key profit drivers to support U.S. market expansion strategy using advanced analytics and customer-level revenue modeling.",
                "Designed randomized controlled trials (RCTs) to measure incremental lift and validate campaign targeting strategies.",
                "Contributed to a scalable campaign activation framework to improve marketing ROI across U.S. markets.",
            ],
        },
        {
            "company": "China CITIC Financial Asset Management",
            "logo": "https://logo.clearbit.com/citicgroup.com",
            "sub": "Chengdu, China · One of China's largest state-owned financial asset management institutions",
            "role": "Financial Assistant Intern",
            "dates": "May 2024 – Aug 2024",
            "bullets": [
                "Conducted financial and data analysis for a financing project exceeding RMB 1.4B (CAD $280M), providing insights that informed investment decisions.",
                "Developed risk management framework components that strengthened asset protection and financial stability.",
                "Researched market and economic trends to identify investment opportunities and proactive allocation strategies.",
                "Built DCF and financial models in Excel to assess target companies' profitability, liquidity, and solvency.",
            ],
        },
        {
            "company": "Zevnodata Fintech",
            "logo": "",
            "sub": "Toronto, Canada · AI/ML-powered data solutions company",
            "role": "Business Analyst Intern",
            "dates": "May 2023 – Aug 2023",
            "bullets": [
                "Consolidated and analyzed 50,000+ external records from Capital IQ, Statista, and internal reports — accelerating analysis by 15%.",
                "Processed Lululemon's ~200k-row dataset in IBM SPSS Modeler using SMOTE, C5 tree, and KNN — achieving 9% higher prediction accuracy.",
                "Applied Python (matplotlib, seaborn, sklearn) to uncover revenue growth and market entry opportunities.",
            ],
        },
    ]

    for e in EXPERIENCE:
        bullets_html = "".join(f"<li>{b}</li>" for b in e["bullets"])
        logo_html = f'<img src="{e["logo"]}" style="width:36px;height:36px;object-fit:contain;border-radius:6px;border:1px solid #DDE3EB;padding:3px;background:white;" onerror="this.style.display=\'none\'">' if e["logo"] else f'<div style="width:36px;height:36px;border-radius:6px;background:{LIGHT_GRAY};border:1px solid #DDE3EB;display:flex;align-items:center;justify-content:center;font-size:1rem;">🏢</div>'
        st.markdown(f"""
        <div class="exp-card">
            <div class="logo-row">
                {logo_html}
                <div>
                    <div class="exp-company">{e['company']}</div>
                    <div class="exp-role">{e['role']}</div>
                </div>
            </div>
            <div class="exp-sub">{e['sub']}</div>
            <div class="exp-dates">🗓 {e['dates']}</div>
            <ul class="exp-bullets">{bullets_html}</ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='custom'>", unsafe_allow_html=True)
    st.markdown('<div class="sec-title">Technical Projects</div>', unsafe_allow_html=True)

    PROJECTS = [
        {
            "title": "LLM-Powered Vacation Rental Recommender",
            "year": "2025",
            "logo": "https://logo.clearbit.com/rotman.utoronto.ca",
            "org": "Rotman School of Management",
            "stack": ["Python", "LLM", "NLP", "Data Pipelines", "Matching Algorithms"],
            "desc": "Developed a Python-based CLI application that recommends vacation rentals based on user preferences, budgets, and group sizes. Integrated large language model for natural language query handling and personalized recommendations — inspired by Airbnb's recommendation engine.",
        },
        {
            "title": "RBAC × Calian Ltd. Data Analytics Case",
            "year": "2024",
            "logo": "https://logo.clearbit.com/rotman.utoronto.ca",
            "org": "Rotman Business Analytics Club",
            "stack": ["Python", "Power BI", "Data Analysis", "Presentation"],
            "desc": "Competed in a real-world data analytics case competition sponsored by Calian Ltd. Developed actionable insights and a data-driven strategy that earned 2nd place among competing teams.",
        },
    ]

    for p in PROJECTS:
        tags_html = " ".join(f'<span class="skill-tag">{t}</span>' for t in p["stack"])
        logo_html = f'<img src="{p["logo"]}" style="width:36px;height:36px;object-fit:contain;border-radius:6px;border:1px solid #DDE3EB;padding:3px;background:white;" onerror="this.style.display=\'none\'">'
        st.markdown(f"""
        <div class="exp-card" style="border-left-color:{DEEP_BLUE};">
            <div class="logo-row">
                {logo_html}
                <div>
                    <div class="exp-company">{p['title']}</div>
                    <div class="exp-role">{p['org']}</div>
                </div>
            </div>
            <div class="exp-dates">📅 {p['year']}</div>
            <p style="font-size:0.88rem;color:#334155;line-height:1.6;margin:0.4rem 0 0.6rem;">{p['desc']}</p>
            <div style="line-height:2.2;">{tags_html}</div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — ACHIEVEMENTS
# ══════════════════════════════════════════════════════════════════════════════
elif "🌟  Achievements" in page:
    st.markdown('<div class="sec-title">Achievements & Interests</div>', unsafe_allow_html=True)

    achievements = [
        {
            "icon": "🏆",
            "label": "Case Competition",
            "text": "2nd Place — RBAC × Calian Ltd. Data Analytics Case Competition, using Python and Power BI to deliver actionable data strategy.",
        },
        {
            "icon": "🏸",
            "label": "Athletics",
            "text": "3rd Place — BC High School Badminton Tournament as a key member of the school team.",
        },
        {
            "icon": "♟️",
            "label": "Chess",
            "text": "Ranked Top 9% worldwide in rapid games on chess.com — a testament to strategic thinking and pattern recognition.",
        },
        {
            "icon": "🍡",
            "label": "Entrepreneurial Mindset",
            "text": "Generated $4,000 in revenue by selling homemade Asian snacks — demonstrating initiative, resourcefulness, and business acumen.",
        },
        {
            "icon": "🌐",
            "label": "Languages",
            "text": "Fluent in both English and Mandarin, enabling cross-cultural communication and collaboration in international environments.",
        },
    ]

    for a in achievements:
        st.markdown(f"""
        <div class="ach-item">
            <div class="ach-icon">{a['icon']}</div>
            <div>
                <div class="ach-label">{a['label']}</div>
                <div class="ach-text">{a['text']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='custom'>", unsafe_allow_html=True)
    st.markdown('<div class="sec-title">Connect</div>', unsafe_allow_html=True)

    resume_text = """Jiefu (Jeff) Zhou
(613) 854-2788 | jeffintp.zhou@rotman.utoronto.ca
LinkedIn: https://www.linkedin.com/in/rotman-mma/

TECHNICAL SKILLS
Python, SQL, R, Power BI, SAS Enterprise Guide, IBM SPSS Modeler, Excel

EDUCATION
Master of Management Analytics (Candidate) – Rotman School of Management, University of Toronto (2026)
Honors Bachelor of Commerce (Finance) – University of Ottawa (2025)

EXPERIENCE
Bank of Montreal (BMO) · Marketing Data Analyst Intern (Jan 2026 – Present)
China CITIC Financial Asset Management · Financial Assistant Intern (May 2024 – Aug 2024)
Zevnodata Fintech · Business Analyst Intern (May 2023 – Aug 2023)

PROJECTS
LLM-Powered Vacation Rental Recommender (2025) – Python, LLM, NLP
RBAC × Calian Data Analytics Case – 2nd Place (2024) – Python, Power BI

ACHIEVEMENTS
2nd Place – RBAC × Calian Data Analytics Case Competition
Top 9% worldwide in rapid chess (chess.com)
$4,000 revenue from homemade Asian snacks
Fluent in English and Mandarin
"""
    c1, c2 = st.columns([2, 4])
    with c1:
        st.download_button("⬇ Download Resume (.txt)", resume_text, "jeff_zhou_resume.txt", "text/plain")
    with c2:
        st.link_button("🔗 LinkedIn Profile", "https://www.linkedin.com/in/rotman-mma/")
