import streamlit as st

st.set_page_config(page_title="MOS Voting Hub", page_icon="📊", layout="wide")

# Password protection
if "password_correct" not in st.session_state:
    st.session_state.password_correct = False

if not st.session_state.password_correct:
    st.title("MOS Voting Hub - Mapped Out Solutions")
    password = st.text_input("Enter shared access password", type="password")
    if st.button("Unlock Application"):
        if password == st.secrets["APP_PASSWORD"]:
            st.session_state.password_correct = True
            st.rerun()
        else:
            st.error("Incorrect password")
    st.stop()

# Sidebar navigation
st.sidebar.title("Mapped Out Solutions")
st.sidebar.write("**MOS Voting Hub**")
st.sidebar.caption("Deciding the next application to build")

page = st.navigation({
    "Dashboard": st.Page("pages/1_dashboard.py", title="Live Leaderboard"),
    "Submit New Idea": st.Page("pages/2_submit_idea.py", title="Submit Idea"),
    "Vote on Ideas": st.Page("pages/3_vote.py", title="Vote"),
    "Idea Details": st.Page("pages/4_idea_details.py", title="View Details")
})

page.run()
