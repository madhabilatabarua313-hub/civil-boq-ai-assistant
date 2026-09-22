import streamlit as st

def inject_css():
    st.markdown("""
    <style>
    .block-container {max-width: 1200px; padding-top: 2rem; padding-bottom: 4rem;}
    h1, h2, h3 {letter-spacing: -0.02em;}
    .stButton > button {border-radius: 10px; font-weight: 600;}
    [data-testid="stMetric"] {
        border: 1px solid rgba(128,128,128,.20);
        padding: 14px;
        border-radius: 12px;
        background: rgba(128,128,128,.04);
    }
    .hero {
        padding: 24px 28px;
        border: 1px solid rgba(128,128,128,.18);
        border-radius: 16px;
        background: linear-gradient(135deg, rgba(64,100,255,.10), rgba(128,64,255,.06));
        margin-bottom: 20px;
    }
    .muted {color: #6b7280;}
    </style>
    """, unsafe_allow_html=True)

def page_header(title, subtitle=""):
    st.markdown(
        f'<div class="hero"><h1>{title}</h1><p class="muted">{subtitle}</p></div>',
        unsafe_allow_html=True,
    )

def metric_card(label, value):
    st.metric(label, value)
