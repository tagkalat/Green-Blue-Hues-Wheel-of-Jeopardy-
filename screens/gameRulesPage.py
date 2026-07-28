import streamlit as st
import streamlit.components.v1 as components

from screens.basePage import BasePage


class GameRulesPage(BasePage):
    """
    Pure info page - shows the game rules. Reached ONLY via the title
    screen's Help button. Has a real sprite Back button that returns to
    the title screen. No path to actually start a game lives here
    anymore - that flow is: title Start -> playerNumberPage -> wheel.
    """

    FRAME_W, FRAME_H = 480, 270

    BACK_BOX = {
        "left_pct": 0.833, "top_pct": 0.370,
        "width_pct": 7.708, "height_pct": 12.963,
    }

    def __init__(self):
        super().__init__("gameRules")
        # player_count is already set directly into st.session_state by
        # PlayerNumberPage's render_nav_trigger_with_value() - nothing to
        # do here, just documenting where it comes from. Access it via:
        #   st.session_state.get("player_count")

    def render(self):
        a = self.assets

        self.render_nav_trigger("gamerules_back", "title")
        # NOTE: GameStartRules_0 and _1 both came back as identical
        # full-canvas frames (like the old title background), so we just
        # use frame 0 as a static image. Swap this for a real animation
        # later if frame 1 ever differs.
        rules_bg = a.get("GameStartRules_0")
        back_unpressed = a.get("GameStartBackbutton_0")
        back_pressed = a.get("GameStartBackbutton_1")

        FRAME_W, FRAME_H = self.FRAME_W, self.FRAME_H
        bb = self.BACK_BOX

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
                background-image: url('data:image/png;base64,{rules_bg}');
                background-size: 100% 100%;
                image-rendering: pixelated;
            }}
            #back-btn {{
                position: absolute;
                left: {bb["left_pct"]:.3f}%;
                top: {bb["top_pct"]:.3f}%;
                width: {bb["width_pct"]:.3f}%;
                height: {bb["height_pct"]:.3f}%;
                cursor: pointer;
                background-size: 100% 100%;
                image-rendering: pixelated;
                background-image: url('data:image/png;base64,{back_unpressed}');
            }}
        </style>

        <div id="stage-wrap">
            <div id="stage">
                <div id="bg-layer"></div>
                <div id="back-btn"></div>
            </div>
        </div>

        <script>
            const unpressedImg = "data:image/png;base64,{back_unpressed}";
            const pressedImg = "data:image/png;base64,{back_pressed}";
            const btn = document.getElementById("back-btn");
            let isPressed = false;

            {self.nav_trigger_js("gamerules_back")}

            btn.addEventListener("pointerdown", (e) => {{
                isPressed = true;
                btn.style.backgroundImage = "url('" + pressedImg + "')";
                btn.setPointerCapture(e.pointerId);
            }});
            btn.addEventListener("pointerup", () => {{
                if (!isPressed) return;
                isPressed = false;
                btn.style.backgroundImage = "url('" + unpressedImg + "')";
                triggerNav_gamerules_back();
            }});
            btn.addEventListener("pointerleave", () => {{
                if (!isPressed) return;
                isPressed = false;
                btn.style.backgroundImage = "url('" + unpressedImg + "')";
            }});
            btn.addEventListener("pointercancel", () => {{
                isPressed = false;
                btn.style.backgroundImage = "url('" + unpressedImg + "')";
            }});
            window.addEventListener("pageshow", () => {{
                btn.style.backgroundImage = "url('" + unpressedImg + "')";
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
