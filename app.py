import streamlit as st

from db import init_db, get_projects
from ui import inject_css


# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="CivilBOQ AI Assistant",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------
# INITIALIZATION
# ---------------------------------------------------------
inject_css()
init_db()


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------
if "active_project_id" not in st.session_state:
    st.session_state.active_project_id = None

if "messages" not in st.session_state:
    st.session_state.messages = []


# ---------------------------------------------------------
# NAVIGATION
# ---------------------------------------------------------
pages = {
    "🏠 Workspace": [
        st.Page(
            "pages/0_🏠_Dashboard.py",
            title="Dashboard",
            icon="🏠",
            default=True,
        ),
    ],
    "📊 Estimation": [
      st.Page(
    "pages/1_Quantity_Takeoff.py",
    title="Quantity Takeoff",
    icon="📐",
)
       st.Page(
    "pages/2_BOQ.py",
    title="BOQ",
    icon="📋",
)

st.Page(
    "pages/3_Market_Rates.py",
    title="Market Rates",
    icon="💰",
)

st.Page(
    "pages/4_AI_Assistant.py",
    title="AI Assistant",
    icon="🤖",
)

st.Page(
    "pages/5_Reviews.py",
    title="Reviews",
    icon="⭐",
)
    ],
}


# ---------------------------------------------------------
# SIDEBAR — PROJECT SELECTOR
# ---------------------------------------------------------
with st.sidebar:

    st.markdown(
        """
        <div style="
            padding: 8px 0 14px 0;
        ">
            <div style="
                font-size: 1.35rem;
                font-weight: 700;
            ">
                🏗️ CivilBOQ AI
            </div>

            <div style="
                font-size: 0.82rem;
                opacity: 0.7;
                margin-top: 3px;
            ">
                Estimation • BOQ • AI
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    projects = get_projects()

    project_options = ["— Select project —"] + [
        p["name"] for p in projects
    ]

    current_project_name = "— Select project —"

    if st.session_state.active_project_id:
        current_project = next(
            (
                p
                for p in projects
                if p["id"] == st.session_state.active_project_id
            ),
            None,
        )

        if current_project:
            current_project_name = current_project["name"]

    selected_project = st.selectbox(
        "Active Project",
        project_options,
        index=(
            project_options.index(current_project_name)
            if current_project_name in project_options
            else 0
        ),
        key="global_project_selector",
    )

    if selected_project != "— Select project —":

        selected_project_data = next(
            p for p in projects
            if p["name"] == selected_project
        )

        st.session_state.active_project_id = selected_project_data["id"]

        st.caption(
            f"📍 {selected_project_data['location']}"
        )

    else:
        st.session_state.active_project_id = None

    st.divider()

    st.caption("CivilBOQ AI Assistant")
    st.caption("Persistent project workspace")


# ---------------------------------------------------------
# RUN SELECTED PAGE
# ---------------------------------------------------------
pg = st.navigation(pages, position="sidebar")

pg.run()
