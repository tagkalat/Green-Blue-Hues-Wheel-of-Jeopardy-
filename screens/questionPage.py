import html as _html

import streamlit as st
import streamlit.components.v1 as components

from screens.basePage import BasePage


class QuestionPage(BasePage):
    """
    Shows the question for whichever category+point-value was selected
    on CategoryPage, plus 3 clickable answer options. Clicking an answer
    records which one was chosen (and what the correct one was) into
    session_state, then continues to AnswerPage to show the result.
    """

    FRAME_W, FRAME_H = 480, 270

    ANSWER_BOXES = {
        1: {"left_pct": 22.917, "top_pct": 26.667, "width_pct": 54.167, "height_pct": 21.111},
        2: {"left_pct": 22.917, "top_pct": 50.000, "width_pct": 54.167, "height_pct": 21.111},
        3: {"left_pct": 22.917, "top_pct": 72.963, "width_pct": 54.167, "height_pct": 21.111},
    }
    QUESTION_TEXT_BOX = {
        "left_pct": 16.667, "top_pct": 1.852, "width_pct": 66.667, "height_pct": 22.963,
    }
    CURRENT_POINTS_BOX = {
        "left_pct": 81.458, "top_pct": 79.630, "width_pct": 17.083, "height_pct": 16.667,
    }

    def __init__(self):
        super().__init__("QuestionPage")

    @staticmethod
    def get_question_data(category: int, question_index: int):
        """
        Placeholder question data - swap for a real lookup (e.g.
        self.controller.get_question(category, question_index) against
        question_repository) once that's wired up. Returns
        (question_text, [answer1, answer2, answer3], correct_index (1-3)).
        """
        return (
            f"Placeholder question for Category {category}, question #{question_index}.",
            ["Answer A", "Answer B", "Answer C"],
            1,  # correct_index - placeholder always marks the first answer correct
        )

    def render(self):
        a = self.assets

        selected_category = st.session_state.get("selected_category", 1)
        selected_question_index = st.session_state.get("selected_question_index", 1)
        current_points = st.session_state.get("current_points", 0)

        question_text, answers, correct_index = self.get_question_data(
            selected_category, selected_question_index
        )
        # Stash these so AnswerPage can display the result without
        # needing to re-derive/re-fetch anything.
        st.session_state["current_question_text"] = question_text
        st.session_state["current_question_answers"] = answers
        st.session_state["current_question_correct_index"] = correct_index

        # One hidden nav trigger per answer button, each capturing which
        # answer number it represents.
        for i in range(1, 4):
            def make_callback(answer_index):
                def callback():
                    st.session_state["selected_answer_index"] = answer_index
                    # TODO: hand off to backend (e.g.
                    # self.controller.submit_answer(answer_index)) once
                    # player_score_service is wired up to actually award
                    # points based on correct/incorrect.
                return callback

            self.render_nav_trigger(
                f"question_answer{i}", "answerPage",
                on_click=make_callback(i),
            )

        bg = a.get("QuestionBackground_0")
        question_box_img = a.get("QuestionTextBox_0")
        current_points_img = a.get("QuestionCurrentPoints_0")

        FRAME_W, FRAME_H = self.FRAME_W, self.FRAME_H
        qtb = self.QUESTION_TEXT_BOX
        cpb = self.CURRENT_POINTS_BOX

        answer_divs = ""
        answer_css = ""
        js_image_lookups = ""
        js_bind_calls = ""

        for i in range(1, 4):
            box = self.ANSWER_BOXES[i]
            unpressed = a.get(f"QuestionAnswer{i}button_0")
            pressed = a.get(f"QuestionAnswer{i}button_1")
            div_id = f"answer{i}-btn"
            text_id = f"answer{i}-text"
            answer_text = answers[i - 1] if i - 1 < len(answers) else ""

            answer_divs += f"""
                <div id="{div_id}" class="answer-hotspot"></div>
                <div id="{text_id}" class="answer-text">{_html.escape(answer_text)}</div>
            """
            answer_css += f"""
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
            js_image_lookups += f"""
                answerImages[{i}] = {{
                    unpressed: "data:image/png;base64,{unpressed}",
                    pressed: "data:image/png;base64,{pressed}"
                }};
            """
            js_bind_calls += f'{self.nav_trigger_js(f"question_answer{i}")}\n'
            js_bind_calls += f'bindAnswerButton("{div_id}", {i}, triggerNav_question_answer{i});\n'

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
            #question-text-layer {{
                position: absolute;
                left: {qtb["left_pct"]:.3f}%;
                top: {qtb["top_pct"]:.3f}%;
                width: {qtb["width_pct"]:.3f}%;
                height: {qtb["height_pct"]:.3f}%;
                background-image: url('data:image/png;base64,{question_box_img}');
                background-size: 100% 100%;
                image-rendering: pixelated;
                pointer-events: none;
            }}
            #question-text {{
                position: absolute;
                left: {qtb["left_pct"]:.3f}%;
                top: {qtb["top_pct"]:.3f}%;
                width: {qtb["width_pct"]:.3f}%;
                height: {qtb["height_pct"]:.3f}%;
                display: flex;
                align-items: center;
                justify-content: center;
                text-align: center;
                font-family: 'Press Start 2P', monospace;
                font-size: min(1.9vw, 11px);
                line-height: 1.4;
                color: #000000;
                pointer-events: none;
                padding: 5%;
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
                top: {cpb["top_pct"]:.3f}%;
                width: {cpb["width_pct"]:.3f}%;
                height: {cpb["height_pct"]:.3f}%;
                display: flex;
                align-items: flex-end;
                justify-content: center;
                text-align: center;
                font-family: 'Press Start 2P', monospace;
                font-size: min(1.8vw, 11px);
                color: #ffffff;
                pointer-events: none;
                padding-bottom: 12%;
                box-sizing: border-box;
            }}
            .answer-hotspot {{
                position: absolute;
                cursor: pointer;
                background-size: 100% 100%;
                image-rendering: pixelated;
            }}
            .answer-text {{
                position: absolute;
                display: flex;
                align-items: center;
                justify-content: center;
                text-align: center;
                font-family: 'Press Start 2P', monospace;
                font-size: min(2vw, 12px);
                color: #000000;
                pointer-events: none;
                padding: 3%;
                box-sizing: border-box;
            }}
            {answer_css}
        </style>

        <div id="stage-wrap">
            <div id="stage">
                <div id="bg-layer"></div>
                <div id="question-text-layer"></div>
                <div id="question-text">{_html.escape(question_text)}</div>
                {answer_divs}
                <div id="current-points-layer"></div>
                <div id="current-points-text">{current_points}</div>
            </div>
        </div>

        <script>
            const answerImages = {{}};
            {js_image_lookups}

            function bindAnswerButton(elementId, aNum, triggerNavFn) {{
                const el = document.getElementById(elementId);
                let isPressed = false;

                el.addEventListener("pointerdown", (e) => {{
                    isPressed = true;
                    el.style.backgroundImage = "url('" + answerImages[aNum].pressed + "')";
                    el.setPointerCapture(e.pointerId);
                }});
                el.addEventListener("pointerup", () => {{
                    if (!isPressed) return;
                    isPressed = false;
                    el.style.backgroundImage = "url('" + answerImages[aNum].unpressed + "')";
                    triggerNavFn();
                }});
                el.addEventListener("pointerleave", () => {{
                    if (!isPressed) return;
                    isPressed = false;
                    el.style.backgroundImage = "url('" + answerImages[aNum].unpressed + "')";
                }});
                el.addEventListener("pointercancel", () => {{
                    isPressed = false;
                    el.style.backgroundImage = "url('" + answerImages[aNum].unpressed + "')";
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