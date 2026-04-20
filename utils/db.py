import streamlit as st
from supabase import create_client, Client
from typing import Optional

@st.cache_resource
def get_supabase_client() -> Client:
    url: str = st.secrets["SUPABASE_URL"]
    key: str = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

def fetch_ideas():
    client = get_supabase_client()
    response = client.table("ideas").select("*").order("submitted_at", desc=True).execute()
    return response.data

def fetch_votes(idea_id: str):
    client = get_supabase_client()
    response = client.table("votes").select("*").eq("idea_id", idea_id).execute()
    return response.data

def insert_idea(name: str, description: str, readme_content: str, demo_link: str, submitted_by: str):
    client = get_supabase_client()
    data = {
        "name": name,
        "description": description,
        "readme_content": readme_content,
        "demo_link": demo_link,
        "submitted_by": submitted_by
    }
    response = client.table("ideas").insert(data).execute()
    return response.data[0]["id"] if response.data else None

def insert_vote(idea_id: str, voter_name: str, cost: int, complexity: int, resourcing: int, revenue_potential: int, strategic_fit: int, comment: str):
    client = get_supabase_client()
    data = {
        "idea_id": idea_id,
        "voter_name": voter_name,
        "cost": cost,
        "complexity": complexity,
        "resourcing": resourcing,
        "revenue_potential": revenue_potential,
        "strategic_fit": strategic_fit,
        "comment": comment
    }
    client.table("votes").insert(data).execute()

def has_voted(idea_id: str, voter_name: str) -> bool:
    client = get_supabase_client()
    response = client.table("votes").select("id").eq("idea_id", idea_id).eq("voter_name", voter_name).execute()
    return len(response.data) > 0