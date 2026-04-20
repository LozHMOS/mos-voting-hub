import streamlit as st
from utils.db import fetch_ideas, fetch_votes

st.title("🔍 Idea Details & Comments")

ideas = fetch_ideas()
idea_options = {idea["name"]: idea for idea in ideas}
selected_name = st.selectbox("Select an idea", options=list(idea_options.keys()))
idea = idea_options[selected_name]

st.subheader(idea["name"])
st.write(idea["description"])
if idea["demo_link"]:
    st.markdown(f"[View Demo]({idea['demo_link']})")

st.markdown("### Full Readme / Information")
st.markdown(idea.get("readme_content", "No content uploaded") or "No content uploaded")

votes = fetch_votes(idea["id"])
if votes:
    st.subheader("Scores from team")
    df = pd.DataFrame(votes)
    st.dataframe(df[["voter_name", "cost", "complexity", "resourcing", "revenue_potential", "strategic_fit", "comment"]], use_container_width=True)
else:
    st.info("No votes yet.")