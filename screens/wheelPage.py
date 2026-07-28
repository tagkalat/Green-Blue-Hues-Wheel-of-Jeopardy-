import streamlit as st
import streamlit.components.v1 as components

from screens.basePage import BasePage


class WheelPage(BasePage):
    """
    Placeholder wheel scene - shows the board layout (background, wheel,
    pointer, points/tokens/turn indicators) statically. The actual
    spin-to-a-specific-sector mechanic isn't built yet; this just gets
    navigation to a real, non-dead-end destination after PlayerNumberPage.
    """

    FRAME_W, FRAME_H = 480, 270

    def __init__(self):
        super().__init__("wheel")

    def render(self):
        a = self.assets
        layers = [
            ("wheelBackground_0", {"left_pct": 0, "top_pct": 0, "width_pct": 100, "height_pct": 100}),
            ("wheelWheel_0", {"left_pct": 23.333, "top_pct": 2.963, "width_pct": 53.333, "height_pct": 94.074}),
            ("wheelPointer_0", {"left_pct": 46.667, "top_pct": 1.111, "width_pct": 5.417, "height_pct": 18.519}),
            ("wheelPlayerTurn_0", {"left_pct": 3.125, "top_pct": 2.963, "width_pct": 20.625, "height_pct": 19.259}),
            ("wheelSpinsLeft_0", {"left_pct": 82.083, "top_pct": 5.556, "width_pct": 15.0, "height_pct": 13.333}),
            ("wheelSpinTokens_0", {"left_pct": 81.458, "top_pct": 60.370, "width_pct": 17.083, "height_pct": 17.037}),
            ("wheelCurrentPoints_0", {"left_pct": 81.458, "top_pct": 78.889, "width_pct": 17.083, "height_pct": 17.407}),
        ]

        FRAME_W, FRAME_H = self.FRAME_W, self.FRAME_H

        layer_divs = ""
        layer_css = ""
        for name, box in layers:
            img_data = a.get(name)
            layer_divs += f'<div class="layer" id="{name}"></div>\n'
            layer_css += f"""
                #{name} {{
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
            {layer_css}
        </style>

        <div id="stage-wrap">
            <div id="stage">
                {layer_divs}
            </div>
        </div>

        <script>
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

        st.caption("Placeholder wheel scene - spin mechanic coming next.")
