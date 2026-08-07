import streamlit as st
import streamlit.components.v1 as components

from screens.basePage import BasePage


class LostTurnPage(BasePage):
    """
    Shown when the wheel lands on "Lose a Turn". If the player has a free
    spin token, they can choose to use one to spin again (Yes) instead of
    losing their turn; otherwise only "No" (turn passes) is offered.
    """

    FRAME_W, FRAME_H = 480, 270

    IF_FREE_SPIN_BOX = {
        "left_pct": 15.625, "top_pct": 45.926,
        "width_pct": 68.75, "height_pct": 21.111,
    }
    YES_BOX = {
        "left_pct": 37.5, "top_pct": 71.852,
        "width_pct": 7.708, "height_pct": 12.963,
    }
    NO_BOX = {
        "left_pct": 54.792, "top_pct": 71.852,
        "width_pct": 7.708, "height_pct": 12.963,
    }
    # Pressed-frame art is a different real size (shorter) than unpressed -
    # that's what makes it look "pressed down". Swap geometry too, not
    # just the image, or the pressed art stretches instead of squishing.
    YES_BOX_PRESSED = {
        "left_pct": 37.5, "top_pct": 73.704,
        "width_pct": 7.708, "height_pct": 11.111,
    }
    NO_BOX_PRESSED = {
        "left_pct": 54.792, "top_pct": 73.704,
        "width_pct": 7.708, "height_pct": 11.111,
    }

    def __init__(self):
        super().__init__("LostTurnPage")

    def render(self):
        a = self.assets

        has_free_spin = st.session_state.get("free_spin_tokens", 0) > 0

        def use_free_spin_and_continue():
            st.session_state["free_spin_tokens"] = max(0, st.session_state.get("free_spin_tokens", 0) - 1)
            # TODO: hand off to backend (e.g. self.controller.use_free_spin())
            # once player_score_service is wired up.

        if has_free_spin:
            self.render_nav_trigger("lostturn_yes", "wheel", on_click=use_free_spin_and_continue)
        # "No" always passes the turn and returns to the wheel.
        # TODO: actual turn-passing logic (advancing to next player) once
        # game_controller/player_score_service can track whose turn it is.
        self.render_nav_trigger("lostturn_no", "wheel")

        bg = a.get("LostTurnPage_0")
        if_free_spin = a.get("IfFreeSpin_0")
        yes_unpressed = a.get("YesButton_0")
        yes_pressed = a.get("YesButton_1")
        no_unpressed = a.get("NoButton_0")
        no_pressed = a.get("NoButton_1")

        FRAME_W, FRAME_H = self.FRAME_W, self.FRAME_H
        ifb = self.IF_FREE_SPIN_BOX
        yb = self.YES_BOX
        nb = self.NO_BOX
        ybp = self.YES_BOX_PRESSED
        nbp = self.NO_BOX_PRESSED

        yes_button_html = f'<div id="yes-btn"></div>' if has_free_spin else ""
        yes_button_css = f"""
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
        """ if has_free_spin else ""

        # Yes button JS only included when it's actually shown, so we're
        # not calling triggerNav functions/binding listeners for hidden
        # elements that don't exist in the DOM.
        yes_button_js = f"""
            {self.nav_trigger_js("lostturn_yes")}
            const yesUnpressedImg = "data:image/png;base64,{yes_unpressed}";
            const yesPressedImg = "data:image/png;base64,{yes_pressed}";
            const yesBtn = document.getElementById("yes-btn");
            let isYesPressed = false;

            yesBtn.addEventListener("pointerdown", (e) => {{
                isYesPressed = true;
                yesBtn.style.backgroundImage = "url('" + yesPressedImg + "')";
                yesBtn.style.left = "{ybp["left_pct"]:.3f}%";
                yesBtn.style.top = "{ybp["top_pct"]:.3f}%";
                yesBtn.style.width = "{ybp["width_pct"]:.3f}%";
                yesBtn.style.height = "{ybp["height_pct"]:.3f}%";
                yesBtn.setPointerCapture(e.pointerId);
            }});
            yesBtn.addEventListener("pointerup", () => {{
                if (!isYesPressed) return;
                isYesPressed = false;
                yesBtn.style.backgroundImage = "url('" + yesUnpressedImg + "')";
                yesBtn.style.left = "{yb["left_pct"]:.3f}%";
                yesBtn.style.top = "{yb["top_pct"]:.3f}%";
                yesBtn.style.width = "{yb["width_pct"]:.3f}%";
                yesBtn.style.height = "{yb["height_pct"]:.3f}%";
                triggerNav_lostturn_yes();
            }});
            yesBtn.addEventListener("pointerleave", () => {{
                if (!isYesPressed) return;
                isYesPressed = false;
                yesBtn.style.backgroundImage = "url('" + yesUnpressedImg + "')";
                yesBtn.style.left = "{yb["left_pct"]:.3f}%";
                yesBtn.style.top = "{yb["top_pct"]:.3f}%";
                yesBtn.style.width = "{yb["width_pct"]:.3f}%";
                yesBtn.style.height = "{yb["height_pct"]:.3f}%";
            }});
            yesBtn.addEventListener("pointercancel", () => {{
                isYesPressed = false;
                yesBtn.style.backgroundImage = "url('" + yesUnpressedImg + "')";
                yesBtn.style.left = "{yb["left_pct"]:.3f}%";
                yesBtn.style.top = "{yb["top_pct"]:.3f}%";
                yesBtn.style.width = "{yb["width_pct"]:.3f}%";
                yesBtn.style.height = "{yb["height_pct"]:.3f}%";
            }});
        """ if has_free_spin else ""

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
            #iffreespin-layer {{
                position: absolute;
                left: {ifb["left_pct"]:.3f}%;
                top: {ifb["top_pct"]:.3f}%;
                width: {ifb["width_pct"]:.3f}%;
                height: {ifb["height_pct"]:.3f}%;
                background-image: url('data:image/png;base64,{if_free_spin}');
                background-size: 100% 100%;
                image-rendering: pixelated;
                pointer-events: none;
            }}
            {yes_button_css}
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
        </style>

        <div id="stage-wrap">
            <div id="stage">
                <div id="bg-layer"></div>
                <div id="iffreespin-layer"></div>
                {yes_button_html}
                <div id="no-btn"></div>
            </div>
        </div>

        <script>
            {yes_button_js}

            {self.nav_trigger_js("lostturn_no")}
            const noUnpressedImg = "data:image/png;base64,{no_unpressed}";
            const noPressedImg = "data:image/png;base64,{no_pressed}";
            const noBtn = document.getElementById("no-btn");
            let isNoPressed = false;

            noBtn.addEventListener("pointerdown", (e) => {{
                isNoPressed = true;
                noBtn.style.backgroundImage = "url('" + noPressedImg + "')";
                noBtn.style.left = "{nbp["left_pct"]:.3f}%";
                noBtn.style.top = "{nbp["top_pct"]:.3f}%";
                noBtn.style.width = "{nbp["width_pct"]:.3f}%";
                noBtn.style.height = "{nbp["height_pct"]:.3f}%";
                noBtn.setPointerCapture(e.pointerId);
            }});
            noBtn.addEventListener("pointerup", () => {{
                if (!isNoPressed) return;
                isNoPressed = false;
                noBtn.style.backgroundImage = "url('" + noUnpressedImg + "')";
                noBtn.style.left = "{nb["left_pct"]:.3f}%";
                noBtn.style.top = "{nb["top_pct"]:.3f}%";
                noBtn.style.width = "{nb["width_pct"]:.3f}%";
                noBtn.style.height = "{nb["height_pct"]:.3f}%";
                triggerNav_lostturn_no();
            }});
            noBtn.addEventListener("pointerleave", () => {{
                if (!isNoPressed) return;
                isNoPressed = false;
                noBtn.style.backgroundImage = "url('" + noUnpressedImg + "')";
                noBtn.style.left = "{nb["left_pct"]:.3f}%";
                noBtn.style.top = "{nb["top_pct"]:.3f}%";
                noBtn.style.width = "{nb["width_pct"]:.3f}%";
                noBtn.style.height = "{nb["height_pct"]:.3f}%";
            }});
            noBtn.addEventListener("pointercancel", () => {{
                isNoPressed = false;
                noBtn.style.backgroundImage = "url('" + noUnpressedImg + "')";
                noBtn.style.left = "{nb["left_pct"]:.3f}%";
                noBtn.style.top = "{nb["top_pct"]:.3f}%";
                noBtn.style.width = "{nb["width_pct"]:.3f}%";
                noBtn.style.height = "{nb["height_pct"]:.3f}%";
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