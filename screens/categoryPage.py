import html as _html

import streamlit as st
import streamlit.components.v1 as components

from screens.basePage import BasePage


class CategoryPage(BasePage):
    """
    Shows the selected category's title and 5 point-value question
    buttons (200/400/600/800/1000, doubled to 400-2000 in round 2). Each
    button is independent - clicking one records which specific question
    was chosen (category + point value) and continues to QuestionPage,
    which looks up and displays that exact question.

    Placeholder category NAMES live in CATEGORY_NAMES below - swap for a
    real question_repository lookup once that's wired up. Point values
    and round-doubling are computed here in the UI layer for now; once
    backend logic exists this could instead just ask the controller for
    "the 5 point values for this round" directly.
    """

    FRAME_W, FRAME_H = 480, 270
    BASE_POINT_VALUES = [200, 400, 600, 800, 1000]

    # Placeholder - replace with a real question_repository lookup by
    # category number once that data exists.
    CATEGORY_NAMES = {
        1: "Category 1", 2: "Category 2", 3: "Category 3",
        4: "Category 4", 5: "Category 5", 6: "Category 6",
    }

    QUESTION_BOXES = {
        1: {"left_pct": 7.292, "top_pct": 32.593, "width_pct": 22.917, "height_pct": 26.667},
        2: {"left_pct": 38.542, "top_pct": 32.593, "width_pct": 22.917, "height_pct": 26.667},
        3: {"left_pct": 69.792, "top_pct": 32.593, "width_pct": 22.917, "height_pct": 26.667},
        4: {"left_pct": 21.875, "top_pct": 61.481, "width_pct": 22.917, "height_pct": 26.667},
        5: {"left_pct": 55.208, "top_pct": 61.481, "width_pct": 22.917, "height_pct": 26.667},
    }
    # The pressed-state art is a genuinely different size (shorter, shifted
    # down slightly) than the unpressed art - that size difference IS the
    # "squished down" look. Swapping just the image while keeping the
    # unpressed box's fixed dimensions stretches the pressed art back out,
    # which looks like elongating instead of pressing. These are each
    # button's OWN real pressed-frame position/size, so on press we swap
    # the element's box to match, not just its background image.
    QUESTION_BOXES_PRESSED = {
        1: {"left_pct": 7.292, "top_pct": 36.296, "width_pct": 22.917, "height_pct": 22.963},
        2: {"left_pct": 38.542, "top_pct": 36.296, "width_pct": 22.917, "height_pct": 22.963},
        3: {"left_pct": 69.792, "top_pct": 36.296, "width_pct": 22.917, "height_pct": 22.963},
        4: {"left_pct": 21.875, "top_pct": 65.185, "width_pct": 22.917, "height_pct": 22.963},
        5: {"left_pct": 55.208, "top_pct": 65.185, "width_pct": 22.917, "height_pct": 22.963},
    }
    CATEGORY_NAME_BOX = {
        "left_pct": 30.208, "top_pct": 1.852, "width_pct": 38.542, "height_pct": 26.667,
    }
    CURRENT_POINTS_BOX = {
        "left_pct": 81.458, "top_pct": 79.630, "width_pct": 17.083, "height_pct": 16.667,
    }

    def __init__(self):
        super().__init__("CategoryPage")

    def render(self):
        a = self.assets

        selected_category = st.session_state.get("selected_category", 1)
        category_name = self.CATEGORY_NAMES.get(selected_category, f"Category {selected_category}")

        game_round = st.session_state.get("game_round", 1)
        multiplier = 2 if game_round == 2 else 1
        point_values = [v * multiplier for v in self.BASE_POINT_VALUES]

        current_points = st.session_state.get("current_points", 0)

        # One hidden nav trigger per question button, each capturing its
        # own point value + question index via a closure, so every
        # button acts fully independently.
        for i, points in enumerate(point_values, start=1):
            def make_callback(question_index, point_value):
                def callback():
                    st.session_state["selected_question_index"] = question_index
                    st.session_state["selected_point_value"] = point_value
                    # TODO: hand off to backend (e.g.
                    # self.controller.get_question(selected_category,
                    # question_index)) once question_repository is wired up,
                    # so QuestionPage can display the real question text.
                return callback

            self.render_nav_trigger(
                f"category_q{i}", "questionPage",
                on_click=make_callback(i, points),
            )

        bg = a.get("CategoryPageBackground_0")
        category_name_img = a.get("CategoryName_0")
        current_points_img = a.get("CategoryPageCurrentPoints_0")

        FRAME_W, FRAME_H = self.FRAME_W, self.FRAME_H
        cnb = self.CATEGORY_NAME_BOX
        cpb = self.CURRENT_POINTS_BOX

        question_divs = ""
        question_css = ""
        js_image_lookups = ""
        js_bind_calls = ""

        for i, points in enumerate(point_values, start=1):
            box = self.QUESTION_BOXES[i]
            unpressed = a.get(f"Q{i}Button_0")
            pressed = a.get(f"Q{i}Button_1")
            div_id = f"q{i}-btn"
            text_id = f"q{i}-text"

            question_divs += f"""
                <div id="{div_id}" class="q-hotspot"></div>
                <div id="{text_id}" class="q-text">{points}</div>
            """
            question_css += f"""
                #{div_id} {{
                    left: {box["left_pct"]:.3f}%;
                    top: {box["top_pct"]:.3f}%;
                    width: {box["width_pct"]:.3f}%;
                    height: {box["height_pct"]:.3f}%;
                    background-image: url('data:image/png;base64,{unpressed}');
                }}
                #{text_id} {{
                    left: {box["left_pct"]:.3f}%;
                    top: {box["top_pct"]:.3f}%;
                    width: {box["width_pct"]:.3f}%;
                    height: {box["height_pct"]:.3f}%;
                }}
            """
            pressed_box = self.QUESTION_BOXES_PRESSED[i]
            js_image_lookups += f"""
                qImages[{i}] = {{
                    unpressed: "data:image/png;base64,{unpressed}",
                    pressed: "data:image/png;base64,{pressed}"
                }};
                qBoxes[{i}] = {{
                    unpressed: {{ left: {box["left_pct"]:.3f}, top: {box["top_pct"]:.3f}, width: {box["width_pct"]:.3f}, height: {box["height_pct"]:.3f} }},
                    pressed: {{ left: {pressed_box["left_pct"]:.3f}, top: {pressed_box["top_pct"]:.3f}, width: {pressed_box["width_pct"]:.3f}, height: {pressed_box["height_pct"]:.3f} }}
                }};
            """
            js_bind_calls += f'{self.nav_trigger_js(f"category_q{i}")}\n'
            js_bind_calls += f'bindQuestionButton("{div_id}", "{text_id}", {i}, triggerNav_category_q{i});\n'

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
            #category-name-layer {{
                position: absolute;
                left: {cnb["left_pct"]:.3f}%;
                top: {cnb["top_pct"]:.3f}%;
                width: {cnb["width_pct"]:.3f}%;
                height: {cnb["height_pct"]:.3f}%;
                background-image: url('data:image/png;base64,{category_name_img}');
                background-size: 100% 100%;
                image-rendering: pixelated;
                pointer-events: none;
            }}
            #category-name-text {{
                position: absolute;
                left: {cnb["left_pct"]:.3f}%;
                top: {cnb["top_pct"]:.3f}%;
                width: {cnb["width_pct"]:.3f}%;
                height: {cnb["height_pct"]:.3f}%;
                display: flex;
                align-items: center;
                justify-content: center;
                text-align: center;
                font-family: 'Press Start 2P', monospace;
                font-size: min(2.8vw, 15px);
                color: #ffffff;
                pointer-events: none;
                padding: 4%;
                box-sizing: border-box;
            }}
            #current-points-layer {{
                position: absolute;
                left: {cpb["left_pct"]:.3f}%;
                top: {cpb["top_pct"]:.3f}%;
                width: {cpb["width_pct"]:.3f}%;
                height: {cpb["height_pct"]:.3f}%;
                background-image: url('data:image/png;base64,{current_points_img}');
                background-size: 100% 100%;
                image-rendering: pixelated;
                pointer-events: none;
            }}
            #current-points-text {{
                position: absolute;
                left: {cpb["left_pct"]:.3f}%;
                top: 85.556%;
                width: {cpb["width_pct"]:.3f}%;
                height: 7.778%;
                display: flex;
                align-items: center;
                justify-content: center;
                text-align: center;
                font-family: 'Press Start 2P', monospace;
                font-size: min(1.8vw, 11px);
                color: #ffffff;
                pointer-events: none;
                box-sizing: border-box;
            }}
            .q-hotspot {{
                position: absolute;
                cursor: pointer;
                background-size: 100% 100%;
                image-rendering: pixelated;
            }}
            .q-text {{
                position: absolute;
                display: flex;
                align-items: center;
                justify-content: center;
                text-align: center;
                font-family: 'Press Start 2P', monospace;
                font-size: min(3vw, 16px);
                color: #ffffff;
                pointer-events: none;
            }}
            {question_css}
        </style>

        <div id="stage-wrap">
            <div id="stage">
                <div id="bg-layer"></div>
                <div id="category-name-layer"></div>
                <div id="category-name-text">{_html.escape(category_name)}</div>
                {question_divs}
                <div id="current-points-layer"></div>
                <div id="current-points-text">{current_points}</div>
            </div>
        </div>

        <script>
            const qImages = {{}};
            const qBoxes = {{}};
            {js_image_lookups}

            function applyBoxGeometry(el, box) {{
                el.style.left = box.left + "%";
                el.style.top = box.top + "%";
                el.style.width = box.width + "%";
                el.style.height = box.height + "%";
            }}

            // Shared binder for all 5 question buttons - avoids
            // hand-duplicating near-identical pointer event blocks. Moves
            // BOTH the hotspot and its text label to match each frame's
            // own real geometry (not just swapping the image), so the
            // pressed state actually looks squished rather than stretched.
            function bindQuestionButton(elementId, textId, qNum, triggerNavFn) {{
                const el = document.getElementById(elementId);
                const textEl = document.getElementById(textId);
                let isPressed = false;

                el.addEventListener("pointerdown", (e) => {{
                    isPressed = true;
                    el.style.backgroundImage = "url('" + qImages[qNum].pressed + "')";
                    applyBoxGeometry(el, qBoxes[qNum].pressed);
                    applyBoxGeometry(textEl, qBoxes[qNum].pressed);
                    el.setPointerCapture(e.pointerId);
                }});
                el.addEventListener("pointerup", () => {{
                    if (!isPressed) return;
                    isPressed = false;
                    el.style.backgroundImage = "url('" + qImages[qNum].unpressed + "')";
                    applyBoxGeometry(el, qBoxes[qNum].unpressed);
                    applyBoxGeometry(textEl, qBoxes[qNum].unpressed);
                    triggerNavFn();
                }});
                el.addEventListener("pointerleave", () => {{
                    if (!isPressed) return;
                    isPressed = false;
                    el.style.backgroundImage = "url('" + qImages[qNum].unpressed + "')";
                    applyBoxGeometry(el, qBoxes[qNum].unpressed);
                    applyBoxGeometry(textEl, qBoxes[qNum].unpressed);
                }});
                el.addEventListener("pointercancel", () => {{
                    isPressed = false;
                    el.style.backgroundImage = "url('" + qImages[qNum].unpressed + "')";
                    applyBoxGeometry(el, qBoxes[qNum].unpressed);
                    applyBoxGeometry(textEl, qBoxes[qNum].unpressed);
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