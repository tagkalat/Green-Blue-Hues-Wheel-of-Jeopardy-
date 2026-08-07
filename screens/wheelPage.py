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

    # Placeholder category names for the 6 category sectors - swap these
    # for real data from question_repository once it's wired up. The 5
    # fixed outcome sectors are interleaved with them below. Order/sector
    # assignment is arbitrary for now (no art-tied mapping exists yet) -
    # reorder this list any time to match the actual wheel art.
    SECTOR_LABELS = [
        "Category 1",
        "Category 2",
        "Free Spin",
        "Category 3",
        "Lose Turn",
        "Category 4",
        "Bankruptcy",
        "Category 5",
        "Player's",
        "Category 6",
        "Opponent's",
    ]

    # Where each sector actually navigates to, matched index-for-index
    # with SECTOR_LABELS above. Category sectors carry which category
    # number to select; the 5 fixed sectors don't need extra data.
    # Keys must exactly match app.py's PAGES dict.
    SECTOR_DESTINATIONS = [
        ("categoryPage", 1),          # 0: Category 1
        ("categoryPage", 2),          # 1: Category 2
        ("freeSpinPage", None),       # 2: Free Spin
        ("categoryPage", 3),          # 3: Category 3
        ("lostTurnPage", None),       # 4: Lose Turn
        ("categoryPage", 4),          # 5: Category 4
        ("bankruptPage", None),       # 6: Bankruptcy
        ("categoryPage", 5),          # 7: Category 5
        ("playersChoicePage", None),  # 8: Player's Choice
        ("categoryPage", 6),          # 9: Category 6
        ("opponentChoicePage", None), # 10: Opponent's Choice
    ]

    # How far out from the wheel's center each label sits, as a percent
    # of the wheel's own radius. 63.5% sits within the colored sector
    # ring (between the hub and the outer rim).
    LABEL_RADIUS_PCT = 63.5

    # Wheel graphic's own box on the stage (from positions_manifest.json).
    # Rotation is applied to this element directly, around its own center,
    # so its position on the page never needs to change - only its
    # internal rotation angle does.
    WHEEL_BOX = {"left_pct": 23.333, "top_pct": 2.963, "width_pct": 53.333, "height_pct": 94.074}

    def __init__(self):
        super().__init__("wheel")

    def render(self):
        a = self.assets
        import html as _html

        # One hidden nav trigger per sector, so the spin-completion JS can
        # fire whichever one matches the sector that was actually landed
        # on. Category sectors also set selected_category before navigating.
        for sector_i, (target_page, category_num) in enumerate(self.SECTOR_DESTINATIONS):
            def make_callback(cat_num):
                def callback():
                    if cat_num is not None:
                        st.session_state["selected_category"] = cat_num
                return callback

            self.render_nav_trigger(
                f"wheel_sector{sector_i}", target_page,
                on_click=make_callback(category_num),
            )

        # Dynamic HUD values - read from session_state with sensible
        # defaults, so this page is already "wired up": once your game
        # logic sets these session_state keys elsewhere (e.g. after each
        # spin, or when a turn changes), this page reflects them
        # automatically with zero further changes needed here.
        player_number_display = st.session_state.get("current_player_number", 1)
        spins_left_display = st.session_state.get("spins_left", 30)  # 30 per round, backend decrements
        free_spin_tokens_display = st.session_state.get("free_spin_tokens", 0)
        current_points_display = st.session_state.get("current_points", 0)

        # Static (non-spinning) layers - background, pointer, HUD elements
        static_layers = [
            ("wheelBackground_0", {"left_pct": 0, "top_pct": 0, "width_pct": 100, "height_pct": 100}),
            ("wheelPlayerTurn_0", {"left_pct": 3.125, "top_pct": 2.963, "width_pct": 20.625, "height_pct": 19.259}),
            ("wheelSpinsLeft_0", {"left_pct": 85.417, "top_pct": 5.556, "width_pct": 7.708, "height_pct": 13.333}),
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

        # Text readouts overlaid on top of their matching box art. Reuses
        # the same box coordinates as the underlying static layer so the
        # text sits centered within each box automatically.
        hud_readouts = [
            ("hud-player", static_layers[1][1], f"Player {player_number_display}"),
            ("hud-spins-left", static_layers[2][1], str(spins_left_display)),
            ("hud-free-spin-tokens", static_layers[3][1], str(free_spin_tokens_display)),
            ("hud-current-points", static_layers[4][1], str(current_points_display)),
        ]
        hud_divs = ""
        hud_css = ""
        for div_id, box, text in hud_readouts:
            hud_divs += f'<div class="hud-readout" id="{div_id}">{_html.escape(text)}</div>\n'
            hud_css += f"""
                #{div_id} {{
                    left: {box["left_pct"]:.3f}%;
                    top: {box["top_pct"]:.3f}%;
                    width: {box["width_pct"]:.3f}%;
                    height: {box["height_pct"]:.3f}%;
                }}
            """

        # Build one rotated label per sector. Each is a full-size wrapper
        # (same size as the wheel graphic) rotated to that sector's angle,
        # with the actual text positioned near the top of that wrapper -
        # i.e. at LABEL_RADIUS_PCT "up" from center, before rotation
        # carries it around to the correct clock position. Because these
        # divs live INSIDE #wheel-graphic, they inherit its transform
        # automatically during the spin animation - no extra JS needed.
        sector_angle = 360 / self.NUM_SECTORS
        # LABEL_RADIUS_PCT is "percent of the wheel's RADIUS" (half the
        # box height/width). CSS `top` percentages are relative to the
        # FULL height though, so converting radius-fraction -> top-percent
        # needs a /2: top_pct = 50 - (radius_pct / 2), not 50 - radius_pct.
        top_offset_pct = 50 - (self.LABEL_RADIUS_PCT / 2)

        label_divs = ""
        for i in range(self.NUM_SECTORS):
            angle = i * sector_angle
            text = _html.escape(self.SECTOR_LABELS[i]) if i < len(self.SECTOR_LABELS) else ""
            label_divs += f"""
            <div class="sector-label" style="transform: rotate({angle:.3f}deg);">
                <div class="sector-label-text" style="top: {top_offset_pct:.3f}%;">{text}</div>
            </div>
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
            .layer {{ position: absolute; image-rendering: pixelated; }}
            {static_css}

            .hud-readout {{
                position: absolute;
                display: flex;
                align-items: center;
                justify-content: center;
                text-align: center;
                font-family: 'Press Start 2P', monospace;
                font-size: min(2.2vw, 13px);
                color: #1a1a1a;
                pointer-events: none;
                padding: 4%;
                box-sizing: border-box;
            }}
            /* Spins-left box sits right next to the small decorative wheel
               icon in the background art - centering the number puts it
               too close to (or overlapping) the icon, so right-align it
               instead to keep clear space between them. */
            #hud-spins-left {{
                justify-content: center;
                font-size: var(--hud-spins-font-size, 24px);
                color: #ffffff;
                padding: 0;
            }}
            /* "Current Points" box has a baked-in label taking the top
               ~38% of its height, with the actual red fill area below it
               - measured directly from the source art's pixels. Position
               the dynamic number within just that red region, not the
               whole box (which was overlapping the label text). */
            #hud-current-points {{
                top: 85.558% !important;
                height: 7.782% !important;
                color: #ffffff;
                font-size: min(1.8vw, 11px);
                padding: 0;
            }}
            {hud_css}

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

            /* Sector labels - each wrapper is rotated to its sector's
               angle; being children of #wheel-graphic, they spin along
               with it automatically. */
            .sector-label {{
                position: absolute;
                inset: 0;
                transform-origin: 50% 50%;
                pointer-events: none;
            }}
            .sector-label-text {{
                position: absolute;
                left: 50%;
                transform: translate(-50%, -50%);
                writing-mode: vertical-lr;
                text-orientation: upright;
                text-align: center;
                font-family: 'Press Start 2P', monospace;
                font-size: var(--label-font-size, 14px);
                line-height: 1.2;
                letter-spacing: 0px;
                color: #1a1a1a;
                white-space: nowrap;
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
                {hud_divs}
                <div id="wheel-graphic">
                    {label_divs}
                </div>
                <div id="pointer-layer"></div>
                <div id="result-readout"></div>
            </div>
        </div>

        <script>
            const NUM_SECTORS = {self.NUM_SECTORS};
            const SECTOR_ANGLE = 360 / NUM_SECTORS;
            const SECTOR_LABELS = {__import__("json").dumps([self.SECTOR_LABELS[i] if i < len(self.SECTOR_LABELS) else "" for i in range(self.NUM_SECTORS)])};

            {"".join(self.nav_trigger_js(f"wheel_sector{i}") for i in range(self.NUM_SECTORS))}
            const sectorNavTriggers = [
                {", ".join(f"triggerNav_wheel_sector{i}" for i in range(self.NUM_SECTORS))}
            ];

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
                    readoutEl.textContent = "Landed on: " + SECTOR_LABELS[winningSector];
                    readoutEl.classList.add("visible");

                    // Let the player see the result for a moment, then
                    // navigate to whatever page that sector leads to.
                    setTimeout(() => {{
                        sectorNavTriggers[winningSector]();
                    }}, 1800);
                }}, 4100); // slightly longer than the 4s CSS transition
            }}

            wheelEl.addEventListener("click", spinWheel);

            // Reference wheel width (in px) that the requested 14px font
            // size was designed/verified against. Font scales up/down
            // proportionally to however big the wheel actually renders,
            // so text stays the same RELATIVE size on any screen instead
            // of staying fixed at 14px while the wheel shrinks around it.
            const REFERENCE_WHEEL_WIDTH_PX = 635;
            const BASE_FONT_PX = 14;

            // HUD readouts (like spins-left) sit on the STAGE, not inside
            // the rotating wheel, so their scale reference is the stage's
            // own width rather than the wheel's. Reference stage width
            // matches what the wheel's 635px reference corresponds to
            // (wheel is 53.333% of stage width).
            const REFERENCE_STAGE_WIDTH_PX = REFERENCE_WHEEL_WIDTH_PX / 0.53333;
            const BASE_HUD_SPINS_FONT_PX = 24;
            const stageEl = document.getElementById("stage");

            function updateHudFontScale() {{
                const scale = stageEl.offsetWidth / REFERENCE_STAGE_WIDTH_PX;
                const fontPx = BASE_HUD_SPINS_FONT_PX * scale;
                stageEl.style.setProperty("--hud-spins-font-size", fontPx + "px");
            }}

            function updateLabelFontScale() {{
                const scale = wheelEl.offsetWidth / REFERENCE_WHEEL_WIDTH_PX;
                const fontPx = BASE_FONT_PX * scale;
                wheelEl.style.setProperty("--label-font-size", fontPx + "px");
            }}

            // Labels are positioned at a fixed radius (LABEL_RADIUS_PCT)
            // by default, but longer labels can be tall enough as
            // vertical text that their outer edge would render past the
            // wheel's visible rim. Measures each label's real rendered
            // size and nudges ONLY the ones that would overflow inward
            // just enough to stay within the wheel - short labels stay
            // exactly at the requested radius. Always resets to the
            // default position first, so this is safe to call repeatedly
            // on every resize (e.g. if the wheel grows back to a size
            // where a previously-clamped label no longer needs clamping).
            function clampLabelsToWheel() {{
                const wheelHeight = wheelEl.offsetHeight;
                const minTopPct = 3; // small safety margin from the outer rim
                const desiredCenterPct = {top_offset_pct:.3f};
                document.querySelectorAll(".sector-label-text").forEach((el) => {{
                    el.style.top = desiredCenterPct + "%"; // reset to default first
                    const halfHeightPct = (el.offsetHeight / 2 / wheelHeight) * 100;
                    const outerEdgePct = desiredCenterPct - halfHeightPct;
                    if (outerEdgePct < minTopPct) {{
                        el.style.top = (minTopPct + halfHeightPct) + "%";
                    }}
                }});
            }}

            function updateLabelSizingAndPosition() {{
                updateLabelFontScale();
                updateHudFontScale();
                clampLabelsToWheel();
            }}
            if (document.fonts && document.fonts.ready) {{
                document.fonts.ready.then(updateLabelSizingAndPosition);
            }}

            {self.fit_to_window_js(FRAME_W, FRAME_H)}

            function resizeFrame() {{
                const stage = document.getElementById("stage");
                if (window.frameElement) {{
                    window.frameElement.style.height = (stage.offsetHeight + 10) + "px";
                }}
            }}
            function fitAndResize() {{
                fitToWindow();
                resizeFrame();
                updateLabelSizingAndPosition();
            }}
            window.addEventListener("resize", fitAndResize);
            window.addEventListener("load", fitAndResize);
            setTimeout(fitAndResize, 50);
            setTimeout(fitAndResize, 300);
            setTimeout(fitAndResize, 800); // extra late pass in case web font loading shifted sizes
        </script>
        """
        components.html(html, height=int(FRAME_H / FRAME_W * 700) + 20)

        st.caption("Click the wheel to spin it. Sector selection is random for now (placeholder until wheel_service is wired up).")