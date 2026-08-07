import streamlit as st
import streamlit.components.v1 as components

from screens.basePage import BasePage


class PlayersChoicePage(BasePage):
    """
    Shown when the wheel lands on "Player's Choice". Lets the current
    player pick which of the 6 categories to answer from next - clicking
    a category sets it in session_state and continues to CategoryPage.
    """

    FRAME_W, FRAME_H = 480, 270
    ASSET_PREFIX = "PlayersChoice"  # matches PlayersChoiceCat1Button_0 etc.

    CATEGORY_BOXES = {
        1: {"left_pct": 25.0, "top_pct": 22.963, "width_pct": 22.917, "height_pct": 22.963},
        2: {"left_pct": 25.0, "top_pct": 47.778, "width_pct": 22.917, "height_pct": 22.963},
        3: {"left_pct": 25.0, "top_pct": 72.963, "width_pct": 22.917, "height_pct": 22.963},
        4: {"left_pct": 53.125, "top_pct": 22.963, "width_pct": 22.917, "height_pct": 22.963},
        5: {"left_pct": 53.125, "top_pct": 47.778, "width_pct": 22.917, "height_pct": 22.963},
        6: {"left_pct": 53.125, "top_pct": 72.963, "width_pct": 22.917, "height_pct": 22.963},
    }
    # Pressed-frame art is shorter than unpressed - swap geometry too, or
    # the pressed art stretches to fill the taller unpressed box instead
    # of visually squishing down.
    CATEGORY_BOXES_PRESSED = {
        1: {"left_pct": 25.0, "top_pct": 26.667, "width_pct": 22.917, "height_pct": 18.889},
        2: {"left_pct": 25.0, "top_pct": 51.852, "width_pct": 22.917, "height_pct": 18.889},
        3: {"left_pct": 25.0, "top_pct": 76.667, "width_pct": 22.917, "height_pct": 18.889},
        4: {"left_pct": 53.125, "top_pct": 26.667, "width_pct": 22.917, "height_pct": 18.889},
        5: {"left_pct": 53.125, "top_pct": 51.852, "width_pct": 22.917, "height_pct": 18.889},
        6: {"left_pct": 53.125, "top_pct": 76.667, "width_pct": 22.917, "height_pct": 18.889},
    }

    def __init__(self):
        super().__init__("PlayersChoicePage")

    def render(self):
        a = self.assets

        # One hidden nav trigger per category, each capturing which
        # category number it represents via a closure.
        for cat_num in self.CATEGORY_BOXES:
            def make_callback(n):
                def callback():
                    st.session_state["selected_category"] = n
                    # TODO: hand off to backend (e.g.
                    # self.controller.select_category(n)) once
                    # question_repository is wired up.
                return callback

            self.render_nav_trigger(
                f"playerschoice_cat{cat_num}", "categoryPage",
                on_click=make_callback(cat_num),
            )

        bg = a.get(f"{self.ASSET_PREFIX}PageBackground_0")

        FRAME_W, FRAME_H = self.FRAME_W, self.FRAME_H

        hotspot_divs = ""
        hotspot_css = ""
        js_bind_calls = ""
        js_image_lookups = ""

        for cat_num, box in self.CATEGORY_BOXES.items():
            unpressed = a.get(f"{self.ASSET_PREFIX}Cat{cat_num}Button_0")
            pressed = a.get(f"{self.ASSET_PREFIX}Cat{cat_num}Button_1")
            div_id = f"cat{cat_num}-btn"

            hotspot_divs += f'<div id="{div_id}" class="cat-hotspot"></div>\n'
            hotspot_css += f"""
                #{div_id} {{
                    left: {box["left_pct"]:.3f}%;
                    top: {box["top_pct"]:.3f}%;
                    width: {box["width_pct"]:.3f}%;
                    height: {box["height_pct"]:.3f}%;
                    background-image: url('data:image/png;base64,{unpressed}');
                }}
            """
            pressed_box = self.CATEGORY_BOXES_PRESSED[cat_num]
            js_image_lookups += f"""
                catImages[{cat_num}] = {{
                    unpressed: "data:image/png;base64,{unpressed}",
                    pressed: "data:image/png;base64,{pressed}"
                }};
                catBoxes[{cat_num}] = {{
                    unpressed: {{ left: {box["left_pct"]:.3f}, top: {box["top_pct"]:.3f}, width: {box["width_pct"]:.3f}, height: {box["height_pct"]:.3f} }},
                    pressed: {{ left: {pressed_box["left_pct"]:.3f}, top: {pressed_box["top_pct"]:.3f}, width: {pressed_box["width_pct"]:.3f}, height: {pressed_box["height_pct"]:.3f} }}
                }};
            """
            js_bind_calls += f'{self.nav_trigger_js(f"playerschoice_cat{cat_num}")}\n'
            js_bind_calls += f'bindCategoryButton("{div_id}", {cat_num}, triggerNav_playerschoice_cat{cat_num});\n'

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
            .cat-hotspot {{
                position: absolute;
                cursor: pointer;
                background-size: 100% 100%;
                image-rendering: pixelated;
            }}
            {hotspot_css}
        </style>

        <div id="stage-wrap">
            <div id="stage">
                <div id="bg-layer"></div>
                {hotspot_divs}
            </div>
        </div>

        <script>
            const catImages = {{}};
            const catBoxes = {{}};
            {js_image_lookups}

            function applyCatBoxGeometry(el, box) {{
                el.style.left = box.left + "%";
                el.style.top = box.top + "%";
                el.style.width = box.width + "%";
                el.style.height = box.height + "%";
            }}

            // Shared binder for all 6 category buttons - avoids
            // hand-duplicating near-identical pointerdown/up/leave/cancel
            // blocks 6 times (and the naming-collision risk that comes
            // with copy-pasting them).
            function bindCategoryButton(elementId, catNum, triggerNavFn) {{
                const el = document.getElementById(elementId);
                let isPressed = false;

                el.addEventListener("pointerdown", (e) => {{
                    isPressed = true;
                    el.style.backgroundImage = "url('" + catImages[catNum].pressed + "')";
                    applyCatBoxGeometry(el, catBoxes[catNum].pressed);
                    el.setPointerCapture(e.pointerId);
                }});
                el.addEventListener("pointerup", () => {{
                    if (!isPressed) return;
                    isPressed = false;
                    el.style.backgroundImage = "url('" + catImages[catNum].unpressed + "')";
                    applyCatBoxGeometry(el, catBoxes[catNum].unpressed);
                    triggerNavFn();
                }});
                el.addEventListener("pointerleave", () => {{
                    if (!isPressed) return;
                    isPressed = false;
                    el.style.backgroundImage = "url('" + catImages[catNum].unpressed + "')";
                    applyCatBoxGeometry(el, catBoxes[catNum].unpressed);
                }});
                el.addEventListener("pointercancel", () => {{
                    isPressed = false;
                    el.style.backgroundImage = "url('" + catImages[catNum].unpressed + "')";
                    applyCatBoxGeometry(el, catBoxes[catNum].unpressed);
                }});
            }}

            {js_bind_calls}

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