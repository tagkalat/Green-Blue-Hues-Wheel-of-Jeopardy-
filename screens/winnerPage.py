import html as _html

import streamlit as st
import streamlit.components.v1 as components

from screens.basePage import BasePage


class WinnerPage(BasePage):
    """
    End-of-game standings. Winner's name + points show in the two green
    boxes at top; the 3 red boxes show 2nd/3rd/4th place (most points
    first, left to right), each with "Player N" on top and their points
    below, stacked within the same box. Only as many red boxes are shown
    as there are actual losers (player_count - 1).
    """

    FRAME_W, FRAME_H = 480, 270

    WINNER_NAME_BOX = {
        "left_pct": 34.375, "top_pct": 18.889, "width_pct": 31.25, "height_pct": 15.185,
    }
    WINNER_POINTS_BOX = {
        "left_pct": 37.5, "top_pct": 36.667, "width_pct": 25.0, "height_pct": 12.963,
    }
    # 1 = leftmost (2nd place), 2 = middle (3rd place), 3 = rightmost (4th place)
    LOSER_BOXES = {
        1: {"left_pct": 12.5, "top_pct": 53.704, "width_pct": 20.833, "height_pct": 24.815},
        2: {"left_pct": 39.583, "top_pct": 53.704, "width_pct": 20.833, "height_pct": 24.815},
        3: {"left_pct": 66.667, "top_pct": 53.704, "width_pct": 20.833, "height_pct": 24.815},
    }
    MAIN_MENU_BOX = {
        "left_pct": 38.333, "top_pct": 80.741, "width_pct": 23.333, "height_pct": 17.407,
    }
    # Pressed-frame art is a different real size than unpressed - swap
    # geometry too, not just the image, or it stretches instead of squishing.
    MAIN_MENU_BOX_PRESSED = {
        "left_pct": 38.333, "top_pct": 83.333, "width_pct": 23.333, "height_pct": 14.815,
    }

    def __init__(self):
        super().__init__("WinnerPage")

    @staticmethod
    def get_final_standings():
        """
        Placeholder final standings - swap for real tracked per-player
        scores (e.g. self.controller.get_final_standings()) once
        player_score_service actually tracks scores per player rather
        than a single shared current_points value. Returns a list of
        {"player": N, "points": X} dicts, sorted highest points first,
        one entry per player (player_count).
        """
        if "final_standings" in st.session_state:
            return st.session_state["final_standings"]

        player_count = st.session_state.get("player_count", 4)
        try:
            player_count = int(player_count)
        except (TypeError, ValueError):
            player_count = 4
        player_count = max(1, min(player_count, 4))

        # Dummy descending placeholder scores just so the layout is
        # testable before real scoring exists.
        placeholder_points = [1000, 700, 400, 100]
        standings = [
            {"player": i + 1, "points": placeholder_points[i]}
            for i in range(player_count)
        ]
        return standings

    def render(self):
        a = self.assets

        standings = self.get_final_standings()
        winner = standings[0] if standings else {"player": 1, "points": 0}
        losers = standings[1:4]  # up to 3 losers (2nd, 3rd, 4th place)

        self.render_nav_trigger("winner_main_menu", "title")

        bg = a.get("WinnerPageBackground_0")
        winner_name_box_img = a.get("WinnerPlayerTextBox_0")
        winner_points_box_img = a.get("WinnerPoints_0")
        main_menu_unpressed = a.get("MainMenuButton_0")
        main_menu_pressed = a.get("MainMenuButton_1")

        loser_asset_names = {1: "Loser1AndPoints_0", 2: "Loser2AndPoints_0", 3: "Loser3AndPoints_0"}

        FRAME_W, FRAME_H = self.FRAME_W, self.FRAME_H
        wnb = self.WINNER_NAME_BOX
        wpb = self.WINNER_POINTS_BOX
        mmb = self.MAIN_MENU_BOX
        mmbp = self.MAIN_MENU_BOX_PRESSED

        loser_divs = ""
        loser_css = ""
        for i, loser in enumerate(losers, start=1):
            box = self.LOSER_BOXES[i]
            box_img = a.get(loser_asset_names[i])
            # Split the box into two explicit sub-regions rather than
            # using percentage padding to nudge text up/down - padding-top/
            # bottom percentages resolve against WIDTH, not height (a real
            # CSS spec quirk), which was blowing the text elements way
            # past the box's actual height.
            top_half_top = box["top_pct"] + 0.06 * box["height_pct"]
            top_half_height = 0.40 * box["height_pct"]
            bottom_half_top = box["top_pct"] + 0.54 * box["height_pct"]
            bottom_half_height = 0.40 * box["height_pct"]

            loser_divs += f"""
                <div class="loser-box-layer" style="
                    left: {box["left_pct"]:.3f}%; top: {box["top_pct"]:.3f}%;
                    width: {box["width_pct"]:.3f}%; height: {box["height_pct"]:.3f}%;
                    background-image: url('data:image/png;base64,{box_img}');
                "></div>
                <div class="loser-text" style="
                    left: {box["left_pct"]:.3f}%; top: {top_half_top:.3f}%;
                    width: {box["width_pct"]:.3f}%; height: {top_half_height:.3f}%;
                ">Player {loser["player"]}</div>
                <div class="loser-text" style="
                    left: {box["left_pct"]:.3f}%; top: {bottom_half_top:.3f}%;
                    width: {box["width_pct"]:.3f}%; height: {bottom_half_height:.3f}%;
                ">{loser["points"]}</div>
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
            #winner-name-layer {{
                position: absolute;
                left: {wnb["left_pct"]:.3f}%; top: {wnb["top_pct"]:.3f}%;
                width: {wnb["width_pct"]:.3f}%; height: {wnb["height_pct"]:.3f}%;
                background-image: url('data:image/png;base64,{winner_name_box_img}');
                background-size: 100% 100%;
                image-rendering: pixelated;
                pointer-events: none;
            }}
            #winner-name-text {{
                position: absolute;
                left: {wnb["left_pct"]:.3f}%; top: {wnb["top_pct"]:.3f}%;
                width: {wnb["width_pct"]:.3f}%; height: {wnb["height_pct"]:.3f}%;
                display: flex; align-items: center; justify-content: center;
                text-align: center;
                font-family: 'Press Start 2P', monospace;
                font-size: min(2.6vw, 15px);
                color: #000000;
                pointer-events: none;
            }}
            #winner-points-layer {{
                position: absolute;
                left: {wpb["left_pct"]:.3f}%; top: {wpb["top_pct"]:.3f}%;
                width: {wpb["width_pct"]:.3f}%; height: {wpb["height_pct"]:.3f}%;
                background-image: url('data:image/png;base64,{winner_points_box_img}');
                background-size: 100% 100%;
                image-rendering: pixelated;
                pointer-events: none;
            }}
            #winner-points-text {{
                position: absolute;
                left: {wpb["left_pct"]:.3f}%; top: {wpb["top_pct"]:.3f}%;
                width: {wpb["width_pct"]:.3f}%; height: {wpb["height_pct"]:.3f}%;
                display: flex; align-items: center; justify-content: center;
                text-align: center;
                font-family: 'Press Start 2P', monospace;
                font-size: min(2.4vw, 14px);
                color: #000000;
                pointer-events: none;
            }}
            .loser-box-layer {{
                position: absolute;
                background-size: 100% 100%;
                image-rendering: pixelated;
                pointer-events: none;
            }}
            .loser-text {{
                position: absolute;
                display: flex;
                align-items: center;
                justify-content: center;
                text-align: center;
                font-family: 'Press Start 2P', monospace;
                font-size: min(1.9vw, 11px);
                color: #1a1a1a;
                pointer-events: none;
                box-sizing: border-box;
            }}
            #main-menu-btn {{
                position: absolute;
                left: {mmb["left_pct"]:.3f}%; top: {mmb["top_pct"]:.3f}%;
                width: {mmb["width_pct"]:.3f}%; height: {mmb["height_pct"]:.3f}%;
                cursor: pointer;
                background-size: 100% 100%;
                image-rendering: pixelated;
                background-image: url('data:image/png;base64,{main_menu_unpressed}');
            }}
        </style>

        <div id="stage-wrap">
            <div id="stage">
                <div id="bg-layer"></div>
                <div id="winner-name-layer"></div>
                <div id="winner-name-text">{_html.escape(f"Player {winner['player']}")}</div>
                <div id="winner-points-layer"></div>
                <div id="winner-points-text">{winner['points']}</div>
                {loser_divs}
                <div id="main-menu-btn"></div>
            </div>
        </div>

        <script>
            {self.nav_trigger_js("winner_main_menu")}
            const mmUnpressedImg = "data:image/png;base64,{main_menu_unpressed}";
            const mmPressedImg = "data:image/png;base64,{main_menu_pressed}";
            const mmBtn = document.getElementById("main-menu-btn");
            let isMmPressed = false;

            mmBtn.addEventListener("pointerdown", (e) => {{
                isMmPressed = true;
                mmBtn.style.backgroundImage = "url('" + mmPressedImg + "')";
                mmBtn.style.left = "{mmbp["left_pct"]:.3f}%";
                mmBtn.style.top = "{mmbp["top_pct"]:.3f}%";
                mmBtn.style.width = "{mmbp["width_pct"]:.3f}%";
                mmBtn.style.height = "{mmbp["height_pct"]:.3f}%";
                mmBtn.setPointerCapture(e.pointerId);
            }});
            mmBtn.addEventListener("pointerup", () => {{
                if (!isMmPressed) return;
                isMmPressed = false;
                mmBtn.style.backgroundImage = "url('" + mmUnpressedImg + "')";
                mmBtn.style.left = "{mmb["left_pct"]:.3f}%";
                mmBtn.style.top = "{mmb["top_pct"]:.3f}%";
                mmBtn.style.width = "{mmb["width_pct"]:.3f}%";
                mmBtn.style.height = "{mmb["height_pct"]:.3f}%";
                triggerNav_winner_main_menu();
            }});
            mmBtn.addEventListener("pointerleave", () => {{
                if (!isMmPressed) return;
                isMmPressed = false;
                mmBtn.style.backgroundImage = "url('" + mmUnpressedImg + "')";
                mmBtn.style.left = "{mmb["left_pct"]:.3f}%";
                mmBtn.style.top = "{mmb["top_pct"]:.3f}%";
                mmBtn.style.width = "{mmb["width_pct"]:.3f}%";
                mmBtn.style.height = "{mmb["height_pct"]:.3f}%";
            }});
            mmBtn.addEventListener("pointercancel", () => {{
                isMmPressed = false;
                mmBtn.style.backgroundImage = "url('" + mmUnpressedImg + "')";
                mmBtn.style.left = "{mmb["left_pct"]:.3f}%";
                mmBtn.style.top = "{mmb["top_pct"]:.3f}%";
                mmBtn.style.width = "{mmb["width_pct"]:.3f}%";
                mmBtn.style.height = "{mmb["height_pct"]:.3f}%";
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