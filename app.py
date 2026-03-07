pip install streamlit
pip install plotly
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Alex Rivera · Resume",
    page_icon="🚀",
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

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: var(--ink) !important;
}
section[data-testid="stSidebar"] * {
    color: var(--paper) !important;
}
section[data-testid="stSidebar"] .stSlider > div > div > div > div {
    background: var(--accent) !important;
}

/* Name hero */
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

/* Section headers */
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

/* Contact pills */
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

/* Timeline cards */
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
.tc-bullets { padding-left: 1.1rem; margin: 0; }
.tc-bullets li { font-size: 0.9rem; color: #333; margin-bottom: 0.25rem; line-height: 1.5; }

/* Metric cards */
.metric-card {
    background: white;
    border-radius: 10px;
    padding: 1.1rem 1.2rem;
    text-align: center;
    box-shadow: 0 1px 6px rgba(0,0,0,0.06);
}
.mc-val  { font-family: 'DM Serif Display', serif; font-size: 2.2rem; color: var(--accent); }
.mc-lab  { font-size: 0.78rem; color: var(--muted); margin-top: 0.15rem; }

/* Education cards */
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

/* Download button override */
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
    "Python":           95,
    "Machine Learning": 90,
    "SQL":              88,
    "Data Viz":         85,
    "PyTorch":          80,
    "MLOps / Docker":   75,
    "Spark":            70,
    "TypeScript":       60,
    "Go":               45,
}

EXPERIENCE = [
    {
        "company": "Nexus AI",
        "role": "Senior ML Engineer",
        "dates": "Mar 2022 – Present",
        "years": 3,
        "bullets": [
            "Led end-to-end training pipeline for a 7B-parameter LLM, cutting inference latency 38%.",
            "Built real-time feature store serving 400 M+ predictions/day with <5 ms p99.",
            "Mentored team of 4 junior engineers; established ML platform best practices.",
        ],
    },
    {
        "company": "DataSphere Inc.",
        "role": "Data Scientist",
        "dates": "Jun 2019 – Feb 2022",
        "years": 2.7,
        "bullets": [
            "Developed churn prediction model that saved $4 M ARR in first year.",
            "Automated reporting dashboard used by 120+ stakeholders across 3 continents.",
            "Ran A/B experiments end-to-end: design, instrumentation, analysis, shipping.",
        ],
    },
    {
        "company": "Qubit Analytics",
        "role": "Data Analyst",
        "dates": "Jan 2018 – May 2019",
        "years": 1.3,
        "bullets": [
            "Built SQL-based ETL pipelines replacing manual Excel workflows (~10 hrs/week saved).",
            "Created Tableau dashboards tracking KPIs for C-suite weekly reviews.",
        ],
    },
]

EDUCATION = [
    ("M.Sc. Computer Science – Machine Learning", "Stanford University", "2017"),
    ("B.Sc. Statistics & Applied Mathematics", "UC Davis", "2015"),
]

PROJECTS = pd.DataFrame({
    "Project":     ["LLM FineTuner OSS", "StreamViz", "ChurnShield", "AutoETL"],
    "Tech Stack":  ["Python · LoRA · vLLM", "React · D3 · FastAPI", "XGBoost · SHAP", "Airflow · dbt · BigQuery"],
    "Stars ⭐":    [1_240, 430, 870, 215],
    "Status":      ["Active", "Active", "Archived", "Active"],
})

