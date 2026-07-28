import streamlit as st

from screens.basePage import BasePage


class WheelPage(BasePage):
    """Placeholder page — replace render() with the real designed UI later."""

    def init(self):
        super().init("wheelPage")  # -> assets/gameRules/

    def render(self):
        st.title("Wheel page")
        st.write("TODO: build the real pixel-art rules page here.")

        if st.button("⬅ Back to title"):
            st.query_params["page"] = "title"
            st.rerun()