import streamlit as st

from screens.basePage import BasePage


class GameRulesPage(BasePage):
    """Placeholder page — replace render() with the real designed UI later."""

    def __init__(self):
        super().__init__("gameRules")  # -> assets/gameRules/

    def render(self):
        st.title("Game Rules")
        st.write("TODO: build the real pixel-art rules page here.")

        if st.button("⬅ Back to title"):
            st.query_params["page"] = "title"
            st.rerun()
