import streamlit as st
import pandas as pd
from datetime import date
from db import init_db, add_market_rate, get_market_rates
from ui import inject_css, page_header

st.set_page_config(page_title="Market Rates", page_icon="💰", layout="wide")
inject_css(); init_db()
page_header("Location-wise Market Rates", "Store material prices with location, source, effective date and verification status.")

with st.form("rate_form"):
    c1,c2 = st.columns(2)
    material = c1.text_input("Material", placeholder="e.g. Cement")
    location = c2.text_input("Location", placeholder="e.g. Chattogram")
    c3,c4 = st.columns(2)
    unit = c3.text_input("Unit", value="bag")
    rate = c4.number_input("Rate (BDT)", min_value=0.0, step=1.0)
    source = st.text_input("Source", value="User entered", placeholder="Supplier quotation / market survey / schedule")
    effective = st.date_input("Effective date", value=date.today())
    verified = st.checkbox("Verified")
    if st.form_submit_button("➕ Add market rate", type="primary"):
        if material.strip() and location.strip() and rate > 0:
            add_market_rate(material.strip(), location.strip(), unit.strip(), rate, source.strip(), effective.isoformat(), verified)
            st.success("Market rate saved.")
            st.rerun()
        else:
            st.error("Material, location and a positive rate are required.")

st.divider()
location_filter = st.text_input("Filter by location", placeholder="e.g. Chattogram")
rates = get_market_rates(location_filter.strip() or None)

if rates:
    df = pd.DataFrame(rates)
    df["status"] = df["verified"].map({1: "Verified", 0: "Unverified"})
    st.dataframe(
        df[["material","location","unit","rate","source","effective_date","status"]],
        use_container_width=True,
        hide_index=True,
    )
else:
    st.info("No rates found. Add the first location-wise rate above.")
