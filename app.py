import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import base64, os
from PIL import Image
import requests
from io import BytesIO

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Jeff Zhou · Portfolio",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

DEEP_BLUE  = "#1F3A5F"
LIGHT_GRAY = "#F5F7FA"
TEAL       = "#2CB1BC"
WHITE      = "#FFFFFF"
TEXT_DARK  = "#1A2B3C"
TEXT_MID   = "#4A6278"

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
    background-color: {LIGHT_GRAY};
    color: {TEXT_DARK};
}}
section[data-testid="stSidebar"] {{ background-color: {DEEP_BLUE} !important; }}
section[data-testid="stSidebar"] * {{ color: #CBD5E1 !important; }}
section[data-testid="stSidebar"] .stRadio label {{
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.95rem !important; font-weight: 500 !important;
    padding: 0.6rem 0.8rem !important; border-radius: 8px !important;
    display: block !important;
}}

.sec-title {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.72rem; font-weight: 600;
    letter-spacing: 0.18em; text-transform: uppercase;
    color: {TEAL}; margin-bottom: 0.5rem;
}}

.hero-name {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(2.2rem, 4vw, 3.2rem);
    font-weight: 700; color: {DEEP_BLUE}; line-height: 1.1; margin: 0;
}}
.hero-role {{
    font-size: 1rem; font-weight: 500; color: {TEAL};
    margin-top: 0.35rem; letter-spacing: 0.04em;
}}
.hero-bio {{
    font-size: 0.95rem; color: {TEXT_MID}; line-height: 1.7;
    margin-top: 0.9rem; max-width: 520px;
}}
.pill-row {{ display:flex; flex-wrap:wrap; gap:0.45rem; margin-top:1rem; }}
.pill {{
    font-size: 0.78rem; background: {LIGHT_GRAY};
    border: 1px solid #DDE3EB; border-radius: 999px;
    padding: 0.28rem 0.8rem; color: {TEXT_DARK}; font-weight: 500;
}}

/* portrait uses st.image — just style its container */
.portrait-container {{
    display: flex; justify-content: center; align-items: center;
    padding-top: 0.5rem;
}}
.portrait-container img {{
    border-radius: 50% !important;
    border: 4px solid {TEAL} !important;
    box-shadow: 0 4px 24px rgba(44,177,188,0.28) !important;
    object-fit: cover; object-position: center top;
}}

.metric-box {{
    background: {WHITE}; border-radius: 10px;
    padding: 0.9rem 1.1rem; text-align: center;
    border: 1px solid #DDE3EB;
}}
.metric-val {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.6rem; font-weight: 700; color: {DEEP_BLUE};
}}
.metric-lab {{ font-size: 0.72rem; color: {TEXT_MID}; margin-top: 0.15rem; font-weight: 500; }}

.skill-tag {{
    display: inline-block; background: rgba(44,177,188,0.10);
    border: 1px solid rgba(44,177,188,0.35); color: {DEEP_BLUE};
    border-radius: 6px; padding: 0.25rem 0.65rem;
    font-size: 0.82rem; font-weight: 500; margin: 0.2rem;
}}

.edu-card {{
    background: {WHITE}; border-radius: 10px;
    padding: 1rem 1.3rem; border: 1px solid #DDE3EB; margin-bottom: 0.8rem;
}}
.edu-degree {{ font-family:'Space Grotesk',sans-serif; font-weight:600; font-size:0.95rem; color:{DEEP_BLUE}; }}
.edu-school {{ font-size:0.82rem; color:{TEAL}; font-weight:500; margin:0.15rem 0; }}
.edu-year   {{ font-size:0.78rem; color:{TEXT_MID}; }}

