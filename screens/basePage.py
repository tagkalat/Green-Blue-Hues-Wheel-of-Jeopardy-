import streamlit as st

from assets.AssetManager import AssetManager
# Adjust the import above to match your actual project structure, e.g.:
#   from assets.AssetManager import AssetManager


class BasePage:
    STAGE_MAX_WIDTH_CSS = "1280px"

    @staticmethod
    def fit_to_window_js(frame_w: int, frame_h: int) -> str:
        """
        Returns a JS snippet that shrinks #stage-wrap's max-width so the
        stage's calculated height never exceeds the ACTUAL browser
        window's visible height (measured via window.parent.innerHeight,
        which works because components.html's iframe is same-origin).

        Call this once from each page's <script> block:
            {self.fit_to_window_js(FRAME_W, FRAME_H)}
        and it defines a fitToWindow() function - call fitToWindow() at
        the same points you already call resizeFrame().
        """
        aspect = frame_w / frame_h
        return f"""
        function fitToWindow() {{
            const stageWrap = document.getElementById("stage-wrap");
            if (!stageWrap || !window.parent) return;

            // 130px buffer accounts for Streamlit's own header bar and
            // page padding above/below the component. Adjust if your
            // layout has more/less surrounding chrome.
            const availableHeight = window.parent.innerHeight - 130;
            const availableWidth = window.parent.innerWidth * 0.95;

            const maxWidthFromHeight = availableHeight * {aspect};
            const finalMax = Math.min(1280, availableWidth, maxWidthFromHeight);

            stageWrap.style.maxWidth = finalMax + "px";
        }}
        // Recalculate whenever the actual browser window resizes, not
        // just the iframe (they're different windows).
        window.parent.addEventListener("resize", fitToWindow);
        """
    def __init__(self, assets_subfolder: str):
        self.assets = AssetManager(assets_subfolder)
        # Will be None until app.py has run its wiring step and stored
        # a controller in session_state — see app.py for that setup.
        self.controller = st.session_state.get("controller")

    def render(self):
        """
        Subclasses MUST override this — it's what actually draws the
        page's UI (HTML components, Streamlit widgets, etc.).
        """
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement its own render() method"
        )