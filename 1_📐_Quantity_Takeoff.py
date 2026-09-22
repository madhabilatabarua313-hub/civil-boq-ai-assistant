import streamlit as st
from db import init_db, get_projects, add_takeoff, get_takeoff, delete_takeoff
from calculations import DEFAULT_ITEMS, calculate_item
from ui import inject_css, page_header

st.set_page_config(page_title="Quantity Takeoff", page_icon="📐", layout="wide")
inject_css(); init_db()
page_header("Quantity Takeoff", "Deterministic engineering calculators with persistent project storage.")

projects = get_projects()
if not projects:
    st.warning("Create a project from the Dashboard first.")
    st.stop()

project_names = [p["name"] for p in projects]
selected = st.selectbox("Project", project_names)
project = next(p for p in projects if p["name"] == selected)
pid = project["id"]

tab1, tab2 = st.tabs(["➕ Add calculation", "📋 Saved quantities"])

with tab1:
    item_code = st.selectbox(
        "Calculation type",
        list(DEFAULT_ITEMS.keys()),
        format_func=lambda x: f"{x} — {DEFAULT_ITEMS[x][0]}",
    )

    if item_code in {"EXC-001", "CON-001", "RCC-001"}:
        c1,c2,c3 = st.columns(3)
        L = c1.number_input("Length", min_value=0.0, step=0.1)
        W = c2.number_input("Width", min_value=0.0, step=0.1)
        D = c3.number_input("Depth / thickness", min_value=0.0, step=0.01)
        if st.button("Calculate", type="primary"):
            qty = calculate_item(item_code, length=L, width=W, depth=D)
            st.success(f"Quantity = **{qty:.3f} {DEFAULT_ITEMS[item_code][1]}**")
            if st.button("Save to project"):
                add_takeoff(pid, item_code, DEFAULT_ITEMS[item_code][0], DEFAULT_ITEMS[item_code][1], qty)
                st.success("Saved permanently.")
                st.rerun()

    elif item_code == "MASON-001":
        c1,c2,c3 = st.columns(3)
        L = c1.number_input("Length", min_value=0.0, step=0.1)
        H = c2.number_input("Height", min_value=0.0, step=0.1)
        T = c3.number_input("Thickness", min_value=0.0, step=0.01)
        if st.button("Calculate", type="primary"):
            qty = calculate_item(item_code, length=L, height=H, thickness=T)
            st.success(f"Quantity = **{qty:.3f} m³**")
            if st.button("Save to project"):
                add_takeoff(pid, item_code, DEFAULT_ITEMS[item_code][0], "m³", qty)
                st.rerun()

    elif item_code in {"PLS-001", "FLR-001"}:
        c1,c2 = st.columns(2)
        L = c1.number_input("Length", min_value=0.0, step=0.1)
        W = c2.number_input("Width", min_value=0.0, step=0.1)
        if st.button("Calculate", type="primary"):
            qty = calculate_item(item_code, length=L, width=W)
            st.success(f"Quantity = **{qty:.3f} m²**")
            if st.button("Save to project"):
                add_takeoff(pid, item_code, DEFAULT_ITEMS[item_code][0], "m²", qty)
                st.rerun()

    elif item_code == "FORM-001":
        area = st.number_input("Formwork area (m²)", min_value=0.0, step=0.1)
        if st.button("Calculate", type="primary"):
            qty = calculate_item(item_code, area=area)
            st.success(f"Quantity = **{qty:.3f} m²**")
            if st.button("Save to project"):
                add_takeoff(pid, item_code, DEFAULT_ITEMS[item_code][0], "m²", qty)
                st.rerun()

    elif item_code == "REBAR-001":
        c1,c2 = st.columns(2)
        dia = c1.number_input("Bar diameter (mm)", min_value=0.0, step=1.0)
        length = c2.number_input("Total bar length (m)", min_value=0.0, step=1.0)
        if st.button("Calculate", type="primary"):
            qty = calculate_item(item_code, diameter=dia, length=length)
            st.success(f"Approx. steel weight = **{qty:.3f} kg**")
            if st.button("Save to project"):
                add_takeoff(pid, item_code, DEFAULT_ITEMS[item_code][0], "kg", qty)
                st.rerun()

with tab2:
    items = get_takeoff(pid)
    if not items:
        st.info("No saved quantities yet.")
    else:
        for item in items:
            with st.container(border=True):
                c1,c2,c3 = st.columns([3,1,1])
                c1.markdown(f"**{item['description']}**")
                c1.caption(item["item_code"])
                c2.metric("Quantity", f"{item['quantity']:.3f} {item['unit']}")
                if c3.button("Delete", key=f"del_{item['id']}"):
                    delete_takeoff(item["id"]); st.rerun()
