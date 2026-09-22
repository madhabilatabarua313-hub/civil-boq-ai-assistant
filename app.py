import streamlit as st
from db import init_db, get_projects, create_project, get_project, save_project
from calculations import calculate_item, DEFAULT_ITEMS
from ai_assistant import ask_claude
from ui import inject_css, page_header, metric_card

st.set_page_config(
    page_title="Civil BOQ AI",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()
init_db()

if "active_project_id" not in st.session_state:
    st.session_state.active_project_id = None
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.markdown("## 🏗️ Civil BOQ AI")
    st.caption("Estimation • BOQ • Market Rates • AI")

    st.divider()
    st.markdown("### Navigation")
    st.page_link("pages/1_📐_Quantity_Takeoff.py", label="Quantity Takeoff", icon="📐")
    st.page_link("pages/2_📋_BOQ.py", label="BOQ", icon="📋")
    st.page_link("pages/3_💰_Market_Rates.py", label="Market Rates", icon="💰")
    st.page_link("pages/4_🤖_AI_Assistant.py", label="AI Assistant", icon="🤖")
    st.page_link("pages/5_⭐_Reviews.py", label="Reviews & Feedback", icon="⭐")

    st.divider()
    st.markdown("### Active project")
    projects = get_projects()
    project_names = ["— Select project —"] + [p["name"] for p in projects]
    selected = st.selectbox("Project", project_names, label_visibility="collapsed")

    if selected != "— Select project —":
        match = next(p for p in projects if p["name"] == selected)
        st.session_state.active_project_id = match["id"]
        st.caption(f"📍 {match['location']}")

page_header(
    "Civil BOQ AI",
    "A clean, persistent workspace for civil quantity takeoff, BOQ estimation and market-rate analysis.",
)

projects = get_projects()

if not projects:
    st.info("No project yet. Create your first project below.")
else:
    cols = st.columns(4)
    cols[0].metric("Projects", len(projects))
    cols[1].metric("Active project", "Selected" if st.session_state.active_project_id else "None")
    cols[2].metric("Modules", "5")
    cols[3].metric("Data storage", "Persistent")

st.divider()

left, right = st.columns([1.15, 1], gap="large")

with left:
    st.subheader("Create a new project")
    with st.form("create_project_form", clear_on_submit=True):
        name = st.text_input("Project name", placeholder="e.g. 4-Storey Commercial Building")
        location = st.text_input("Project location", placeholder="e.g. Chattogram")
        project_type = st.selectbox(
            "Project type",
            ["Residential", "Commercial", "Institutional", "Industrial", "Road", "Water Supply", "Other"],
        )
        area = st.number_input("Approx. floor area (sqft)", min_value=0.0, step=100.0)
        floors = st.number_input("Number of floors", min_value=0, step=1)
        submitted = st.form_submit_button("➕ Create Project", use_container_width=True)

        if submitted:
            if not name.strip():
                st.error("Project name is required.")
            else:
                pid = create_project(
                    name=name.strip(),
                    location=location.strip() or "Not specified",
                    project_type=project_type,
                    floor_area=area,
                    floors=int(floors),
                )
                st.session_state.active_project_id = pid
                st.success("Project created and saved.")
                st.rerun()

with right:
    st.subheader("Recent projects")
    if projects:
        for p in projects[:8]:
            with st.container(border=True):
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.markdown(f"**{p['name']}**")
                    st.caption(f"📍 {p['location']} • {p['project_type']} • {p['floors']} floors")
                with c2:
                    if st.button("Open", key=f"open_{p['id']}", use_container_width=True):
                        st.session_state.active_project_id = p["id"]
                        st.rerun()
    else:
        st.caption("Your saved projects will appear here.")

st.divider()

st.subheader("Quick start")
q1, q2, q3, q4 = st.columns(4)
q1.markdown("### 📐\nQuantity\nTakeoff")
q2.markdown("### 📋\nBuild\nBOQ")
q3.markdown("### 💰\nAdd local\nMarket Rates")
q4.markdown("### 🤖\nAsk the\nAI Assistant")

st.caption("Important: AI suggestions are preliminary. Engineering quantities and rates should be reviewed by a qualified professional before tendering, procurement or construction.")
