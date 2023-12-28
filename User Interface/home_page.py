import streamlit as st

def app ():
    st.title("Welcome to the Movie Recommendation System")
    st.write("To receive personalized movie recommendations, choose an option from the sidebar:")

    st.markdown("- If you are a new user, select 'New User' :new:")
    st.markdown("- If you are an existing user, select 'Existing User' :bust_in_silhouette:")
