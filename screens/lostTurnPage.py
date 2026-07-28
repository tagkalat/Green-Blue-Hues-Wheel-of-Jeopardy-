import streamlit as st

from screens.basePage import BasePage


class LostTurnPage(BasePage):
    """
    Placeholder - shows background, the "if free spin" text box, and both
    Yes/No buttons statically (unpressed frame only). No click logic yet.
    """

    def __init__(self):
        super().__init__("LostTurnPage")

    def render(self):
        self.render_static_scene([
            ("LostTurnPage_0", {"left_pct": 0, "top_pct": 0, "width_pct": 100, "height_pct": 100}),
            ("IfFreeSpin_0", {"left_pct": 15.625, "top_pct": 45.926, "width_pct": 68.75, "height_pct": 21.111}),
            ("YesButton_0", {"left_pct": 37.5, "top_pct": 71.852, "width_pct": 7.708, "height_pct": 12.963}),
            ("NoButton_0", {"left_pct": 54.792, "top_pct": 71.852, "width_pct": 7.708, "height_pct": 12.963}),
        ])
        if st.button("⬅ Back to title", key="back_to_title_lostturn"):
            st.query_params["page"] = "title"
            st.rerun()
