import streamlit as st
from db import init_db, get_projects, get_project, get_ai_messages, save_ai_message, get_takeoff, get_market_rates
from ai_assistant import ask_claude
from ui import inject_css, page_header

st.set_page_config(page_title="AI Assistant", page_icon="🤖", layout="wide")
inject_css(); init_db()
page_header("AI Assistant", "Ask about quantities, BOQ structure, rate sources and estimation logic.")

projects = get_projects()
if not projects:
    st.warning("Create a project first.")
    st.stop()

selected = st.selectbox("Project context", [p["name"] for p in projects])
project = next(p for p in projects if p["name"] == selected)

history = get_ai_messages(project["id"])
for m in history:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

prompt = st.chat_input("e.g. Explain my current BOQ and identify missing rate inputs.")
if prompt:
    save_ai_message(project["id"], "user", prompt)
    context = {
        "project": project,
        "takeoff": get_takeoff(project["id"]),
        "market_rates": get_market_rates(project["location"]),
    }
    messages = [{"role": m["role"], "content": m["content"]} for m in history]
    messages.append({"role": "user", "content": prompt})
    answer = ask_claude(messages, project_context=str(context))
    save_ai_message(project["id"], "assistant", answer)
    st.rerun()

st.caption("AI outputs are preliminary. Do not use unverified AI quantities or rates directly for construction, tendering or contractual decisions.")
