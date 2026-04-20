import streamlit as st
import pandas as pd
import plotly.express as px
from utils.db import fetch_ideas, fetch_votes

st.title("📊 Live Leaderboard - MOS Voting Hub")

ideas = fetch_ideas()
if not ideas:
    st.info("No ideas submitted yet. Use the Submit New Idea page to get started.")
    st.stop()

data = []
for idea in ideas:
    votes = fetch_votes(idea["id"])
    if votes:
        df_votes = pd.DataFrame(votes)
        avg_cost = df_votes["cost"].mean()
        avg_complexity = df_votes["complexity"].mean()
        avg_resourcing = df_votes["resourcing"].mean()
        avg_revenue = df_votes["revenue_potential"].mean()
        avg_fit = df_votes["strategic_fit"].mean()
        n_votes = len(df_votes)
        
        # Inverted scores for cost/complexity/resourcing
        score = ((5 - avg_cost) + (5 - avg_complexity) + (5 - avg_resourcing) + (avg_revenue * 2) + avg_fit) / 6
        data.append({
            "Idea": idea["name"],
            "Votes": n_votes,
            "Overall Score": round(score, 2),
            "Cost": round(avg_cost, 1),
            "Complexity": round(avg_complexity, 1),
            "Resourcing": round(avg_resourcing, 1),
            "Revenue Potential": round(avg_revenue, 1),
            "Strategic Fit": round(avg_fit, 1),
            "ID": idea["id"]
        })

if data:
    df = pd.DataFrame(data)
    df = df.sort_values("Overall Score", ascending=False)
    st.dataframe(df.drop(columns=["ID"]), use_container_width=True, hide_index=True)
    
    st.subheader("Visual Breakdown")
    fig = px.bar(df, x="Idea", y="Overall Score", color="Overall Score", color_continuous_scale="Viridis")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No votes cast yet.")