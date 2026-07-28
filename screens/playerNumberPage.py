import streamlit as st
import streamlit.components.v1 as components

from screens.basePage import BasePage


class PlayerNumberPage(BasePage):
    """
    Asks how many players will be playing. The number box itself has no
    dedicated art, so we overlay a real HTML <input> (styled with a pixel
    font) directly on top of the green box drawn in the background art.
    """

    FRAME_W, FRAME_H = 480, 270

    # Green input box location, found by detecting its fill color directly
    # in the background art (no separate asset/JSON existed for it).
    INPUT_BOX = {
        "left_pct": 33.958, "top_pct": 40.000,
        "width_pct": 32.292, "height_pct": 24.444,
    }

    # Button bounding box from positions_manifest.json (unpressed frame)
    BUTTON_BOX = {
        "left_pct": 38.333, "top_pct": 73.333,
        "width_pct": 23.333, "height_pct": 17.407,
    }

    def __init__(self):
        super().__init__("playerNumberPage")

    def render(self):
        a = self.assets
        bg = a.get("PagePlayerNumberBackground_0")
        button_unpressed = a.get("PagePlayerNumberButton_0")
        button_pressed = a.get("PagePlayerNumberButton_1")

        FRAME_W, FRAME_H = self.FRAME_W, self.FRAME_H
        ib = self.INPUT_BOX
        bb = self.BUTTON_BOX

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
            /* Hide the little up/down spinner arrows most browsers add to
               number inputs, since they don't fit the pixel-art look. */
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
                left: {bb["left_pct"]:.3f}%;
                top: {bb["top_pct"]:.3f}%;
                width: {bb["width_pct"]:.3f}%;
                height: {bb["height_pct"]:.3f}%;
                cursor: pointer;
                background-size: 100% 100%;
                image-rendering: pixelated;
                background-image: url('data:image/png;base64,{button_unpressed}');
            }}
        </style>

        <div id="stage-wrap">
            <div id="stage">
                <div id="bg-layer"></div>
                <input id="player-count-input" type="number" min="1" max="12" value="4" />
                <div id="submit-btn"></div>
            </div>
        </div>

        <script>
            const unpressedImg = "data:image/png;base64,{button_unpressed}";
            const pressedImg = "data:image/png;base64,{button_pressed}";

            const btn = document.getElementById("submit-btn");
            const input = document.getElementById("player-count-input");
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

                const count = input.value || "1";
                const url = new URL(window.parent.location.href);
                url.searchParams.set("page", "gameRules");
                url.searchParams.set("playerCount", count);
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

        # Read the player count back out on the receiving page (gameRules)
        # via: st.query_params.get("playerCount")