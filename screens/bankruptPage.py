import streamlit as st
import streamlit.components.v1 as components

from screens.basePage import BasePage


class BankruptPage(BasePage):
    """
    Shown when the wheel lands on "Bankruptcy". Resets the current
    player's points to 0, then returns to the wheel on click-anywhere.
    """

    FRAME_W, FRAME_H = 480, 270

    def __init__(self):
        super().__init__("BankruptPage")

    def render(self):
        a = self.assets

        self.render_nav_trigger("bankrupt_continue", "wheel")

        st.session_state["current_points"] = 0
        # TODO: hand off to backend (e.g. self.controller.apply_bankruptcy())
        # once player_score_service is wired up.

        bg = a.get("PageBankrupt_0")
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
            {self.nav_trigger_js("bankrupt_continue")}
            document.getElementById("click-anywhere").addEventListener("click", () => {{
                triggerNav_bankrupt_continue();
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