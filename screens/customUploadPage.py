import streamlit as st

from screens.basePage import BasePage


class CustomUploadPage(BasePage):
    """Placeholder page — replace render() with the real designed UI later."""

    def __init__(self):
        super().__init__("customUploadpage")  # -> assets/customUploadpage/

    def render(self):
        st.title("Upload Custom Questions")
        st.write("TODO: build the real pixel-art upload page here.")

        if st.button("⬅ Back to title"):
            st.query_params["page"] = "title"
            st.rerun()
