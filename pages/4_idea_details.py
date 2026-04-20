import streamlit as st
import pandas as pd
from utils.db import fetch_ideas, fetch_votes

st.title("🔍 Idea Details & Comments")

ideas = fetch_ideas()
if not ideas:
    st.info("No ideas submitted yet.")
    st.stop()

idea_options = {idea["name"]: idea for idea in ideas}
selected_name = st.selectbox("Select an idea", options=list(idea_options.keys()))
idea = idea_options[selected_name]

st.subheader(idea["name"])
st.write(idea["description"])
if idea.get("demo_link"):
    st.markdown(f"[View Demo]({idea['demo_link']})")

st.markdown("### Full Readme / Information")
st.markdown(idea.get("readme_content", "No content uploaded") or "No content uploaded")

votes = fetch_votes(idea["id"])
if votes:
    st.subheader("Scores from team")
    df = pd.DataFrame(votes)
    # Show only the columns we care about
    display_cols = ["voter_name", "cost", "complexity", "resourcing", "revenue_potential", "strategic_fit", "comment"]
    st.dataframe(df[display_cols], use_container_width=True)
else:
    st.info("No votes yet for this idea.")
