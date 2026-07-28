import streamlit.components.v1 as components

from screens.basePage import BasePage


class TitlePage(BasePage):
    """
    Renders the title screen: static background, looping title+stars
    animation, and three pixel-art buttons (Start, Custom, Help) with
    real press/hold/release behavior.
    """

    FRAME_W, FRAME_H = 480, 270

    # Exact bounding boxes pulled straight from each button's Aseprite JSON
    # (spriteSourceSize), no guessing needed since these were trimmed exports.
    BOXES = {
        "start":  (176, 128, 176 + 128, 128 + 64),
        "custom": (176, 192, 176 + 128, 192 + 64),
        "help":   (432, 224, 432 + 48, 224 + 48),
    }

    def __init__(self):
        super().__init__("titlepage")  # -> assets/titlepage/

    def _css_box(self, name: str) -> str:
        x0, y0, x1, y1 = self.BOXES[name]
        left = x0 / self.FRAME_W * 100
        top = y0 / self.FRAME_H * 100
        width = (x1 - x0) / self.FRAME_W * 100
        height = (y1 - y0) / self.FRAME_H * 100
        return f"left:{left:.3f}%; top:{top:.3f}%; width:{width:.3f}%; height:{height:.3f}%;"

    def render(self):
        a = self.assets

        # Hidden real Streamlit buttons that actually perform navigation -
        # see BasePage.render_nav_trigger() for why this replaced the old
        # window.parent.location.href approach (blocked by iframe sandbox).
        self.render_nav_trigger("title_start", "playerNumberPage")
        self.render_nav_trigger("title_custom", "customUploadpage")
        self.render_nav_trigger("title_help", "gameRules")

        bg = a.get("background_0")
        title_stars_0 = a.get("TitleAndStars_0")
        title_stars_1 = a.get("TitleAndStars_1")

        start_unpressed = a.get("StartButton_0")
        start_pressed = a.get("StartButton_1")
        custom_unpressed = a.get("CustomButton_0")
        custom_pressed = a.get("CustomButton_1")
        help_unpressed = a.get("HelpButton_0")
        help_pressed = a.get("HelpButton_1")

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
            /* Title + stars combined layer, looping between its 2 frames */
            #titlestars-layer {{
                position: absolute;
                inset: 0;
                background-image: url('data:image/png;base64,{title_stars_0}');
                background-size: 100% 100%;
                image-rendering: pixelated;
                pointer-events: none;
            }}
            .hotspot {{
                position: absolute;
                cursor: pointer;
                background-size: 100% 100%;
                image-rendering: pixelated;
            }}
            #start-btn  {{ {self._css_box("start")}  background-image: url('data:image/png;base64,{start_unpressed}'); }}
            #custom-btn {{ {self._css_box("custom")} background-image: url('data:image/png;base64,{custom_unpressed}'); }}
            #help-btn   {{ {self._css_box("help")}   background-image: url('data:image/png;base64,{help_unpressed}'); }}
        </style>

        <div id="stage-wrap">
            <div id="stage">
                <div id="bg-layer"></div>
                <div id="titlestars-layer"></div>
                <div id="start-btn" class="hotspot"></div>
                <div id="custom-btn" class="hotspot"></div>
                <div id="help-btn" class="hotspot"></div>
            </div>
        </div>

        <script>
            // --- Title/stars twinkle loop ---
            const tsFrames = [
                "data:image/png;base64,{title_stars_0}",
                "data:image/png;base64,{title_stars_1}"
            ];
            let tsIndex = 0;
            const tsEl = document.getElementById("titlestars-layer");
            setInterval(() => {{
                tsIndex = (tsIndex + 1) % tsFrames.length;
                tsEl.style.backgroundImage = "url('" + tsFrames[tsIndex] + "')";
            }}, 500);

            // --- Button press/hold/release + navigation ---
            const unpressedImgs = {{
                start: "data:image/png;base64,{start_unpressed}",
                custom: "data:image/png;base64,{custom_unpressed}",
                help: "data:image/png;base64,{help_unpressed}"
            }};
            const pressedImgs = {{
                start: "data:image/png;base64,{start_pressed}",
                custom: "data:image/png;base64,{custom_pressed}",
                help: "data:image/png;base64,{help_pressed}"
            }};

            {self.nav_trigger_js("title_start")}
            {self.nav_trigger_js("title_custom")}
            {self.nav_trigger_js("title_help")}

            const navTriggers = {{
                start: triggerNav_title_start,
                custom: triggerNav_title_custom,
                help: triggerNav_title_help
            }};

            function bindButton(id, key) {{
                const el = document.getElementById(id);
                let isPressed = false;

                el.addEventListener("pointerdown", (e) => {{
                    isPressed = true;
                    el.style.backgroundImage = "url('" + pressedImgs[key] + "')";
                    el.setPointerCapture(e.pointerId);
                }});

                el.addEventListener("pointerup", () => {{
                    if (!isPressed) return;
                    isPressed = false;
                    el.style.backgroundImage = "url('" + unpressedImgs[key] + "')";
                    navTriggers[key]();
                }});

                el.addEventListener("pointerleave", () => {{
                    if (!isPressed) return;
                    isPressed = false;
                    el.style.backgroundImage = "url('" + unpressedImgs[key] + "')";
                }});
                el.addEventListener("pointercancel", () => {{
                    isPressed = false;
                    el.style.backgroundImage = "url('" + unpressedImgs[key] + "')";
                }});
            }}

            bindButton("start-btn", "start");
            bindButton("custom-btn", "custom");
            bindButton("help-btn", "help");

            // Reset to unpressed on any (re)show, including bfcache restores
            function resetButtons() {{
                document.getElementById("start-btn").style.backgroundImage = "url('" + unpressedImgs.start + "')";
                document.getElementById("custom-btn").style.backgroundImage = "url('" + unpressedImgs.custom + "')";
                document.getElementById("help-btn").style.backgroundImage = "url('" + unpressedImgs.help + "')";
            }}
            window.addEventListener("pageshow", resetButtons);

            {self.fit_to_window_js(FRAME_W, FRAME_H)}

            // Auto-size the iframe to the actual responsive stage height
            function resizeFrame() {{
                const stage = document.getElementById("stage");
                if (window.frameElement) {{
                    window.frameElement.style.height = (stage.offsetHeight + 10) + "px";
                }}
            }}
            function fitAndResize() {{
                fitToWindow();
                resizeFrame();
            }}
            window.addEventListener("resize", fitAndResize);
            window.addEventListener("load", fitAndResize);
            setTimeout(fitAndResize, 50);
            setTimeout(fitAndResize, 300);
        </script>
        """
        components.html(html, height=int(FRAME_H / FRAME_W * 700) + 20)