CERTS = [
    "AWS Certified Machine Learning – Specialty (2023)",
    "Google Professional Data Engineer (2022)",
    "Deep Learning Specialization – Coursera / DeepLearning.AI (2020)",
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
    show_projects  = st.checkbox("Open-source projects", value=True)
    show_certs     = st.checkbox("Certifications",        value=True)
    show_education = st.checkbox("Education",             value=True)

    chart_type = st.radio(
        "Skill chart style",
        ["Horizontal bars", "Radar / Spider"],
        index=0,
    )

    st.markdown("---")
    st.caption("Built with Streamlit · v1.0")

# ── HEADER ────────────────────────────────────────────────────────────────────
col_h, col_metrics = st.columns([3, 2], gap="large")

with col_h:
    st.markdown('<p class="hero-name">Alex Rivera</p>', unsafe_allow_html=True)
    st.markdown('<p class="hero-title">Senior ML Engineer &amp; Data Scientist</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="hero-tagline">I turn messy data into reliable models and reliable models into products people trust. '
        'Currently making LLMs go fast at Nexus AI.</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="pill-row">'
        '<span class="pill">📍 San Francisco, CA</span>'
        '<span class="pill">✉️ alex@example.com</span>'
        '<span class="pill">🔗 linkedin.com/in/alexrivera</span>'
        '<span class="pill">🐙 github.com/alexrivera</span>'
        '</div>',
        unsafe_allow_html=True,
    )

with col_metrics:
    st.markdown("<div style='height:1.6rem'></div>", unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    m1.markdown('<div class="metric-card"><div class="mc-val">7+</div><div class="mc-lab">Years Experience</div></div>', unsafe_allow_html=True)
    m2.markdown('<div class="metric-card"><div class="mc-val">$4M</div><div class="mc-lab">Revenue Impact</div></div>', unsafe_allow_html=True)
    m3.markdown('<div class="metric-card"><div class="mc-val">1.2k</div><div class="mc-lab">GitHub Stars</div></div>', unsafe_allow_html=True)

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
    else:  # Radar
        categories = list(filtered_skills.keys())
        values     = list(filtered_skills.values()) + [list(filtered_skills.values())[0]]
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

# Timeline chart
exp_df = pd.DataFrame({
    "Role":    [e["role"]    for e in EXPERIENCE],
    "Company": [e["company"] for e in EXPERIENCE],
    "Years":   [e["years"]   for e in EXPERIENCE],
})

fig_exp = px.bar(
    exp_df, x="Years", y="Company", orientation="h",
    text="Role",
    color="Years", color_continuous_scale=["#f2e8df", "#c84b31"],
)
fig_exp.update_traces(textposition="inside", insidetextanchor="start",
                      textfont=dict(size=12, family="DM Mono"), marker_line_width=0)
fig_exp.update_layout(
    coloraxis_showscale=False,
    plot_bgcolor="white", paper_bgcolor="#f5f0e8",
    margin=dict(l=0, r=40, t=10, b=10), height=200,
    font=dict(family="DM Sans", size=13),
    xaxis=dict(title="Years", showgrid=True, gridcolor="#eee"),
    yaxis=dict(title=""),
)
st.plotly_chart(fig_exp, use_container_width=True)

# Cards
display_exp = EXPERIENCE if selected_role == "All" else [e for e in EXPERIENCE if e["role"] == selected_role]
for e in display_exp:
    bullets_html = "".join(f"<li>{b}</li>" for b in e["bullets"])
    st.markdown(f"""
    <div class="timeline-card">
        <div class="tc-company">{e['company']}</div>
        <div class="tc-role">{e['role']}</div>
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

# ── PROJECTS ──────────────────────────────────────────────────────────────────
if show_projects:
    st.markdown('<div class="section-label">Open-Source Projects</div>', unsafe_allow_html=True)
    styled = PROJECTS.style.background_gradient(
        subset=["Stars ⭐"], cmap="YlOrRd"
    ).set_table_styles([
        {"selector": "th", "props": [("font-family", "DM Mono, monospace"), ("font-size", "0.8rem"),
                                     ("background", "#0d0d0d"), ("color", "#f5f0e8")]},
        {"selector": "td", "props": [("font-size", "0.88rem")]},
    ])
    st.dataframe(PROJECTS, use_container_width=True, hide_index=True)

# ── CERTIFICATIONS ────────────────────────────────────────────────────────────
if show_certs:
    st.markdown('<div class="section-label">Certifications</div>', unsafe_allow_html=True)
    for c in CERTS:
        st.markdown(f"🏅 {c}")

# ── CONTACT / FOOTER ──────────────────────────────────────────────────────────
st.markdown("<hr style='margin:2.5rem 0 1rem; border-color:#ddd8ce'>", unsafe_allow_html=True)
col_cta1, col_cta2, col_spacer = st.columns([2, 2, 4])
with col_cta1:
    resume_text = """Alex Rivera – Senior ML Engineer
alex@example.com | linkedin.com/in/alexrivera | github.com/alexrivera

EXPERIENCE
Nexus AI · Senior ML Engineer (Mar 2022–Present)
DataSphere Inc. · Data Scientist (Jun 2019–Feb 2022)
Qubit Analytics · Data Analyst (Jan 2018–May 2019)

EDUCATION
M.Sc. Computer Science – ML, Stanford (2017)
B.Sc. Statistics & Applied Math, UC Davis (2015)
"""
    st.download_button("⬇ Download Resume (.txt)", resume_text, "alex_rivera_resume.txt", "text/plain")
with col_cta2:
    st.link_button("🔗 View GitHub", "https://github.com")

st.caption("Built with Streamlit · Alex Rivera · 2025")
