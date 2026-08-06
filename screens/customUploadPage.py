import streamlit as st
import streamlit.components.v1 as components

from screens.basePage import BasePage


class CustomUploadPage(BasePage):
    """
    Lets the host upload a custom question set. Uses Streamlit's own
    native st.file_uploader (which already supports drag-and-drop out of
    the box) - CSS-overlaid to sit visually inside the "Drag and drop"
    box art rather than as a separate plain widget elsewhere on the page.

    WHY NATIVE, NOT A CUSTOM IFRAME BRIDGE: an earlier attempt tried
    reading dropped files inside the iframe and bridging the data out via
    a hidden Streamlit widget (the same trick used for button clicks
    elsewhere). That trick reliably works for CLICKS (no data), but
    testing showed it does NOT reliably deliver actual VALUES to
    Streamlit's backend - the DOM shows the right value, but Python
    receives an empty string. Streamlit's native uploader sidesteps this
    entirely since it's not going through any custom bridge at all.

    HOW THE OVERLAY WORKS: the file_uploader and the iframe (scene art)
    are both rendered inside the SAME keyed container, which is sized to
    the same 480x270 aspect ratio as the stage. The iframe fills that
    container completely (position:absolute inset:0). The uploader's
    dropzone element is ALSO absolutely positioned within that same
    container, at the exact same percentage coordinates as the box art
    inside the iframe - so both share one coordinate space and land in
    the same visual spot. The dropzone's default icon/text are hidden
    (CSS) since the box art already has "Drag and drop..." baked in.
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
    START_BOX = {
        "left_pct": 86.667, "top_pct": 82.963,
        "width_pct": 13.333, "height_pct": 17.778,
    }

    WRAPPER_KEY = "custom_upload_scene_wrapper"

    def __init__(self):
        super().__init__("customUploadpage")

    def render(self):
        a = self.assets

        self.render_nav_trigger("customupload_start", "playerNumberPage")
        self.render_nav_trigger("customupload_back", "title")

        bg = a.get("CustomUploadBackground_0")
        back_unpressed = a.get("CustomUploadBackbutton_0")
        back_pressed = a.get("CustomUploadBackbutton_1")
        start_unpressed = a.get("CustomUploadStartButton_0")
        start_pressed = a.get("CustomUploadStartButton_1")

        FRAME_W, FRAME_H = self.FRAME_W, self.FRAME_H
        rb = self.RULEBOX_BOX
        bb = self.BACK_BOX
        sb = self.START_BOX

        # Everything - the native uploader AND the iframe scene - lives
        # inside this one keyed container, so both share the same
        # coordinate space for absolute positioning to line up.
        with st.container(key=self.WRAPPER_KEY):
            uploaded_file = st.file_uploader(
                "Upload your custom question set (Excel template)",
                type=["xlsx"],
                label_visibility="collapsed",
            )

            file_was_uploaded = uploaded_file is not None
            if file_was_uploaded:
                st.session_state["custom_questions_file"] = uploaded_file
                # TODO: hand this off to your backend (e.g.
                # self.controller.load_custom_questions(uploaded_file))
                # once question_repository's loading interface is ready.

            # Swap to the clean/empty box art once a file's chosen - the
            # default box has "Drag and drop..." baked directly into the
            # image (not separate text we can toggle), so it visually
            # clashes with Streamlit's file chip once one's shown on top.
            rulebox = a.get("CustomUploadRulebox_1" if file_was_uploaded else "CustomUploadRulebox_0")

            if file_was_uploaded:
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
                        pointer-events: none;
                    "></div>
                """
            else:
                donemark_html = ""

            html = f"""
            <style>
                html, body {{ margin: 0; padding: 0; }}
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
                #start-btn {{
                    position: absolute;
                    left: {sb["left_pct"]:.3f}%;
                    top: {sb["top_pct"]:.3f}%;
                    width: {sb["width_pct"]:.3f}%;
                    height: {sb["height_pct"]:.3f}%;
                    cursor: pointer;
                    background-size: 100% 100%;
                    image-rendering: pixelated;
                    background-image: url('data:image/png;base64,{start_unpressed}');
                }}
            </style>

            <div id="stage">
                <div id="bg-layer"></div>
                <div id="rulebox-layer"></div>
                {donemark_html}
                <div id="back-btn"></div>
                <div id="start-btn"></div>
            </div>

            <script>
                {self.nav_trigger_js("customupload_back")}
                {self.nav_trigger_js("customupload_start")}

                const backUnpressedImg = "data:image/png;base64,{back_unpressed}";
                const backPressedImg = "data:image/png;base64,{back_pressed}";
                const backBtn = document.getElementById("back-btn");
                let isBackPressed = false;

                backBtn.addEventListener("pointerdown", (e) => {{
                    isBackPressed = true;
                    backBtn.style.backgroundImage = "url('" + backPressedImg + "')";
                    backBtn.setPointerCapture(e.pointerId);
                }});
                backBtn.addEventListener("pointerup", () => {{
                    if (!isBackPressed) return;
                    isBackPressed = false;
                    backBtn.style.backgroundImage = "url('" + backUnpressedImg + "')";
                    triggerNav_customupload_back();
                }});
                backBtn.addEventListener("pointerleave", () => {{
                    if (!isBackPressed) return;
                    isBackPressed = false;
                    backBtn.style.backgroundImage = "url('" + backUnpressedImg + "')";
                }});
                backBtn.addEventListener("pointercancel", () => {{
                    isBackPressed = false;
                    backBtn.style.backgroundImage = "url('" + backUnpressedImg + "')";
                }});

                const startUnpressedImg = "data:image/png;base64,{start_unpressed}";
                const startPressedImg = "data:image/png;base64,{start_pressed}";
                const startBtn = document.getElementById("start-btn");
                let isStartPressed = false;

                startBtn.addEventListener("pointerdown", (e) => {{
                    isStartPressed = true;
                    startBtn.style.backgroundImage = "url('" + startPressedImg + "')";
                    startBtn.setPointerCapture(e.pointerId);
                }});
                startBtn.addEventListener("pointerup", () => {{
                    if (!isStartPressed) return;
                    isStartPressed = false;
                    startBtn.style.backgroundImage = "url('" + startUnpressedImg + "')";
                    triggerNav_customupload_start();
                }});
                startBtn.addEventListener("pointerleave", () => {{
                    if (!isStartPressed) return;
                    isStartPressed = false;
                    startBtn.style.backgroundImage = "url('" + startUnpressedImg + "')";
                }});
                startBtn.addEventListener("pointercancel", () => {{
                    isStartPressed = false;
                    startBtn.style.backgroundImage = "url('" + startUnpressedImg + "')";
                }});

                window.addEventListener("pageshow", () => {{
                    backBtn.style.backgroundImage = "url('" + backUnpressedImg + "')";
                    startBtn.style.backgroundImage = "url('" + startUnpressedImg + "')";
                }});

                // Position the native file_uploader's dropzone via JS-applied
                // inline styles (from inside the iframe, targeting the parent
                // page - same window.parent.document pattern used by the nav
                // triggers). A plain stylesheet rule wasn't reliably beating
                // Streamlit's own CSS for height/top even with !important,
                // but a JS-applied inline !important style always wins.
                (function() {{
                    const wrapper = window.parent.document.querySelector('div[class*="st-key-{self.WRAPPER_KEY}"]');
                    if (!wrapper) {{ console.warn("upload wrapper not found for positioning"); return; }}

                    function positionDropzone() {{
                        // Re-query fresh every time, rather than reusing a
                        // captured reference - Streamlit replaces the
                        // dropzone's DOM node when transitioning between
                        // "empty" and "file chosen" states, which would
                        // otherwise leave us styling a stale, detached
                        // element while the real (new) one stays unstyled.
                        const dropzone = wrapper.querySelector('[data-testid="stFileUploaderDropzone"]');
                        const elementContainer = wrapper.querySelector('[data-testid="stElementContainer"]');
                        if (!dropzone) return;

                        // stElementContainer (a Streamlit-internal wrapper)
                        // has position:relative by default, making IT the
                        // CSS containing block for our absolutely-positioned
                        // dropzone instead of our own outer wrapper - and
                        // since it has height:0, that broke percentage
                        // sizing entirely. Neutralizing its position lets
                        // the containing-block search continue up to our
                        // actual wrapper (which has a real, non-zero height).
                        if (elementContainer) {{
                            elementContainer.style.setProperty("position", "static", "important");
                        }}
                        dropzone.style.setProperty("position", "absolute", "important");
                        dropzone.style.setProperty("left", "{rb["left_pct"]:.3f}%", "important");
                        dropzone.style.setProperty("top", "{rb["top_pct"]:.3f}%", "important");
                        dropzone.style.setProperty("width", "{rb["width_pct"]:.3f}%", "important");
                        dropzone.style.setProperty("height", "{rb["height_pct"]:.3f}%", "important");
                        dropzone.style.setProperty("min-height", "0", "important");
                        dropzone.style.setProperty("max-height", "none", "important");
                        dropzone.style.setProperty("overflow", "auto", "important");
                        dropzone.style.setProperty("padding-top", "8%", "important");
                        dropzone.style.setProperty("box-sizing", "border-box", "important");
                    }}
                    positionDropzone();
                    window.parent.addEventListener("resize", positionDropzone);
                    setTimeout(positionDropzone, 300);
                    setTimeout(positionDropzone, 1000);
                    new window.parent.MutationObserver(positionDropzone).observe(wrapper, {{ childList: true, subtree: true }});
                }})();

                function resizeFrame() {{
                    const stage = document.getElementById("stage");
                    if (window.frameElement) {{
                        window.frameElement.style.height = (stage.offsetHeight + 10) + "px";
                    }}
                }}
                window.addEventListener("resize", resizeFrame);
                window.addEventListener("load", resizeFrame);
                setTimeout(resizeFrame, 50);
                setTimeout(resizeFrame, 300);
            </script>
            """
            components.html(html, height=int(FRAME_H / FRAME_W * 700) + 20)

        # CSS: size the wrapper to the stage's aspect ratio, make the
        # iframe fill it completely, and absolutely position the native
        # uploader's dropzone at the same coordinates as the box art -
        # hiding its default icon/text since the art already has its own.
        st.markdown(
            f"""
            <style>
                div[class*="st-key-{self.WRAPPER_KEY}"] {{
                    position: relative;
                    width: 100%;
                    max-width: {self.STAGE_MAX_WIDTH_CSS};
                    aspect-ratio: {FRAME_W} / {FRAME_H};
                    margin: 0 auto;
                }}
                div[class*="st-key-{self.WRAPPER_KEY}"] iframe {{
                    position: absolute;
                    inset: 0;
                    width: 100%;
                    height: 100%;
                    border: none;
                }}
                div[class*="st-key-{self.WRAPPER_KEY}"] [data-testid="stFileUploader"] {{
                    height: 0;
                    overflow: visible;
                }}
                div[class*="st-key-{self.WRAPPER_KEY}"] [data-testid="stFileUploaderDropzone"] {{
                    background: transparent !important;
                    border: none !important;
                    z-index: 5;
                }}
                div[class*="st-key-{self.WRAPPER_KEY}"] [data-testid="stFileUploaderDropzoneInstructions"] {{
                    display: none !important;
                }}
                div[class*="st-key-{self.WRAPPER_KEY}"] [data-testid="stBaseButton-secondary"] {{
                    display: none !important;
                }}
                div[class*="st-key-{self.WRAPPER_KEY}"] [data-testid="stWidgetLabel"] {{
                    display: none !important;
                }}
            </style>
            """,
            unsafe_allow_html=True,
        )
