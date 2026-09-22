import streamlit as st
import pandas as pd
from db import init_db, get_projects, get_takeoff, get_market_rates
from ui import inject_css, page_header

st.set_page_config(page_title="BOQ", page_icon="📋", layout="wide")
inject_css(); init_db()
page_header("BOQ", "Turn saved quantities and location-wise rates into a transparent estimate.")

projects = get_projects()
if not projects:
    st.warning("Create a project first.")
    st.stop()

selected = st.selectbox("Project", [p["name"] for p in projects])
project = next(p for p in projects if p["name"] == selected)

items = get_takeoff(project["id"])
rates = get_market_rates(project["location"])

rate_map = {}
for r in rates:
    rate_map.setdefault(r["material"].lower(), r)

rows = []
for x in items:
    rate = x["rate"]
    # Exact description match where available; otherwise keep 0 for user entry.
    candidate = rate_map.get(x["description"].lower())
    if candidate:
        rate = candidate["rate"]
    rows.append({
        "Code": x["item_code"],
        "Description": x["description"],
        "Unit": x["unit"],
        "Quantity": round(x["quantity"], 3),
        "Rate": rate,
        "Amount": round(x["quantity"] * rate, 2),
    })

if not rows:
    st.info("Add quantities from the Quantity Takeoff page.")
    st.stop()

df = pd.DataFrame(rows)
st.dataframe(df, use_container_width=True, hide_index=True)

total = float(df["Amount"].sum())
c1,c2,c3 = st.columns(3)
c1.metric("BOQ Items", len(df))
c2.metric("Direct Cost", f"৳ {total:,.2f}")
c3.metric("Project Location", project["location"])

st.subheader("Cost adjustments")
overhead = st.number_input("Overhead (%)", min_value=0.0, value=0.0, step=0.5)
profit = st.number_input("Profit (%)", min_value=0.0, value=0.0, step=0.5)
contingency = st.number_input("Contingency (%)", min_value=0.0, value=0.0, step=0.5)

final_total = total * (1 + (overhead + profit + contingency) / 100)
st.success(f"Estimated total: **৳ {final_total:,.2f}**")

st.download_button(
    "⬇️ Download BOQ CSV",
    df.to_csv(index=False).encode("utf-8"),
    file_name=f"{project['name'].replace(' ','_')}_BOQ.csv",
    mime="text/csv",
)
