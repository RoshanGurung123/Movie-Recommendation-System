import streamlit as st
from streamlit_option_menu import option_menu
import existing_user, new_user, home_page, user_profile

st.set_page_config(
    page_title="Movie Reccommendation System",
    # page_icon="film"
)

class MultiApp:
    def __init__ (self):
        self.apps = []

    def add_app (self, title, function):
        self.apps.append({
            "title": title,
            "function": function
        })

    def run(self):
        with st.sidebar:
            app = option_menu(
                menu_title='Menu',
                options=['Home', 'New User', 'Existing User','User Profile'],
                icons=['house', 'person-add', 'person','person-circle'],
                menu_icon='list',
                default_index=0,
                styles={
                    "container": {"padding": "4!important", "background-color": 'black'},
                    "icon": {"color": "white", "font-size": "20px"},
                    "nav-link": {"color": "white", "font-size": "18px", "text-align": "left", "margin": "0px",
                                 "--hover-color": "orange"},
                    "nav-link-selected": {"background-color": "#02ab21"},
                    "menu-title":{"font-size":"24px", "margin-bottom":"5px"}}
            )
        if app == "Home":
            home_page.app()
        if app=="Existing User":
            existing_user.recommendation_existing_user()
        if app=="New User":
            new_user.content_based_recommend_movies()
        if app=="User Profile":
            user_profile.user_profile()

multi_app=MultiApp()
multi_app.run()