/* flip cards */
.flip-front {{
    background: {WHITE}; border-radius: 14px;
    padding: 1.2rem 1rem 0.8rem; text-align: center;
    box-shadow: 0 2px 16px rgba(31,58,95,0.09);
    border: 2px solid #DDE3EB;
}}
.flip-back {{
    background: {WHITE}; border-radius: 14px;
    padding: 1.2rem 1.4rem;
    box-shadow: 0 2px 16px rgba(31,58,95,0.09);
    border: 2px solid {TEAL};
}}
.fc-company {{
    font-family:'Space Grotesk',sans-serif; font-weight:700;
    font-size:1rem; color:{DEEP_BLUE}; margin-top:0.6rem; line-height:1.3;
}}
.fc-role  {{ font-size:0.82rem; font-weight:600; color:{TEAL}; margin:0.25rem 0; }}
.fc-meta  {{ font-size:0.79rem; color:{TEXT_MID}; margin:0.12rem 0; }}
.fc-hint  {{ font-size:0.72rem; color:{TEAL}; font-weight:600; letter-spacing:0.05em; margin-top:0.8rem; }}
.back-company {{ font-family:'Space Grotesk',sans-serif; font-weight:700; font-size:0.98rem; color:{DEEP_BLUE}; }}
.back-role {{ font-size:0.82rem; font-weight:600; color:{TEAL}; margin:0.1rem 0 0.4rem; }}
.back-sub  {{ font-size:0.76rem; color:{TEXT_MID}; font-style:italic; margin-bottom:0.5rem; }}
.back-bullets {{ padding-left:1.1rem; margin:0; }}
.back-bullets li {{ font-size:0.84rem; color:#334155; margin-bottom:0.3rem; line-height:1.5; }}

.proj-card {{
    border-left:3px solid {DEEP_BLUE}; padding:1rem 1.3rem;
    background:{WHITE}; border-radius:0 10px 10px 0; margin-bottom:1rem;
    box-shadow:0 1px 8px rgba(31,58,95,0.06);
}}
.ach-item {{
    display:flex; align-items:flex-start; gap:0.8rem;
    background:{WHITE}; border-radius:10px;
    padding:0.85rem 1.1rem; margin-bottom:0.7rem;
    border:1px solid #DDE3EB; box-shadow:0 1px 4px rgba(31,58,95,0.04);
}}
.ach-icon  {{ font-size:1.4rem; line-height:1; }}
.ach-label {{ font-size:0.72rem; font-weight:600; color:{TEAL}; text-transform:uppercase; letter-spacing:0.07em; margin-bottom:0.1rem; }}
.ach-text  {{ font-size:0.9rem; color:{TEXT_DARK}; line-height:1.5; }}

hr.custom {{ border:none; border-top:1px solid #DDE3EB; margin:1.5rem 0; }}

/* logo boxes (used with st.image) */
div[data-testid="stImage"] img {{
    border-radius: 8px;
}}

/* round portrait specifically */
.round-photo div[data-testid="stImage"] img {{
    border-radius: 50% !important;
    border: 4px solid {TEAL} !important;
    box-shadow: 0 4px 24px rgba(44,177,188,0.28) !important;
}}

.stDownloadButton > button {{
    background:{DEEP_BLUE} !important; color:white !important;
    border:none !important; border-radius:8px !important;
    font-family:'Space Grotesk',sans-serif !important;
    font-weight:600 !important; font-size:0.85rem !important;
    padding:0.5rem 1.3rem !important;
}}
</style>
""", unsafe_allow_html=True)

# ── Helpers ───────────────────────────────────────────────────────────────────
def load_image_safe(path_or_url, is_url=False):
    """Return PIL Image or None — never raises."""
    try:
        if is_url:
            r = requests.get(path_or_url, timeout=5)
            return Image.open(BytesIO(r.content)).convert("RGBA")
        else:
            return Image.open(path_or_url)
    except Exception:
        return None

def round_image(img, size=220):
    """Crop PIL image to a circle."""
    from PIL import ImageDraw
    img = img.convert("RGBA").resize((size, size), Image.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)
    result = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    result.paste(img, (0, 0), mask)
    return result

def radar_chart(categories, values):
    cats = categories + [categories[0]]
    vals = values + [values[0]]
    fig = go.Figure(go.Scatterpolar(
        r=vals, theta=cats, fill="toself",
        fillcolor="rgba(44,177,188,0.15)",
        line=dict(color=TEAL, width=2.5),
        marker=dict(size=7, color=TEAL),
    ))
    fig.update_layout(
        polar=dict(
            bgcolor=WHITE,
            angularaxis=dict(tickfont=dict(size=11, family="Inter", color=TEXT_DARK)),
            radialaxis=dict(visible=True, range=[0, 100],
                            tickfont=dict(size=9, color=TEXT_MID),
                            gridcolor="#DDE3EB"),
        ),
        showlegend=False, paper_bgcolor=WHITE,
        margin=dict(l=55, r=55, t=45, b=45),
        height=360, font=dict(family="Inter"),
    )
    return fig

def show_logo(url, width=64, fallback_text=""):
    """Try st.image with URL; fall back to styled text badge."""
    try:
        st.image(url, width=width)
    except Exception:
        st.markdown(
            f'<div style="width:{width}px;height:{width}px;display:flex;align-items:center;'
            f'justify-content:center;background:{LIGHT_GRAY};border:1px solid #DDE3EB;'
            f'border-radius:8px;font-family:Space Grotesk,sans-serif;font-weight:700;'
            f'font-size:0.85rem;color:{DEEP_BLUE};">{fallback_text}</div>',
            unsafe_allow_html=True,
        )

# ── Logo URLs — Google Favicon (always works, server-side) ────────────────────
BMO_LOGO     = "https://www.google.com/s2/favicons?domain=bmo.com&sz=128"
ROTMAN_LOGO  = "https://www.google.com/s2/favicons?domain=rotman.utoronto.ca&sz=128"
UOTTAWA_LOGO = "https://www.google.com/s2/favicons?domain=uottawa.ca&sz=128"

# ── Session state ─────────────────────────────────────────────────────────────
if "radar_domain" not in st.session_state:
    st.session_state.radar_domain = "General"
for key in ["flip_bmo", "flip_citic", "flip_zevno"]:
    if key not in st.session_state:
        st.session_state[key] = False

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style='text-align:center;margin-bottom:2rem;'>
        <div style='font-family:Space Grotesk,sans-serif;font-size:1.1rem;font-weight:700;color:white;'>Jeff Zhou</div>
        <div style='font-size:0.75rem;color:{TEAL};margin-top:0.2rem;'>MMA Candidate · Rotman</div>
    </div>""", unsafe_allow_html=True)

    page = st.radio("", options=[
        "🏠  About Me",
        "🎓  Education & Skills",
        "💼  Experience & Projects",
        "🌟  Additional",
    ], label_visibility="collapsed")

    st.markdown("<div style='height:3rem'></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size:0.7rem;color:#64748B;text-align:center;'>Built with Streamlit · 2025</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — ABOUT ME
# ══════════════════════════════════════════════════════════════════════════════
if "🏠  About Me" in page:

    col_info, col_portrait = st.columns([3, 1], gap="large")

    with col_portrait:
        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
        portrait = load_image_safe("headshot.jpeg")
        if portrait:
            circ = round_image(portrait, size=220)
            st.image(circ, use_container_width=False, width=220)
        else:
            st.markdown(
                f'<div style="width:210px;height:210px;border-radius:50%;background:{LIGHT_GRAY};'
                f'border:4px solid {TEAL};display:flex;align-items:center;justify-content:center;'
                f'font-size:3.5rem;margin:auto;">👤</div>',
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
            f'<a href="https://www.linkedin.com/in/rotman-mma/" target="_blank" style="text-decoration:none;">'
            f'<span class="pill" style="border-color:{TEAL};color:{TEAL};">🔗 LinkedIn</span></a>'
            '</div>',
            unsafe_allow_html=True,
        )

    st.markdown("<hr class='custom'>", unsafe_allow_html=True)

    # Metrics
    st.markdown('<div class="sec-title">Impact at a Glance</div>', unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    m1.markdown('<div class="metric-box"><div class="metric-val">$280M</div><div class="metric-lab">Project Analyzed at CITIC</div></div>', unsafe_allow_html=True)
    m2.markdown('<div class="metric-box"><div class="metric-val">5M+</div><div class="metric-lab">Customers Modeled at BMO</div></div>', unsafe_allow_html=True)
    m3.markdown('<div class="metric-box"><div class="metric-val">+9%</div><div class="metric-lab">Prediction Accuracy Gain</div></div>', unsafe_allow_html=True)
    m4.markdown('<div class="metric-box"><div class="metric-val">+15%</div><div class="metric-lab">Analysis Speed Increase</div></div>', unsafe_allow_html=True)

    st.markdown("<hr class='custom'>", unsafe_allow_html=True)
    st.markdown('<div class="sec-title">Skill Profile — Select a Domain</div>', unsafe_allow_html=True)

    RADAR_DATA = {
        "General": {
            "emoji": "🧠",
            "cats": ["Problem Solving", "Analytical Thinking", "Business Understanding", "Communication", "Learning Ability", "Project Execution"],
            "vals": [90, 95, 85, 70, 90, 80],
        },
        "Data Science": {
            "emoji": "📊",
            "cats": ["ML", "Python", "SQL", "R", "Power BI", "LLM"],
            "vals": [90, 90, 90, 60, 75, 60],
        },
        "Finance": {
            "emoji": "💹",
            "cats": ["Financial Modeling", "Valuation", "Portfolio Theory", "Financial Markets", "Risk Analysis", "Excel / Financial Tools"],
            "vals": [90, 85, 75, 80, 70, 70],
        },
    }

    rb1, rb2, rb3 = st.columns(3)
    for col, dom in zip([rb1, rb2, rb3], ["General", "Data Science", "Finance"]):
        with col:
            is_active = st.session_state.radar_domain == dom
            emoji = RADAR_DATA[dom]["emoji"]
            if st.button(
                f"{emoji}  {dom}",
                key=f"btn_{dom}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
            ):
                st.session_state.radar_domain = dom
                st.rerun()

    active = st.session_state.radar_domain
    d = RADAR_DATA[active]
    st.markdown(
        f'<div style="margin:0.8rem 0 0.2rem;font-family:Space Grotesk,sans-serif;font-weight:600;'
        f'font-size:1rem;color:{DEEP_BLUE};">{d["emoji"]} {active} Skills</div>',
        unsafe_allow_html=True,
    )

    col_radar, col_bars = st.columns([3, 2], gap="large")
    with col_radar:
        st.plotly_chart(radar_chart(d["cats"], d["vals"]), use_container_width=True)
    with col_bars:
        st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)
        for skill, score in sorted(zip(d["cats"], d["vals"]), key=lambda x: -x[1]):
            bar_color = TEAL if score >= 80 else ("#6B9FBF" if score >= 65 else "#94A3B8")
            st.markdown(f"""
            <div style='margin-bottom:0.7rem;'>
                <div style='display:flex;justify-content:space-between;margin-bottom:0.2rem;'>
                    <span style='font-size:0.83rem;font-weight:500;color:{TEXT_DARK};'>{skill}</span>
                    <span style='font-size:0.83rem;font-weight:700;color:{DEEP_BLUE};'>{score}</span>
                </div>
                <div style='background:#DDE3EB;border-radius:999px;height:7px;'>
                    <div style='background:{bar_color};width:{score}%;height:7px;border-radius:999px;'></div>
                </div>
            </div>""", unsafe_allow_html=True)

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
            "logo": ROTMAN_LOGO,
            "logo_fb": "UofT",
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
            "logo": UOTTAWA_LOGO,
            "logo_fb": "uOtt",
            "details": [],
        },
    ]

    for e in edu_data:
        details_html = "".join(
            f'<li style="font-size:0.85rem;color:{TEXT_MID};margin-bottom:0.2rem;">{d}</li>'
            for d in e["details"]
        )
        details_block = f'<ul style="padding-left:1.1rem;margin-top:0.6rem;">{details_html}</ul>' if e["details"] else ""

        c_logo, c_text = st.columns([1, 8], gap="small")
        with c_logo:
            st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
            try:
                st.image(e["logo"], width=52)
            except Exception:
                st.markdown(
                    f'<div style="width:52px;height:52px;display:flex;align-items:center;justify-content:center;'
                    f'background:{LIGHT_GRAY};border:1px solid #DDE3EB;border-radius:8px;font-size:0.7rem;'
                    f'font-weight:700;color:{DEEP_BLUE};">{e["logo_fb"]}</div>',
                    unsafe_allow_html=True,
                )
        with c_text:
            st.markdown(f"""
            <div class="edu-card" style="margin-bottom:0;">
                <div class="edu-degree">{e['degree']}</div>
                <div class="edu-school">{e['school']}</div>
                <div class="edu-year">📅 {e['year']}</div>
                {details_block}
            </div>""", unsafe_allow_html=True)
        st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)

    st.markdown("<hr class='custom'>", unsafe_allow_html=True)
    st.markdown('<div class="sec-title">Technical Skills</div>', unsafe_allow_html=True)

    skill_groups = {
        "💻 Programming Languages": ["Python", "SQL", "R"],
        "📊 Analytics & BI Tools": ["Power BI", "IBM SPSS Modeler", "SAS Enterprise Guide"],
        "🤖 Machine Learning": ["Supervised Learning", "Customer Segmentation", "SMOTE", "XGBoost", "Sklearn", "LLMs"],
        "📈 Financial Tools": ["Excel / Financial Modeling", "DCF Valuation", "Risk Analysis", "Portfolio Analysis"],
        "🛠️ Other Software": ["Microsoft Word", "PowerPoint"],
    }
    for group, skills in skill_groups.items():
        st.markdown(f'<div style="font-family:Space Grotesk,sans-serif;font-weight:600;font-size:0.9rem;color:{DEEP_BLUE};margin:1rem 0 0.5rem;">{group}</div>', unsafe_allow_html=True)
        tags = " ".join(f'<span class="skill-tag">{s}</span>' for s in skills)
        st.markdown(f'<div style="line-height:2.4;">{tags}</div>', unsafe_allow_html=True)

    st.markdown("<hr class='custom'>", unsafe_allow_html=True)
    st.markdown('<div class="sec-title">Languages</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    c1.markdown(f'<div class="metric-box" style="text-align:left;padding:1rem 1.2rem;"><div style="font-size:1.4rem;margin-bottom:0.3rem;">🇺🇸</div><div style="font-family:Space Grotesk,sans-serif;font-weight:600;color:{DEEP_BLUE};">English</div><div style="font-size:0.8rem;color:{TEAL};font-weight:500;">Fluent</div></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="metric-box" style="text-align:left;padding:1rem 1.2rem;"><div style="font-size:1.4rem;margin-bottom:0.3rem;">🇨🇳</div><div style="font-family:Space Grotesk,sans-serif;font-weight:600;color:{DEEP_BLUE};">Mandarin</div><div style="font-size:0.8rem;color:{TEAL};font-weight:500;">Fluent (Native)</div></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — EXPERIENCE & PROJECTS
# ══════════════════════════════════════════════════════════════════════════════
elif "💼  Experience & Projects" in page:
    st.markdown('<div class="sec-title">Professional Experience</div>', unsafe_allow_html=True)
    st.markdown(f'<p style="font-size:0.88rem;color:{TEXT_MID};margin-bottom:1.2rem;">Click any card to reveal details.</p>', unsafe_allow_html=True)

    EXPERIENCE = [
        {
            "key":      "flip_bmo",
            "company":  "Bank of Montreal (BMO)",
            "role":     "Marketing Data Analyst Intern",
            "location": "Toronto, Canada",
            "period":   "Jan 2026 – Present",
            "logo":     BMO_LOGO,
            "logo_fb":  "BMO",
            "sub":      "One of Canada's largest banks",
            "bullets": [
                "Developed predictive models to estimate 12-month revenue across a 5M+ U.S. customer base.",
                "Built customer segmentation models to improve targeting precision for marketing campaigns.",
                "Analyzed profit drivers to support U.S. market expansion using advanced analytics.",
                "Designed randomized controlled trials (RCTs) to measure incremental lift.",
                "Contributed to a scalable campaign activation framework to improve marketing ROI.",
            ],
        },
        {
            "key":      "flip_citic",
            "company":  "China CITIC Financial Asset Management",
            "role":     "Financial Assistant Intern",
            "location": "Chengdu, China",
            "period":   "May 2024 – Aug 2024",
            "logo":     None,
            "logo_fb":  "CITIC",
            "sub":      "One of China's largest state-owned financial asset management institutions",
            "bullets": [
                "Conducted financial analysis for a financing project exceeding RMB 1.4B (CAD $280M).",
                "Developed risk management framework components for asset protection.",
                "Researched market and economic trends to identify investment opportunities.",
                "Built DCF and financial models in Excel to assess target companies' true value.",
            ],
        },
        {
            "key":      "flip_zevno",
            "company":  "Zevnodata Fintech",
            "role":     "Business Analyst Intern",
            "location": "Toronto, Canada",
            "period":   "May 2023 – Aug 2023",
            "logo":     None,
            "logo_fb":  "ZEV",
            "sub":      "AI/ML-powered full-spectrum data solutions company",
            "bullets": [
                "Consolidated 50,000+ records from Capital IQ, Statista, and internal reports — 15% faster analysis.",
                "Processed Lululemon's ~200k-row dataset using SMOTE, C5 tree, and KNN — +9% accuracy.",
                "Applied Python (matplotlib, seaborn, sklearn) to surface revenue growth opportunities.",
            ],
        },
    ]

    cols = st.columns(3, gap="medium")
    for col, e in zip(cols, EXPERIENCE):
        with col:
            flipped = st.session_state[e["key"]]

            if not flipped:
                # ── FRONT ────────────────────────────────────────────────────
                st.markdown('<div class="flip-front">', unsafe_allow_html=True)

                # Logo — use st.image centered in a column trick
                lc1, lc2, lc3 = st.columns([1, 2, 1])
                with lc2:
                    if e["logo"]:
                        try:
                            st.image(e["logo"], width=72)
                        except Exception:
                            st.markdown(
                                f'<div style="width:72px;height:72px;display:flex;align-items:center;'
                                f'justify-content:center;background:{LIGHT_GRAY};border:1px solid #DDE3EB;'
                                f'border-radius:10px;font-family:Space Grotesk,sans-serif;font-weight:700;'
                                f'font-size:1rem;color:{DEEP_BLUE};">{e["logo_fb"]}</div>',
                                unsafe_allow_html=True,
                            )
                    else:
                        st.markdown(
                            f'<div style="width:72px;height:72px;display:flex;align-items:center;'
                            f'justify-content:center;background:{DEEP_BLUE};border-radius:10px;'
                            f'font-family:Space Grotesk,sans-serif;font-weight:700;'
                            f'font-size:1rem;color:white;">{e["logo_fb"]}</div>',
                            unsafe_allow_html=True,
                        )

                st.markdown(f"""
                    <div class="fc-company">{e['company']}</div>
                    <div class="fc-role">{e['role']}</div>
                    <div class="fc-meta">📍 {e['location']}</div>
                    <div class="fc-meta">🗓 {e['period']}</div>
                    <div class="fc-hint">TAP FOR DETAILS ↓</div>
                </div>""", unsafe_allow_html=True)

                if st.button("See Details →", key=f"btn_{e['key']}", use_container_width=True):
                    st.session_state[e["key"]] = True
                    st.rerun()

            else:
                # ── BACK ─────────────────────────────────────────────────────
                bullets_html = "".join(f"<li>{b}</li>" for b in e["bullets"])
                st.markdown(f"""
                <div class="flip-back">
                    <div class="back-company">{e['company']}</div>
                    <div class="back-role">{e['role']} · {e['period']}</div>
                    <div class="back-sub">{e['sub']}</div>
                    <ul class="back-bullets">{bullets_html}</ul>
                </div>""", unsafe_allow_html=True)

                if st.button("← Back", key=f"back_{e['key']}", use_container_width=True):
                    st.session_state[e["key"]] = False
                    st.rerun()

    st.markdown("<hr class='custom'>", unsafe_allow_html=True)
    st.markdown('<div class="sec-title">Technical Projects</div>', unsafe_allow_html=True)

    PROJECTS = [
        {
            "title": "LLM-Powered Vacation Rental Recommender",
            "year":  "2025",
            "org":   "Rotman School of Management",
            "logo":  ROTMAN_LOGO,
            "logo_fb": "Rot",
            "stack": ["Python", "LLM", "NLP", "Data Pipelines", "Matching Algorithms"],
            "desc":  "Python-based CLI app recommending vacation rentals via user preferences, budget, and group size. Integrated an LLM for natural language query handling — inspired by Airbnb.",
        },
        {
            "title": "RBAC × Calian Ltd. Data Analytics Case",
            "year":  "2024",
            "org":   "Rotman Business Analytics Club — 🏆 2nd Place",
            "logo":  ROTMAN_LOGO,
            "logo_fb": "Rot",
            "stack": ["Python", "Power BI", "Data Analysis", "Strategy"],
            "desc":  "Real-world case competition sponsored by Calian Ltd. Developed data-driven insights and actionable strategy, placing 2nd among competing teams.",
        },
    ]

    for p in PROJECTS:
        tags = " ".join(f'<span class="skill-tag">{t}</span>' for t in p["stack"])
        pc1, pc2 = st.columns([1, 12], gap="small")
        with pc1:
            try:
                st.image(p["logo"], width=36)
            except Exception:
                st.markdown(
                    f'<div style="width:36px;height:36px;background:{LIGHT_GRAY};border:1px solid #DDE3EB;'
                    f'border-radius:6px;display:flex;align-items:center;justify-content:center;'
                    f'font-size:0.65rem;font-weight:700;color:{DEEP_BLUE};">{p["logo_fb"]}</div>',
                    unsafe_allow_html=True,
                )
        with pc2:
            st.markdown(f"""
            <div class="proj-card">
                <div style="font-family:Space Grotesk,sans-serif;font-weight:700;font-size:0.98rem;color:{DEEP_BLUE};">{p['title']}</div>
                <div style="font-size:0.8rem;color:{TEAL};font-weight:500;margin:0.1rem 0 0.4rem;">{p['org']} · 📅 {p['year']}</div>
                <p style="font-size:0.87rem;color:#334155;line-height:1.6;margin:0 0 0.5rem;">{p['desc']}</p>
                <div style="line-height:2.3;">{tags}</div>
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — ADDITIONAL
# ══════════════════════════════════════════════════════════════════════════════
elif "🌟  Additional" in page:
    st.markdown('<div class="sec-title">Additional Interests & Achievements</div>', unsafe_allow_html=True)

    items = [
        ("🏆", "Case Competition",  "2nd Place — RBAC × Calian Ltd. Data Analytics Case Competition, using Python and Power BI to deliver actionable data strategy."),
        ("🏸", "Athletics",         "3rd Place — BC High School Badminton Tournament as a key member of the school team."),
        ("♟️", "Chess",             "Ranked Top 7% worldwide in rapid games on chess.com — strategic thinking and pattern recognition."),
        ("🍡", "Entrepreneurship",  "Generated $4,000 in revenue by selling homemade Asian snacks — initiative, resourcefulness, business acumen."),
        ("🌐", "Languages",         "Fluent in both English and Mandarin, enabling cross-cultural collaboration in international environments."),
    ]
    for icon, label, text in items:
        st.markdown(f"""
        <div class="ach-item">
            <div class="ach-icon">{icon}</div>
            <div>
                <div class="ach-label">{label}</div>
                <div class="ach-text">{text}</div>
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<hr class='custom'>", unsafe_allow_html=True)
    st.markdown('<div class="sec-title">Connect</div>', unsafe_allow_html=True)

    resume_txt = """Jiefu (Jeff) Zhou
(613) 854-2788 | jeffintp.zhou@rotman.utoronto.ca
LinkedIn: https://www.linkedin.com/in/rotman-mma/

SKILLS: Python, SQL, R, Power BI, SAS, IBM SPSS Modeler, Excel

EDUCATION
MMA (Candidate) – Rotman, University of Toronto (2026)
HBCom Finance – University of Ottawa (2025)

EXPERIENCE
BMO · Marketing Data Analyst Intern · Jan 2026–Present
China CITIC · Financial Assistant Intern · May–Aug 2024
Zevnodata Fintech · Business Analyst Intern · May–Aug 2023

ACHIEVEMENTS
2nd Place – RBAC × Calian Case Competition
Top 9% worldwide in rapid chess (chess.com)
$4,000 revenue from homemade Asian snacks
Fluent: English & Mandarin
"""
    c1, c2, _ = st.columns([2, 2, 4])
    with c1:
        st.download_button("⬇ Download Resume", resume_txt, "jeff_zhou_resume.txt", "text/plain")
    with c2:
        st.link_button("🔗 LinkedIn", "https://www.linkedin.com/in/rotman-mma/")
