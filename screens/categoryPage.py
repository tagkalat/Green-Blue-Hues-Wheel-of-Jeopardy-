import streamlit as st

from screens.basePage import BasePage


class CategoryPage(BasePage):
    """
    Placeholder - shows background, category name, current points, and
    all 5 question buttons statically (unpressed frame only). No click
    logic yet.
    """

    def __init__(self):
        super().__init__("CategoryPage")

    def render(self):
        self.render_static_scene([
            ("CategoryPageBackground_0", {"left_pct": 0, "top_pct": 0, "width_pct": 100, "height_pct": 100}),
            ("CategoryName_0", {"left_pct": 30.208, "top_pct": 1.852, "width_pct": 38.542, "height_pct": 26.667}),
            ("Q1Button_0", {"left_pct": 7.292, "top_pct": 32.593, "width_pct": 22.917, "height_pct": 26.667}),
            ("Q2Button_0", {"left_pct": 38.542, "top_pct": 32.593, "width_pct": 22.917, "height_pct": 26.667}),
            ("Q3Button_0", {"left_pct": 69.792, "top_pct": 32.593, "width_pct": 22.917, "height_pct": 26.667}),
            ("Q4Button_0", {"left_pct": 21.875, "top_pct": 61.481, "width_pct": 22.917, "height_pct": 26.667}),
            ("Q5Button_0", {"left_pct": 55.208, "top_pct": 61.481, "width_pct": 22.917, "height_pct": 26.667}),
            ("CategoryPageCurrentPoints_0", {"left_pct": 81.458, "top_pct": 79.630, "width_pct": 17.083, "height_pct": 16.667}),
        ])
        if st.button("⬅ Back to title", key="back_to_title_category"):
            st.query_params["page"] = "title"
            st.rerun()
