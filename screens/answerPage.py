import streamlit as st

from screens.basePage import BasePage


class AnswerPage(BasePage):
    """
    Placeholder - shows background, the answer boxes, current points, and
    the free-spin prompt with its Yes/No buttons, all statically
    (unpressed frame only). No click logic yet.
    """

    def __init__(self):
        super().__init__("AnswerPage")

    def render(self):
        self.render_static_scene([
            ("AnswerPageBackground_0", {"left_pct": 0, "top_pct": 0, "width_pct": 100, "height_pct": 100}),
            ("AnswerPageAnswerSelectedBox_0", {"left_pct": 14.583, "top_pct": 0.0, "width_pct": 69.792, "height_pct": 30.741}),
            ("AnswerPageAnswerCorrectBox_0", {"left_pct": 16.667, "top_pct": 32.593, "width_pct": 65.625, "height_pct": 30.741}),
            ("AnswerPageCurrentPoints_0", {"left_pct": 81.458, "top_pct": 79.630, "width_pct": 17.083, "height_pct": 16.667}),
            ("AnswerPageFreeSpin_0", {"left_pct": 23.125, "top_pct": 64.815, "width_pct": 52.292, "height_pct": 16.667}),
            ("AnswerPageFreeSpinYesButton_0", {"left_pct": 37.5, "top_pct": 83.333, "width_pct": 7.708, "height_pct": 12.963}),
            ("AnswerPageFreeSpinNoButton_0", {"left_pct": 54.792, "top_pct": 83.333, "width_pct": 7.708, "height_pct": 12.963}),
        ])
        if st.button("⬅ Back to title", key="back_to_title_answer"):
            st.query_params["page"] = "title"
            st.rerun()
