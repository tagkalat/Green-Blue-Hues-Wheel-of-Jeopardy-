import streamlit as st
import streamlit.components.v1 as components

from screens.basePage import BasePage


class WheelPage(BasePage):
    """
    Wheel scene with a real click-to-spin mechanic. Clicking the wheel
    graphic spins it via a CSS rotation animation and lands precisely
    within a chosen sector (11 sectors, each 360/11 degrees).

    NOTE on sector selection: right now the winning sector is picked
    randomly in JS as a placeholder (see pickWinningSector() below) since
    game_controller isn't wired up yet. Once wheel_service can tell us
    which sector should win, swap that one function out to use the real
    value instead - everything else (the rotation math/animation) stays
    the same regardless of where the sector index comes from.
    """

    FRAME_W, FRAME_H = 480, 270
    NUM_SECTORS = 11

    # Wheel graphic's own box on the stage (from positions_manifest.json).
    # Rotation is applied to this element directly, around its own center,
    # so its position on the page never needs to change - only its
    # internal rotation angle does.
    WHEEL_BOX = {"left_pct": 23.333, "top_pct": 2.963, "width_pct": 53.333, "height_pct": 94.074}

    def __init__(self):
        super().__init__("wheel")

    def render(self):
        a = self.assets

        # Static (non-spinning) layers - background, pointer, HUD elements
        static_layers = [
            ("wheelBackground_0", {"left_pct": 0, "top_pct": 0, "width_pct": 100, "height_pct": 100}),
            ("wheelPlayerTurn_0", {"left_pct": 3.125, "top_pct": 2.963, "width_pct": 20.625, "height_pct": 19.259}),
            ("wheelSpinsLeft_0", {"left_pct": 82.083, "top_pct": 5.556, "width_pct": 15.0, "height_pct": 13.333}),
            ("wheelSpinTokens_0", {"left_pct": 81.458, "top_pct": 60.370, "width_pct": 17.083, "height_pct": 17.037}),
            ("wheelCurrentPoints_0", {"left_pct": 81.458, "top_pct": 78.889, "width_pct": 17.083, "height_pct": 17.407}),
        ]
        # Pointer is drawn AFTER (on top of) the wheel graphic, since it
        # sits fixed above the spinning wheel and must never rotate with it.
        pointer_layer = ("wheelPointer_0", {"left_pct": 46.667, "top_pct": 1.111, "width_pct": 5.417, "height_pct": 18.519})

        wheel_img = a.get("wheelWheel_0")

        FRAME_W, FRAME_H = self.FRAME_W, self.FRAME_H
        wb = self.WHEEL_BOX

        static_divs = ""
        static_css = ""
        for i, (name, box) in enumerate(static_layers):
            img_data = a.get(name)
            div_id = f"static-{i}"
            static_divs += f'<div class="layer" id="{div_id}"></div>\n'
            static_css += f"""
                #{div_id} {{
                    position: absolute;
                    left: {box["left_pct"]:.3f}%;
                    top: {box["top_pct"]:.3f}%;
                    width: {box["width_pct"]:.3f}%;
                    height: {box["height_pct"]:.3f}%;
                    background-image: url('data:image/png;base64,{img_data}');
                    background-size: 100% 100%;
                    image-rendering: pixelated;
                }}
            """
        pointer_name, pointer_box = pointer_layer
        pointer_img = a.get(pointer_name)

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
            .layer {{ position: absolute; image-rendering: pixelated; }}
            {static_css}

            #wheel-graphic {{
                position: absolute;
                left: {wb["left_pct"]:.3f}%;
                top: {wb["top_pct"]:.3f}%;
                width: {wb["width_pct"]:.3f}%;
                height: {wb["height_pct"]:.3f}%;
                background-image: url('data:image/png;base64,{wheel_img}');
                background-size: 100% 100%;
                image-rendering: pixelated;
                cursor: pointer;
                transform-origin: 50% 50%;
                transform: rotate(0deg);
                /* Duration/easing of the spin - ease-out gives that
                   "fast start, slow finish" feel of a real wheel. */
                transition: transform 4s cubic-bezier(0.17, 0.67, 0.16, 0.99);
            }}
            #wheel-graphic.spinning {{
                cursor: not-allowed;
            }}

            #pointer-layer {{
                position: absolute;
                left: {pointer_box["left_pct"]:.3f}%;
                top: {pointer_box["top_pct"]:.3f}%;
                width: {pointer_box["width_pct"]:.3f}%;
                height: {pointer_box["height_pct"]:.3f}%;
                background-image: url('data:image/png;base64,{pointer_img}');
                background-size: 100% 100%;
                image-rendering: pixelated;
                pointer-events: none;
            }}

            #result-readout {{
                position: absolute;
                left: 50%;
                bottom: 4%;
                transform: translateX(-50%);
                font-family: monospace;
                font-size: min(3vw, 18px);
                color: white;
                background: rgba(0,0,0,0.55);
                padding: 4px 10px;
                border-radius: 4px;
                pointer-events: none;
                opacity: 0;
                transition: opacity 0.4s;
            }}
            #result-readout.visible {{ opacity: 1; }}
        </style>

        <div id="stage-wrap">
            <div id="stage">
                {static_divs}
                <div id="wheel-graphic"></div>
                <div id="pointer-layer"></div>
                <div id="result-readout"></div>
            </div>
        </div>

        <script>
            const NUM_SECTORS = {self.NUM_SECTORS};
            const SECTOR_ANGLE = 360 / NUM_SECTORS;

            const wheelEl = document.getElementById("wheel-graphic");
            const readoutEl = document.getElementById("result-readout");

            let currentRotation = 0;   // total accumulated rotation so far
            let isSpinning = false;

            // PLACEHOLDER: picks a random sector (0 to NUM_SECTORS-1).
            // Swap this out once the backend can supply the real winning
            // sector - everything below this function works the same
            // regardless of how the sector index is chosen.
            function pickWinningSector() {{
                return Math.floor(Math.random() * NUM_SECTORS);
            }}

            function spinWheel() {{
                if (isSpinning) return;
                isSpinning = true;
                wheelEl.classList.add("spinning");
                readoutEl.classList.remove("visible");

                const winningSector = pickWinningSector();

                // Angle (within the wheel's own 0-360 space) that puts
                // the CENTER of the winning sector under the pointer.
                // Sector 0 is assumed to start at the top (0deg), matching
                // where the pointer sits, going clockwise.
                const targetAngleInWheel = winningSector * SECTOR_ANGLE;

                // We rotate the WHEEL clockwise to bring that sector under
                // the (fixed, top-mounted) pointer - so the wheel needs to
                // turn by the negative of that angle (360 - target),
                // otherwise sector 0 rotating clockwise moves AWAY from
                // the pointer instead of staying under it.
                const neededOffset = (360 - targetAngleInWheel) % 360;

                // Add several full spins purely for visual drama - doesn't
                // change which sector we land on, since 360deg is a full
                // circle regardless of how many times we go around.
                const fullSpins = 5 + Math.floor(Math.random() * 3); // 5-7 spins

                // Always add a NEW forward rotation on top of wherever the
                // wheel currently is, so consecutive spins keep visually
                // spinning forward rather than snapping backward.
                const currentOffset = ((currentRotation % 360) + 360) % 360;
                const deltaToTarget = ((neededOffset - currentOffset) + 360) % 360;

                currentRotation += (fullSpins * 360) + deltaToTarget;
                wheelEl.style.transform = "rotate(" + currentRotation + "deg)";

                setTimeout(() => {{
                    isSpinning = false;
                    wheelEl.classList.remove("spinning");
                    readoutEl.textContent = "Landed on sector: " + (winningSector + 1);
                    readoutEl.classList.add("visible");
                }}, 4100); // slightly longer than the 4s CSS transition
            }}

            wheelEl.addEventListener("click", spinWheel);

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

        st.caption("Click the wheel to spin it. Sector selection is random for now (placeholder until wheel_service is wired up).")
