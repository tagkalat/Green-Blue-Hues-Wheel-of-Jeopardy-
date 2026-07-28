import streamlit as st
import streamlit.components.v1 as components

from screens.basePage import BasePage


class GameRulesPage(BasePage):
    """
    Shows the game rules. Has a real sprite Back button (returns to
    playerNumberPage). The "Start Game" action has no art yet, so it's a
    temporary native Streamlit button until that asset exists.
    """

    FRAME_W, FRAME_H = 480, 270

    BACK_BOX = {
        "left_pct": 0.833, "top_pct": 0.370,
        "width_pct": 7.708, "height_pct": 12.963,
    }

    def __init__(self):
        super().__init__("gameRules")

        # Carry the player count forward from playerNumberPage into
        # session_state, so it survives further navigation even after
        # the "playerCount" query param is gone from the URL.
        count = st.query_params.get("playerCount")
        if count is not None:
            st.session_state["player_count"] = count

    def render(self):
        a = self.assets
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

            btn.addEventListener("pointerdown", (e) => {{
                isPressed = true;
                btn.style.backgroundImage = "url('" + pressedImg + "')";
                btn.setPointerCapture(e.pointerId);
            }});
            btn.addEventListener("pointerup", () => {{
                if (!isPressed) return;
                isPressed = false;
                btn.style.backgroundImage = "url('" + unpressedImg + "')";
                const url = new URL(window.parent.location.href);
                url.searchParams.set("page", "playerNumberPage");
                window.parent.location.href = url.toString();
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

        st.write("")  # small spacing gap below the component
        # TODO: replace with a real pixel-art "Start Game" button/asset
        # once it's designed - this is a placeholder so the flow is
        # testable end-to-end right now.
        if st.button("▶ Start Game (placeholder)"):
            st.query_params["page"] = "wheelPage"  # adjust to your real first gameplay page
            st.rerun()