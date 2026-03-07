import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Jeff Zhou · Resume",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@300;400;500&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --ink:    #0d0d0d;
    --paper:  #f5f0e8;
    --cream:  #ede8dd;
    --accent: #c84b31;
    --muted:  #7a7068;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--paper);
    color: var(--ink);
}

section[data-testid="stSidebar"] {
    background-color: var(--ink) !important;
}
section[data-testid="stSidebar"] * {
    color: var(--paper) !important;
}

.hero-name {
    font-family: 'DM Serif Display', serif;
    font-size: clamp(2.8rem, 6vw, 5rem);
    line-height: 1;
    letter-spacing: -0.02em;
    color: var(--ink);
    margin: 0;
}
.hero-title {
    font-family: 'DM Mono', monospace;
    font-size: 0.9rem;
    font-weight: 400;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--accent);
    margin-top: 0.4rem;
}
.hero-tagline {
    font-size: 1.05rem;
    color: var(--muted);
    margin-top: 1rem;
    max-width: 520px;
    line-height: 1.6;
}

.section-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--accent);
    border-bottom: 1px solid var(--cream);
    padding-bottom: 0.4rem;
    margin-bottom: 1.2rem;
    margin-top: 2rem;
}

.pill-row { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 1rem; }
.pill {
    font-family: 'DM Mono', monospace;
    font-size: 0.78rem;
    background: var(--cream);
    border: 1px solid #d4cec4;
    border-radius: 999px;
    padding: 0.3rem 0.85rem;
    color: var(--ink);
}

