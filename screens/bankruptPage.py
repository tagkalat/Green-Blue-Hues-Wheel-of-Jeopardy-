import streamlit as st

from screens.basePage import BasePage


class BankruptPage(BasePage):
    """Placeholder - single static full-canvas image. No interactivity yet."""

    def __init__(self):
        super().__init__("BankruptPage")

    def render(self):
        self.render_static_scene([
            ("PageBankrupt_0", {"left_pct": 0, "top_pct": 0, "width_pct": 100, "height_pct": 100}),
        ])
        if st.button("⬅ Back to title", key="back_to_title_bankrupt"):
            st.query_params["page"] = "title"
            st.rerun()
