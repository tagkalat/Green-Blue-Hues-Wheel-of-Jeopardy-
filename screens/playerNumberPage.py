import streamlit as st
import streamlit.components.v1 as components

from screens.basePage import BasePage


class PlayerNumberPage(BasePage):
    """
    Asks how many players will be playing. The number box itself has no
    dedicated art, so we overlay a real HTML <input> (styled with a pixel
    font) directly on top of the green box drawn in the background art.

    Also has a Back button (reusing GameStartBackbutton art) returning to
    the title screen.
    """

    FRAME_W, FRAME_H = 480, 270

    # Green input box location, found by detecting its fill color directly
    # in the background art (no separate asset/JSON existed for it).
    INPUT_BOX = {
        "left_pct": 33.958, "top_pct": 40.000,
        "width_pct": 32.292, "height_pct": 24.444,
    }

    # Button bounding box from positions_manifest.json (unpressed frame)
    SUBMIT_BOX = {
        "left_pct": 38.333, "top_pct": 73.333,
        "width_pct": 23.333, "height_pct": 17.407,
    }
    BACK_BOX = {
        "left_pct": 0.833, "top_pct": 0.370,
        "width_pct": 7.708, "height_pct": 12.963,
    }

    def __init__(self):
        super().__init__("playerNumberPage")

    def render(self):
        a = self.assets

        self.render_nav_trigger_with_value(
            "playernum_submit", "wheel",
            value_session_key="player_count", default_value=4,
        )
        self.render_nav_trigger("playernum_back", "title")

        bg = a.get("PagePlayerNumberBackground_0")
        submit_unpressed = a.get("PagePlayerNumberButton_0")
        submit_pressed = a.get("PagePlayerNumberButton_1")
        back_unpressed = a.get("GameStartBackbutton_0")
        back_pressed = a.get("GameStartBackbutton_1")

        FRAME_W, FRAME_H = self.FRAME_W, self.FRAME_H
        ib = self.INPUT_BOX
        sb = self.SUBMIT_BOX
        bk = self.BACK_BOX

        html = f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

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
            #player-count-input {{
                position: absolute;
                left: {ib["left_pct"]:.3f}%;
                top: {ib["top_pct"]:.3f}%;
                width: {ib["width_pct"]:.3f}%;
                height: {ib["height_pct"]:.3f}%;
                border: none;
                background: transparent;
                text-align: center;
                font-family: 'Press Start 2P', monospace;
                font-size: min(4vw, 28px);
                color: #1a1a1a;
                box-sizing: border-box;
            }}
            #player-count-input::-webkit-outer-spin-button,
            #player-count-input::-webkit-inner-spin-button {{
                -webkit-appearance: none;
                margin: 0;
            }}
            #player-count-input[type=number] {{
                -moz-appearance: textfield;
            }}
            #submit-btn {{
                position: absolute;
                left: {sb["left_pct"]:.3f}%;
                top: {sb["top_pct"]:.3f}%;
                width: {sb["width_pct"]:.3f}%;
                height: {sb["height_pct"]:.3f}%;
                cursor: pointer;
                background-size: 100% 100%;
                image-rendering: pixelated;
                background-image: url('data:image/png;base64,{submit_unpressed}');
            }}
            #back-btn {{
                position: absolute;
                left: {bk["left_pct"]:.3f}%;
                top: {bk["top_pct"]:.3f}%;
                width: {bk["width_pct"]:.3f}%;
                height: {bk["height_pct"]:.3f}%;
                cursor: pointer;
                background-size: 100% 100%;
                image-rendering: pixelated;
                background-image: url('data:image/png;base64,{back_unpressed}');
            }}
        </style>

        <div id="stage-wrap">
            <div id="stage">
                <div id="bg-layer"></div>
                <input id="player-count-input" type="number" min="1" max="12" value="4" />
                <div id="submit-btn"></div>
                <div id="back-btn"></div>
            </div>
        </div>

        <script>
            {self.nav_trigger_with_value_js("playernum_submit")}
            {self.nav_trigger_js("playernum_back")}

            // --- Submit button (its own uniquely-named variables) ---
            const submitUnpressedImg = "data:image/png;base64,{submit_unpressed}";
            const submitPressedImg = "data:image/png;base64,{submit_pressed}";
            const submitBtn = document.getElementById("submit-btn");
            const input = document.getElementById("player-count-input");
            let isSubmitPressed = false;

            submitBtn.addEventListener("pointerdown", (e) => {{
                isSubmitPressed = true;
                submitBtn.style.backgroundImage = "url('" + submitPressedImg + "')";
                submitBtn.setPointerCapture(e.pointerId);
            }});
            submitBtn.addEventListener("pointerup", () => {{
                if (!isSubmitPressed) return;
                isSubmitPressed = false;
                submitBtn.style.backgroundImage = "url('" + submitUnpressedImg + "')";
                const count = input.value || "1";
                setAndTriggerNav_playernum_submit(count);
            }});
            submitBtn.addEventListener("pointerleave", () => {{
                if (!isSubmitPressed) return;
                isSubmitPressed = false;
                submitBtn.style.backgroundImage = "url('" + submitUnpressedImg + "')";
            }});
            submitBtn.addEventListener("pointercancel", () => {{
                isSubmitPressed = false;
                submitBtn.style.backgroundImage = "url('" + submitUnpressedImg + "')";
            }});

            // --- Back button (its own uniquely-named variables) ---
            const backUnpressedImg = "data:image/png;base64,{back_unpressed}";
            const backPressedImg = "data:image/png;base64,{back_pressed}";
            const backBtn = document.getElementById("back-btn");
            let isBackPressed = false;

            backBtn.addEventListener("pointerdown", (e) => {{
                isBackPressed = true;
                backBtn.style.backgroundImage = "url('" + backPressedImg + "')";
                backBtn.setPointerCapture(e.pointerId);
            }});
            backBtn.addEventListener("pointerup", () => {{
                if (!isBackPressed) return;
                isBackPressed = false;
                backBtn.style.backgroundImage = "url('" + backUnpressedImg + "')";
                triggerNav_playernum_back();
            }});
            backBtn.addEventListener("pointerleave", () => {{
                if (!isBackPressed) return;
                isBackPressed = false;
                backBtn.style.backgroundImage = "url('" + backUnpressedImg + "')";
            }});
            backBtn.addEventListener("pointercancel", () => {{
                isBackPressed = false;
                backBtn.style.backgroundImage = "url('" + backUnpressedImg + "')";
            }});

            window.addEventListener("pageshow", () => {{
                submitBtn.style.backgroundImage = "url('" + submitUnpressedImg + "')";
                backBtn.style.backgroundImage = "url('" + backUnpressedImg + "')";
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