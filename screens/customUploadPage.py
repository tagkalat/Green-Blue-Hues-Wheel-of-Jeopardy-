import streamlit as st
import streamlit.components.v1 as components

from screens.basePage import BasePage


class CustomUploadPage(BasePage):
    """
    Lets the host upload a custom question set. Shows the rules box
    explaining the required format, a native file uploader, a checkmark
    that appears once a file is chosen, and a Back button that (per
    design) actually continues FORWARD to playerNumberPage.
    """

    FRAME_W, FRAME_H = 480, 270

    RULEBOX_BOX = {
        "left_pct": 33.333, "top_pct": 7.407,
        "width_pct": 33.333, "height_pct": 33.333,
    }
    DONEMARK_BOX = {
        "left_pct": 71.875, "top_pct": 20.370,
        "width_pct": 8.333, "height_pct": 11.111,
    }
    BACK_BOX = {
        "left_pct": 0.833, "top_pct": 0.370,
        "width_pct": 7.708, "height_pct": 12.963,
    }

    def __init__(self):
        super().__init__("customUploadpage")

    def render(self):
        a = self.assets

        self.render_nav_trigger("customupload_back", "playerNumberPage")
        bg = a.get("CustomUploadBackground_0")
        # NOTE: Rulebox_0 and _1 share the same position/size - treating
        # as a static box for now since there's no clear press/animation
        # behavior defined for it yet.
        rulebox = a.get("CustomUploadRulebox_0")
        back_unpressed = a.get("CustomUploadBackbutton_0")
        back_pressed = a.get("CustomUploadBackbutton_1")

        uploaded_file = st.file_uploader(
            "Upload your custom question set (Excel template)",
            type=["xlsx"],
        )
        file_was_uploaded = uploaded_file is not None

        if file_was_uploaded:
            st.session_state["custom_questions_file"] = uploaded_file
            # TODO: hand this off to your backend (e.g.
            # self.controller.load_custom_questions(uploaded_file))
            # once question_repository's loading interface is ready.
            donemark_html = f"""
                <div id="donemark" style="
                    position: absolute;
                    left: {self.DONEMARK_BOX["left_pct"]:.3f}%;
                    top: {self.DONEMARK_BOX["top_pct"]:.3f}%;
                    width: {self.DONEMARK_BOX["width_pct"]:.3f}%;
                    height: {self.DONEMARK_BOX["height_pct"]:.3f}%;
                    background-image: url('data:image/png;base64,{a.get("CustomUploadDonemark_1")}');
                    background-size: 100% 100%;
                    image-rendering: pixelated;
                "></div>
            """
        else:
            donemark_html = ""

        FRAME_W, FRAME_H = self.FRAME_W, self.FRAME_H
        rb = self.RULEBOX_BOX
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
                background-image: url('data:image/png;base64,{bg}');
                background-size: 100% 100%;
                image-rendering: pixelated;
            }}
            #rulebox-layer {{
                position: absolute;
                left: {rb["left_pct"]:.3f}%;
                top: {rb["top_pct"]:.3f}%;
                width: {rb["width_pct"]:.3f}%;
                height: {rb["height_pct"]:.3f}%;
                background-image: url('data:image/png;base64,{rulebox}');
                background-size: 100% 100%;
                image-rendering: pixelated;
                pointer-events: none;
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
                <div id="rulebox-layer"></div>
                {donemark_html}
                <div id="back-btn"></div>
            </div>
        </div>

        <script>
            const unpressedImg = "data:image/png;base64,{back_unpressed}";
            const pressedImg = "data:image/png;base64,{back_pressed}";
            const btn = document.getElementById("back-btn");
            let isPressed = false;

            {self.nav_trigger_js("customupload_back")}

            btn.addEventListener("pointerdown", (e) => {{
                isPressed = true;
                btn.style.backgroundImage = "url('" + pressedImg + "')";
                btn.setPointerCapture(e.pointerId);
            }});
            btn.addEventListener("pointerup", () => {{
                if (!isPressed) return;
                isPressed = false;
                btn.style.backgroundImage = "url('" + unpressedImg + "')";
                // Per design: this button continues FORWARD, not back.
                triggerNav_customupload_back();
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