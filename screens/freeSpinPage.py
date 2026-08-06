import streamlit as st
import streamlit.components.v1 as components

from screens.basePage import BasePage


class FreeSpinPage(BasePage):
    """
    Shown when the wheel lands on "Free Spin". Grants the current player
    a free spin token, then returns to the wheel on click-anywhere (no
    art exists for a "pressed" state since this is a full-canvas
    announcement image, not a literal button).
    """

    FRAME_W, FRAME_H = 480, 270

    def __init__(self):
        super().__init__("freeSpinPage")

    def render(self):
        a = self.assets

        self.render_nav_trigger("freespin_continue", "wheel")

        # Grant the token on every visit to this page. (This page has only
        # one interactive element - the click-anywhere hotspot - which
        # immediately navigates away, so render() naturally only runs
        # once per visit; no extra guard needed against double-granting.)
        st.session_state["free_spin_tokens"] = st.session_state.get("free_spin_tokens", 0) + 1
        # TODO: hand off to backend (e.g. self.controller.grant_free_spin())
        # once player_score_service is wired up.

        bg = a.get("FreeSpinPage_0")
        FRAME_W, FRAME_H = self.FRAME_W, self.FRAME_H

        html = f"""
        <style>
            html, body {{ margin: 0; padding: 0; }}
            #stage-wrap {{
                width: 100%;
                max-width: {self.STAGE_MAX_WIDTH_CSS};
                margin: 0 auto;
            }}
            #stage {{
                position: relative;
                width: 100%;
                aspect-ratio: {FRAME_W} / {FRAME_H};
                image-rendering: pixelated;
                overflow: hidden;
            }}
            #bg-layer {{
                position: absolute;
                inset: 0;
                background-image: url('data:image/png;base64,{bg}');
                background-size: 100% 100%;
                image-rendering: pixelated;
            }}
            #click-anywhere {{
                position: absolute;
                inset: 0;
                cursor: pointer;
            }}
        </style>

        <div id="stage-wrap">
            <div id="stage">
                <div id="bg-layer"></div>
                <div id="click-anywhere"></div>
            </div>
        </div>

        <script>
            {self.nav_trigger_js("freespin_continue")}
            document.getElementById("click-anywhere").addEventListener("click", () => {{
                triggerNav_freespin_continue();
            }});

            {self.fit_to_window_js(FRAME_W, FRAME_H)}

            function resizeFrame() {{
                const stage = document.getElementById("stage");
                if (window.frameElement) {{
                    window.frameElement.style.height = (stage.offsetHeight + 10) + "px";
                }}
            }}
            function fitAndResize() {{ fitToWindow(); resizeFrame(); }}
            window.addEventListener("resize", fitAndResize);
            window.addEventListener("load", fitAndResize);
            setTimeout(fitAndResize, 50);
            setTimeout(fitAndResize, 300);
        </script>
        """
        components.html(html, height=int(FRAME_H / FRAME_W * 700) + 20)