.timeline-card {
    border-left: 3px solid var(--accent);
    padding: 0.9rem 1.2rem;
    background: white;
    border-radius: 0 8px 8px 0;
    margin-bottom: 1rem;
    box-shadow: 0 1px 6px rgba(0,0,0,0.05);
}
.tc-company { font-weight: 600; font-size: 1rem; }
.tc-role    { font-family: 'DM Mono', monospace; font-size: 0.8rem; color: var(--accent); margin: 0.15rem 0; }
.tc-dates   { font-size: 0.8rem; color: var(--muted); margin-bottom: 0.5rem; }
.tc-sub     { font-size: 0.78rem; color: var(--muted); font-style: italic; margin-bottom: 0.4rem; }
.tc-bullets { padding-left: 1.1rem; margin: 0; }
.tc-bullets li { font-size: 0.9rem; color: #333; margin-bottom: 0.25rem; line-height: 1.5; }

.metric-card {
    background: white;
    border-radius: 10px;
    padding: 1.1rem 1.2rem;
    text-align: center;
    box-shadow: 0 1px 6px rgba(0,0,0,0.06);
}
.mc-val  { font-family: 'DM Serif Display', serif; font-size: 2.2rem; color: var(--accent); }
.mc-lab  { font-size: 0.78rem; color: var(--muted); margin-top: 0.15rem; }

.edu-card {
    background: white;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    box-shadow: 0 1px 6px rgba(0,0,0,0.05);
    margin-bottom: 0.8rem;
}
.edu-degree { font-weight: 600; font-size: 0.95rem; }
.edu-school { font-family: 'DM Mono', monospace; font-size: 0.8rem; color: var(--accent); }
.edu-year   { font-size: 0.8rem; color: var(--muted); }

.stDownloadButton > button {
    background: var(--accent) !important;
    color: white !important;
    border: none !important;
    border-radius: 6px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.05em !important;
    padding: 0.5rem 1.2rem !important;
}
</style>
""", unsafe_allow_html=True)

# ── Data ──────────────────────────────────────────────────────────────────────
SKILLS = {
    "Python":                    90,
    "SQL":                       85,
    "R":                         75,
    "Power BI":                  80,
    "Machine Learning":          82,
    "IBM SPSS Modeler":          70,
    "SAS Enterprise Guide":      68,
    "Excel / Financial Modeling":85,
    "Data Visualization":        80,
}

EXPERIENCE = [
    {
        "company": "Bank of Montreal (BMO)",
        "sub": "Toronto, Canada",
        "role": "Marketing Data Analyst Intern",
        "dates": "Jan 2026 – Present",
        "months": 3,
        "bullets": [
            "Developed predictive models to estimate 12-month revenue across a 5M+ U.S. customer base, enabling identification of high lifetime value segments.",
            "Built customer segmentation models to define high-value personas and improve targeting precision for marketing campaigns.",
            "Analyzed key profit drivers to support U.S. market expansion strategy using advanced analytics and customer-level revenue modeling.",
            "Designing randomized controlled trials (RCTs) to measure incremental lift and validate campaign targeting strategies.",
            "Contributed to the development of a scalable campaign activation framework to improve marketing ROI across U.S. markets.",
        ],
    },
    {
        "company": "China CITIC Financial Asset Management",
        "sub": "Chengdu, China · One of China's largest state-owned financial asset management institutions",
        "role": "Financial Assistant Intern",
        "dates": "May 2024 – Aug 2024",
        "months": 4,
        "bullets": [
            "Conducted financial and data analysis for a financing project exceeding RMB 1.4B (CAD $280M), providing insights that informed investment decisions and funding structure.",
            "Developed risk management framework components that strengthened asset protection and improved financial stability.",
            "Researched market and economic trends to identify investment opportunities, enabling proactive allocation strategies.",
            "Built DCF and financial models in Excel to assess target companies' profitability, liquidity, and solvency.",
        ],
    },
    {
        "company": "Zevnodata Fintech",
        "sub": "Toronto, Canada · AI/ML-powered data solutions company",
        "role": "Business Analyst Intern",
        "dates": "May 2023 – Aug 2023",
        "months": 4,
        "bullets": [
            "Consolidated and analyzed 50,000+ external records from Capital IQ, Statista, and internal reports — accelerating business performance analysis by 15%.",
            "Cleaned and processed Lululemon's ~200k-row transaction dataset in IBM SPSS Modeler using SMOTE, C5 tree, and KNN — achieving 9% higher prediction accuracy.",
            "Applied Python (matplotlib, seaborn, sklearn) to uncover revenue growth and market entry opportunities.",
        ],
    },
]

EDUCATION = [
    ("Master of Management Analytics (Candidate)", "Rotman School of Management, University of Toronto", "2026"),
    ("Honors Bachelor of Commerce (Finance)", "University of Ottawa", "2025"),
]

PROJECTS = pd.DataFrame({
    "Project":    ["LLM Vacation Rental Recommender", "RBAC × Calian Data Analytics Case"],
    "Year":       ["2025", "2024"],
    "Tech Stack": ["Python · LLM · NLP · Data Pipelines", "Python · Power BI"],
    "Highlight":  ["Airbnb-inspired CLI with natural language query handling", "🏆 2nd Place finish"],
})

ACHIEVEMENTS = [
    "🏆 2nd Place – RBAC × Calian Ltd. Data Analytics Case Competition",
    "🏸 3rd Place – BC High School Badminton Tournament",
    "♟️ Top 9% worldwide in rapid chess (chess.com)",
    "🍡 $4,000 revenue generated selling homemade Asian snacks",
    "🌐 Fluent in English and Mandarin",
]

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎛️ Controls")
    st.caption("Customise what you see")
    st.markdown("---")

    st.markdown("**Skill proficiency threshold**")
    min_skill = st.slider(
        "Show skills ≥", min_value=0, max_value=100, value=50, step=5,
        help="Hide skills below this proficiency level"
    )

    st.markdown("**Experience filter**")
    roles = ["All"] + [e["role"] for e in EXPERIENCE]
    selected_role = st.selectbox("Filter by role", roles)

    st.markdown("**Sections to display**")
    show_projects     = st.checkbox("Projects", value=True)
    show_achievements = st.checkbox("Achievements & Interests", value=True)
    show_education    = st.checkbox("Education", value=True)

    chart_type = st.radio(
        "Skill chart style",
        ["Horizontal bars", "Radar / Spider"],
        index=0,
    )

    st.markdown("---")
    st.caption("Built with Streamlit · Jeff Zhou · 2025")

# ── HEADER ────────────────────────────────────────────────────────────────────
col_h, col_metrics = st.columns([3, 2], gap="large")

with col_h:
    st.markdown('<p class="hero-name">Jiefu (Jeff) Zhou</p>', unsafe_allow_html=True)
    st.markdown('<p class="hero-title">Marketing Data Analyst · MMA Candidate @ Rotman</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="hero-tagline">Analytics professional bridging finance and data science. '
        'I build predictive models, customer segmentation pipelines, and data-driven strategies '
        'that move the needle — currently doing exactly that at BMO.</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="pill-row">'
        '<span class="pill">📍 Toronto, ON</span>'
        '<span class="pill">📞 (613) 854-2788</span>'
        '<span class="pill">✉️ jeffintp.zhou@rotman.utoronto.ca</span>'
        '<span class="pill">🔗 LinkedIn – Jiefu</span>'
        '</div>',
        unsafe_allow_html=True,
    )

with col_metrics:
    st.markdown("<div style='height:1.6rem'></div>", unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    m1.markdown('<div class="metric-card"><div class="mc-val">$280M</div><div class="mc-lab">Project Analyzed at CITIC</div></div>', unsafe_allow_html=True)
    m2.markdown('<div class="metric-card"><div class="mc-val">5M+</div><div class="mc-lab">Customers Modeled at BMO</div></div>', unsafe_allow_html=True)
    m3.markdown('<div class="metric-card"><div class="mc-val">+9%</div><div class="mc-lab">Prediction Accuracy Gain</div></div>', unsafe_allow_html=True)

st.markdown("<hr style='margin:2rem 0; border-color:#ddd8ce'>", unsafe_allow_html=True)

# ── SKILLS ────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Skills & Proficiency</div>', unsafe_allow_html=True)

filtered_skills = {k: v for k, v in SKILLS.items() if v >= min_skill}

if not filtered_skills:
    st.info("No skills match the current threshold. Lower the slider in the sidebar.")
else:
    sk_df = pd.DataFrame({"Skill": list(filtered_skills.keys()), "Level": list(filtered_skills.values())})
    sk_df = sk_df.sort_values("Level", ascending=True)

    if chart_type == "Horizontal bars":
        fig = px.bar(
            sk_df, x="Level", y="Skill", orientation="h",
            text="Level", range_x=[0, 100],
            color="Level",
            color_continuous_scale=["#f2e8df", "#c84b31"],
        )
        fig.update_traces(texttemplate="%{text}%", textposition="outside", marker_line_width=0)
        fig.update_layout(
            coloraxis_showscale=False,
            plot_bgcolor="#ffffff", paper_bgcolor="#f5f0e8",
            margin=dict(l=0, r=40, t=10, b=10),
            height=max(260, len(filtered_skills) * 44),
            font=dict(family="DM Sans", size=13),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, title=""),
            yaxis=dict(title=""),
        )
    else:
        categories = list(filtered_skills.keys())
        values = list(filtered_skills.values()) + [list(filtered_skills.values())[0]]
        cats_closed = categories + [categories[0]]
        fig = go.Figure(go.Scatterpolar(
            r=values, theta=cats_closed, fill="toself",
            fillcolor="rgba(200,75,49,0.18)",
            line=dict(color="#c84b31", width=2),
        ))
        fig.update_layout(
            polar=dict(
                bgcolor="white",
                radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(size=10)),
            ),
            showlegend=False,
            paper_bgcolor="#f5f0e8",
            margin=dict(l=40, r=40, t=20, b=20),
            height=380,
            font=dict(family="DM Sans"),
        )

    st.plotly_chart(fig, use_container_width=True)

# ── EXPERIENCE ────────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Work Experience</div>', unsafe_allow_html=True)

exp_df = pd.DataFrame({
    "Role":    [e["role"]    for e in EXPERIENCE],
    "Company": [e["company"] for e in EXPERIENCE],
    "Months":  [e["months"]  for e in EXPERIENCE],
})

fig_exp = px.bar(
    exp_df, x="Months", y="Company", orientation="h",
    text="Role",
    color="Months", color_continuous_scale=["#f2e8df", "#c84b31"],
)
fig_exp.update_traces(textposition="inside", insidetextanchor="start",
                      textfont=dict(size=12, family="DM Mono"), marker_line_width=0)
fig_exp.update_layout(
    coloraxis_showscale=False,
    plot_bgcolor="white", paper_bgcolor="#f5f0e8",
    margin=dict(l=0, r=40, t=10, b=10), height=200,
    font=dict(family="DM Sans", size=13),
    xaxis=dict(title="Months", showgrid=True, gridcolor="#eee"),
    yaxis=dict(title=""),
)
st.plotly_chart(fig_exp, use_container_width=True)

display_exp = EXPERIENCE if selected_role == "All" else [e for e in EXPERIENCE if e["role"] == selected_role]
for e in display_exp:
    bullets_html = "".join(f"<li>{b}</li>" for b in e["bullets"])
    st.markdown(f"""
    <div class="timeline-card">
        <div class="tc-company">{e['company']}</div>
        <div class="tc-role">{e['role']}</div>
        <div class="tc-sub">{e['sub']}</div>
        <div class="tc-dates">🗓 {e['dates']}</div>
        <ul class="tc-bullets">{bullets_html}</ul>
    </div>""", unsafe_allow_html=True)

# ── EDUCATION ─────────────────────────────────────────────────────────────────
if show_education:
    st.markdown('<div class="section-label">Education</div>', unsafe_allow_html=True)
    for degree, school, year in EDUCATION:
        st.markdown(f"""
        <div class="edu-card">
            <div class="edu-degree">{degree}</div>
            <div class="edu-school">{school}</div>
            <div class="edu-year">{year}</div>
        </div>""", unsafe_allow_html=True)
    st.markdown("📌 **Club Memberships:** Rotman Business Analytics Club · Rotman Business Technology Association")

# ── PROJECTS ──────────────────────────────────────────────────────────────────
if show_projects:
    st.markdown('<div class="section-label">Technical Projects</div>', unsafe_allow_html=True)
    st.dataframe(PROJECTS, use_container_width=True, hide_index=True)

# ── ACHIEVEMENTS ──────────────────────────────────────────────────────────────
if show_achievements:
    st.markdown('<div class="section-label">Achievements & Interests</div>', unsafe_allow_html=True)
    for a in ACHIEVEMENTS:
        st.markdown(a)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("<hr style='margin:2.5rem 0 1rem; border-color:#ddd8ce'>", unsafe_allow_html=True)

resume_text = """Jiefu (Jeff) Zhou
(613) 854-2788 | jeffintp.zhou@rotman.utoronto.ca | LinkedIn: Jiefu

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
RBAC x Calian Ltd. Data Analytics Case Competition – 2nd Place (2024) – Python, Power BI

ACHIEVEMENTS
2nd Place – RBAC x Calian Data Analytics Case Competition
Top 9% worldwide in rapid chess (chess.com)
Fluent in English and Mandarin
"""

col1, col2, _ = st.columns([2, 2, 4])
with col1:
    st.download_button("⬇ Download Resume (.txt)", resume_text, "jeff_zhou_resume.txt", "text/plain")
with col2:
    st.link_button("🔗 View LinkedIn", "https://linkedin.com")

st.caption("Built with Streamlit · Jiefu (Jeff) Zhou · 2025")
