import streamlit as st

from db import (
    get_projects,
    create_project,
)
from ui import page_header


# ---------------------------------------------------------
# PAGE HEADER
# ---------------------------------------------------------
page_header(
    "CivilBOQ AI Assistant",
    "A clean workspace for civil quantity takeoff, BOQ estimation, "
    "market-rate analysis and AI-assisted project decisions.",
)


# ---------------------------------------------------------
# PROJECT DATA
# ---------------------------------------------------------
projects = get_projects()


# ---------------------------------------------------------
# SUMMARY METRICS
# ---------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Projects",
        len(projects),
    )

with col2:
    st.metric(
        "Active Project",
        "Selected"
        if st.session_state.get("active_project_id")
        else "None",
    )

with col3:
    st.metric(
        "Core Modules",
        "5",
    )

with col4:
    st.metric(
        "Data Storage",
        "Persistent",
    )


st.divider()


# ---------------------------------------------------------
# CREATE PROJECT
# ---------------------------------------------------------
left, right = st.columns(
    [1.15, 1],
    gap="large",
)


with left:

    st.subheader("Create a New Project")

    st.caption(
        "Start by creating a project. Your estimation data "
        "will be associated with the selected project."
    )

    with st.form(
        "create_project_form",
        clear_on_submit=True,
    ):

        name = st.text_input(
            "Project Name",
            placeholder="e.g. 4-Storey Commercial Building",
        )

        location = st.text_input(
            "Project Location",
            placeholder="e.g. Chattogram",
        )

        project_type = st.selectbox(
            "Project Type",
            [
                "Residential",
                "Commercial",
                "Institutional",
                "Industrial",
                "Road",
                "Water Supply",
                "Other",
            ],
        )

        area = st.number_input(
            "Approx. Floor Area (sqft)",
            min_value=0.0,
            step=100.0,
        )

        floors = st.number_input(
            "Number of Floors",
            min_value=0,
            step=1,
        )

        submitted = st.form_submit_button(
            "➕ Create Project",
            use_container_width=True,
        )

        if submitted:

            if not name.strip():

                st.error(
                    "Project name is required."
                )

            else:

                project_id = create_project(
                    name=name.strip(),
                    location=(
                        location.strip()
                        or "Not specified"
                    ),
                    project_type=project_type,
                    floor_area=area,
                    floors=int(floors),
                )

                st.session_state.active_project_id = (
                    project_id
                )

                st.success(
                    "Project created and saved successfully."
                )

                st.rerun()


# ---------------------------------------------------------
# RECENT PROJECTS
# ---------------------------------------------------------
with right:

    st.subheader("Recent Projects")

    if projects:

        for project in projects[:8]:

            with st.container(
                border=True
            ):

                st.markdown(
                    f"**{project['name']}**"
                )

                st.caption(
                    f"📍 {project['location']}  •  "
                    f"{project['project_type']}  •  "
                    f"{project['floors']} floors"
                )

                if st.button(
                    "Open Project",
                    key=f"open_{project['id']}",
                    use_container_width=True,
                ):

                    st.session_state.active_project_id = (
                        project["id"]
                    )

                    st.rerun()

    else:

        st.info(
            "No projects yet. Create your first project "
            "to begin quantity takeoff and BOQ estimation."
        )


# ---------------------------------------------------------
# QUICK START
# ---------------------------------------------------------
st.divider()

st.subheader("Quick Start")

q1, q2, q3, q4 = st.columns(4)

with q1:
    st.markdown("### 📐")
    st.markdown("**Quantity Takeoff**")
    st.caption(
        "Calculate excavation, concrete, masonry, "
        "plaster and other quantities."
    )

with q2:
    st.markdown("### 📋")
    st.markdown("**BOQ**")
    st.caption(
        "Convert quantities into structured BOQ items "
        "and project costs."
    )

with q3:
    st.markdown("### 💰")
    st.markdown("**Market Rates**")
    st.caption(
        "Maintain location-specific material and "
        "construction rates."
    )

with q4:
    st.markdown("### 🤖")
    st.markdown("**AI Assistant**")
    st.caption(
        "Ask questions about quantities, BOQ, rates "
        "and estimation assumptions."
    )


# ---------------------------------------------------------
# ENGINEERING NOTICE
# ---------------------------------------------------------
st.divider()

st.info(
    "Engineering note: AI-generated suggestions are preliminary. "
    "Quantities, rates, assumptions and final BOQ values should "
    "be reviewed by a qualified civil/structural professional "
    "before tendering, procurement or construction."
)
