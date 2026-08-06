import html as _html

import streamlit as st
import streamlit.components.v1 as components

from screens.basePage import BasePage


class AnswerPage(BasePage):
    """
    Shows what the player selected vs. the actual correct answer, and
    updates their points accordingly (+points if correct, -points if
    wrong). If they got it wrong AND have a free spin token available,
    offers a bonus "Use Free Spin?" prompt (Yes = spin again immediately,
    No = continue normally). Otherwise the whole page is click-anywhere
    to continue, same pattern as FreeSpinPage/BankruptPage.
    """

    FRAME_W, FRAME_H = 480, 270

    SELECTED_BOX = {
        "left_pct": 14.583, "top_pct": 0.0, "width_pct": 69.792, "height_pct": 30.741,
    }
    CORRECT_BOX = {
        "left_pct": 16.667, "top_pct": 32.593, "width_pct": 65.625, "height_pct": 30.741,
    }
    CURRENT_POINTS_BOX = {
        "left_pct": 81.458, "top_pct": 79.630, "width_pct": 17.083, "height_pct": 16.667,
    }
    FREE_SPIN_PROMPT_BOX = {
        "left_pct": 23.125, "top_pct": 64.815, "width_pct": 52.292, "height_pct": 16.667,
    }
    YES_BOX = {
        "left_pct": 37.5, "top_pct": 83.333, "width_pct": 7.708, "height_pct": 12.963,
    }
    NO_BOX = {
        "left_pct": 54.792, "top_pct": 83.333, "width_pct": 7.708, "height_pct": 12.963,
    }

    def __init__(self):
        super().__init__("AnswerPage")

    def render(self):
        a = self.assets

        answers = st.session_state.get("current_question_answers", ["", "", ""])
        selected_index = st.session_state.get("selected_answer_index", 1)
        correct_index = st.session_state.get("current_question_correct_index", 1)
        point_value = st.session_state.get("selected_point_value", 0)

        selected_text = answers[selected_index - 1] if selected_index - 1 < len(answers) else ""
        correct_text = answers[correct_index - 1] if correct_index - 1 < len(answers) else ""

        is_correct = selected_index == correct_index

        # Award/deduct points - only do this once per visit (not on every
        # rerun), otherwise repeated interactions on this same page (e.g.
        # a resize-triggered rerun) would double-apply the score change.
        if not st.session_state.get("_answer_points_applied_this_visit"):
            if is_correct:
                st.session_state["current_points"] = st.session_state.get("current_points", 0) + point_value
            else:
                st.session_state["current_points"] = st.session_state.get("current_points", 0) - point_value
            st.session_state["_answer_points_applied_this_visit"] = True
            # TODO: hand off to backend (e.g.
            # self.controller.apply_answer_result(is_correct, point_value))
            # once player_score_service is wired up.

        current_points = st.session_state.get("current_points", 0)
        has_free_spin = st.session_state.get("free_spin_tokens", 0) > 0
        show_free_spin_prompt = (not is_correct) and has_free_spin

        def use_free_spin_and_continue():
            st.session_state["free_spin_tokens"] = max(0, st.session_state.get("free_spin_tokens", 0) - 1)
            st.session_state["_answer_points_applied_this_visit"] = False  # reset for next visit to this page
            # TODO: hand off to backend (e.g. self.controller.use_free_spin())
            # once player_score_service is wired up.

        def continue_normally():
            st.session_state["_answer_points_applied_this_visit"] = False  # reset for next visit to this page

        if show_free_spin_prompt:
            self.render_nav_trigger("answer_freespin_yes", "wheel", on_click=use_free_spin_and_continue)
            self.render_nav_trigger("answer_freespin_no", "wheel", on_click=continue_normally)
        else:
            self.render_nav_trigger("answer_continue", "wheel", on_click=continue_normally)

        bg = a.get("AnswerPageBackground_0")
        selected_box_img = a.get("AnswerPageAnswerSelectedBox_0")
        correct_box_img = a.get("AnswerPageAnswerCorrectBox_0")
        current_points_img = a.get("AnswerPageCurrentPoints_0")

        FRAME_W, FRAME_H = self.FRAME_W, self.FRAME_H
        sb = self.SELECTED_BOX
        cb = self.CORRECT_BOX
        cpb = self.CURRENT_POINTS_BOX
        fpb = self.FREE_SPIN_PROMPT_BOX
        yb = self.YES_BOX
        nb = self.NO_BOX

        free_spin_html = ""
        free_spin_css = ""
        free_spin_js = ""
        click_anywhere_html = ""
        click_anywhere_js = ""

        if show_free_spin_prompt:
            free_spin_img = a.get("AnswerPageFreeSpin_0")
            yes_unpressed = a.get("AnswerPageFreeSpinYesButton_0")
            yes_pressed = a.get("AnswerPageFreeSpinYesButton_1")
            no_unpressed = a.get("AnswerPageFreeSpinNoButton_0")
            no_pressed = a.get("AnswerPageFreeSpinNoButton_1")

            free_spin_html = f"""
                <div id="freespin-prompt-layer"></div>
                <div id="yes-btn"></div>
                <div id="no-btn"></div>
            """
            free_spin_css = f"""
                #freespin-prompt-layer {{
                    position: absolute;
                    left: {fpb["left_pct"]:.3f}%;
                    top: {fpb["top_pct"]:.3f}%;
                    width: {fpb["width_pct"]:.3f}%;
                    height: {fpb["height_pct"]:.3f}%;
                    background-image: url('data:image/png;base64,{free_spin_img}');
                    background-size: 100% 100%;
                    image-rendering: pixelated;
                    pointer-events: none;
                }}
                #yes-btn {{
                    position: absolute;
                    left: {yb["left_pct"]:.3f}%;
                    top: {yb["top_pct"]:.3f}%;
                    width: {yb["width_pct"]:.3f}%;
                    height: {yb["height_pct"]:.3f}%;
                    cursor: pointer;
                    background-size: 100% 100%;
                    image-rendering: pixelated;
                    background-image: url('data:image/png;base64,{yes_unpressed}');
                }}
                #no-btn {{
                    position: absolute;
                    left: {nb["left_pct"]:.3f}%;
                    top: {nb["top_pct"]:.3f}%;
                    width: {nb["width_pct"]:.3f}%;
                    height: {nb["height_pct"]:.3f}%;
                    cursor: pointer;
                    background-size: 100% 100%;
                    image-rendering: pixelated;
                    background-image: url('data:image/png;base64,{no_unpressed}');
                }}
            """
            free_spin_js = f"""
                {self.nav_trigger_js("answer_freespin_yes")}
                {self.nav_trigger_js("answer_freespin_no")}

                const yesUnpressedImg = "data:image/png;base64,{yes_unpressed}";
                const yesPressedImg = "data:image/png;base64,{yes_pressed}";
                const yesBtn = document.getElementById("yes-btn");
                let isYesPressed = false;
                yesBtn.addEventListener("pointerdown", (e) => {{
                    isYesPressed = true;
                    yesBtn.style.backgroundImage = "url('" + yesPressedImg + "')";
                    yesBtn.setPointerCapture(e.pointerId);
                }});
                yesBtn.addEventListener("pointerup", () => {{
                    if (!isYesPressed) return;
                    isYesPressed = false;
                    yesBtn.style.backgroundImage = "url('" + yesUnpressedImg + "')";
                    triggerNav_answer_freespin_yes();
                }});
                yesBtn.addEventListener("pointerleave", () => {{
                    if (!isYesPressed) return;
                    isYesPressed = false;
                    yesBtn.style.backgroundImage = "url('" + yesUnpressedImg + "')";
                }});
                yesBtn.addEventListener("pointercancel", () => {{
                    isYesPressed = false;
                    yesBtn.style.backgroundImage = "url('" + yesUnpressedImg + "')";
                }});

                const noUnpressedImg = "data:image/png;base64,{no_unpressed}";
                const noPressedImg = "data:image/png;base64,{no_pressed}";
                const noBtn = document.getElementById("no-btn");
                let isNoPressed = false;
                noBtn.addEventListener("pointerdown", (e) => {{
                    isNoPressed = true;
                    noBtn.style.backgroundImage = "url('" + noPressedImg + "')";
                    noBtn.setPointerCapture(e.pointerId);
                }});
                noBtn.addEventListener("pointerup", () => {{
                    if (!isNoPressed) return;
                    isNoPressed = false;
                    noBtn.style.backgroundImage = "url('" + noUnpressedImg + "')";
                    triggerNav_answer_freespin_no();
                }});
                noBtn.addEventListener("pointerleave", () => {{
                    if (!isNoPressed) return;
                    isNoPressed = false;
                    noBtn.style.backgroundImage = "url('" + noUnpressedImg + "')";
                }});
                noBtn.addEventListener("pointercancel", () => {{
                    isNoPressed = false;
                    noBtn.style.backgroundImage = "url('" + noUnpressedImg + "')";
                }});
            """
        else:
            click_anywhere_html = '<div id="click-anywhere"></div>'
            click_anywhere_js = f"""
                {self.nav_trigger_js("answer_continue")}
                document.getElementById("click-anywhere").addEventListener("click", () => {{
                    triggerNav_answer_continue();
                }});
            """

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
            #selected-box-layer {{
                position: absolute;
                left: {sb["left_pct"]:.3f}%;
                top: {sb["top_pct"]:.3f}%;
                width: {sb["width_pct"]:.3f}%;
                height: {sb["height_pct"]:.3f}%;
                background-image: url('data:image/png;base64,{selected_box_img}');
                background-size: 100% 100%;
                image-rendering: pixelated;
                pointer-events: none;
            }}
            #selected-text {{
                position: absolute;
                left: {sb["left_pct"]:.3f}%;
                top: 17.037%;
                width: {sb["width_pct"]:.3f}%;
                height: 12.593%;
                display: flex;
                align-items: center;
                justify-content: center;
                text-align: center;
                font-family: 'Press Start 2P', monospace;
                font-size: min(2.2vw, 13px);
                line-height: 1.2;
                color: #000000;
                pointer-events: none;
                padding: 2% 8%;
                box-sizing: border-box;
            }}
            #correct-box-layer {{
                position: absolute;
                left: {cb["left_pct"]:.3f}%;
                top: {cb["top_pct"]:.3f}%;
                width: {cb["width_pct"]:.3f}%;
                height: {cb["height_pct"]:.3f}%;
                background-image: url('data:image/png;base64,{correct_box_img}');
                background-size: 100% 100%;
                image-rendering: pixelated;
                pointer-events: none;
            }}
            #correct-text {{
                position: absolute;
                left: {cb["left_pct"]:.3f}%;
                top: 49.630%;
                width: {cb["width_pct"]:.3f}%;
                height: 12.593%;
                display: flex;
                align-items: center;
                justify-content: center;
                text-align: center;
                font-family: 'Press Start 2P', monospace;
                font-size: min(2.2vw, 13px);
                line-height: 1.2;
                color: #000000;
                pointer-events: none;
                padding: 2% 8%;
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
            #click-anywhere {{
                position: absolute;
                inset: 0;
                cursor: pointer;
            }}
            {free_spin_css}
        </style>

        <div id="stage-wrap">
            <div id="stage">
                <div id="bg-layer"></div>
                <div id="selected-box-layer"></div>
                <div id="selected-text">{_html.escape(selected_text)}</div>
                <div id="correct-box-layer"></div>
                <div id="correct-text">{_html.escape(correct_text)}</div>
                <div id="current-points-layer"></div>
                <div id="current-points-text">{current_points}</div>
                {free_spin_html}
                {click_anywhere_html}
            </div>
        </div>

        <script>
            {free_spin_js}
            {click_anywhere_js}

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