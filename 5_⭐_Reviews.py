import streamlit as st
import statistics
from db import init_db, add_review, get_reviews
from ui import inject_css, page_header

st.set_page_config(page_title="Reviews", page_icon="⭐", layout="wide")
inject_css(); init_db()
page_header("Reviews & Feedback", "Public feedback helps improve the estimation workflow.")

reviews = get_reviews()
if reviews:
    avg = statistics.mean(r["rating"] for r in reviews)
    c1,c2 = st.columns(2)
    c1.metric("Public rating", f"{avg:.1f} / 5")
    c2.metric("Total reviews", len(reviews))
else:
    st.info("Be the first to review the app.")

st.subheader("Leave a public review")
with st.form("review_form", clear_on_submit=True):
    name = st.text_input("Display name")
    rating = st.select_slider("Rating", options=[1,2,3,4,5], value=5)
    comment = st.text_area("Your feedback", placeholder="What worked well? What should be improved?")
    if st.form_submit_button("Publish review", type="primary"):
        if not name.strip() or not comment.strip():
            st.error("Name and feedback are required.")
        else:
            add_review(name.strip(), rating, comment.strip())
            st.success("Your review is now public.")
            st.rerun()

st.divider()
st.subheader("Public reviews")
for r in reviews:
    stars = "★" * r["rating"] + "☆" * (5-r["rating"])
    with st.container(border=True):
        st.markdown(f"**{r['display_name']}**  {stars}")
        st.write(r["comment"])
        st.caption(r["created_at"])
