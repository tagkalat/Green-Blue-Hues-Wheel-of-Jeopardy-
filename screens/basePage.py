import streamlit as st

from assets.AssetManager import AssetManager
# Adjust the import above to match your actual project structure, e.g.:
#   from assets.AssetManager import AssetManager


class BasePage:
    """
    Every page in the app inherits from this. It defines the common
    shape the router relies on, so app.py never needs to know anything
    page-specific — it just calls .render() on whichever page is active.

    Subclasses must:
      - call super().__init__("their_asset_subfolder_name")
      - implement their own render() method

    self.controller gives every page access to the shared GameController
    instance (wired up once in app.py and stored in st.session_state so
    it survives Streamlit's rerun-the-whole-script-on-every-click behavior).
    """

    # Fallback CSS cap - used as the outer max-width in each page's CSS.
    # The REAL responsive fitting happens via FIT_TO_WINDOW_JS below, since
    # CSS vh/vw units don't work as expected inside components.html's
    # iframe (they measure the iframe's own box, not the actual browser
    # window - and we're the ones setting the iframe's height, so a
    # CSS-only vh cap ends up not constraining anything meaningfully).
    STAGE_MAX_WIDTH_CSS = "1280px"

    @staticmethod
    def fit_to_window_js(frame_w: int, frame_h: int) -> str:
        """
        Returns a JS snippet that shrinks #stage-wrap's max-width so the
        stage's calculated height never exceeds the ACTUAL browser
        window's visible height (measured via window.parent.innerHeight,
        which works because components.html's iframe is same-origin).

        Call this once from each page's <script> block:
            {self.fit_to_window_js(FRAME_W, FRAME_H)}
        and it defines a fitToWindow() function - call fitToWindow() at
        the same points you already call resizeFrame().
        """
        aspect = frame_w / frame_h
        return f"""
        function fitToWindow() {{
            const stageWrap = document.getElementById("stage-wrap");
            if (!stageWrap || !window.parent) return;

            // 130px buffer accounts for Streamlit's own header bar and
            // page padding above/below the component. Adjust if your
            // layout has more/less surrounding chrome.
            const availableHeight = window.parent.innerHeight - 130;
            const availableWidth = window.parent.innerWidth * 0.95;

            const maxWidthFromHeight = availableHeight * {aspect};
            const finalMax = Math.min(1280, availableWidth, maxWidthFromHeight);

            stageWrap.style.maxWidth = finalMax + "px";
        }}
        // Recalculate whenever the actual browser window resizes, not
        // just the iframe (they're different windows).
        window.parent.addEventListener("resize", fitToWindow);
        """

    def render_nav_trigger(self, nav_id: str, target_page: str, extra_session_keys: dict = None):
        """
        Renders an invisible REAL Streamlit button that performs navigation
        when clicked. Pair this with nav_trigger_js(nav_id) in your JS -
        instead of setting window.parent.location.href (which is silently
        blocked now that components.html's iframe sandbox doesn't grant
        allow-top-navigation), JS finds this real button in the parent
        page via same-origin DOM access and calls .click() on it. A real
        click on a real Streamlit button isn't sandboxed at all, so this
        sidesteps the restriction entirely.

        extra_session_keys: optional dict of {session_state_key: None}
        placeholders this nav trigger should carry forward as-is (their
        current session_state values are preserved across the rerun
        automatically - session_state isn't cleared by st.rerun()).
        """
        label = f"NAVTRIGGER-{nav_id}"
        container_key = f"hidden_nav_{nav_id}"
        with st.container(key=container_key):
            if st.button(label, key=f"navbtn_{nav_id}"):
                st.query_params["page"] = target_page
                st.rerun()
        # Push the container off-screen. Off-screen elements are still
        # perfectly clickable via JS .click() - only real mouse events
        # need visibility, synthetic .click() calls don't.
        st.markdown(
            f"""
            <style>
                div[class*="st-key-{container_key}"] {{
                    position: absolute;
                    left: -9999px;
                    top: -9999px;
                }}
            </style>
            """,
            unsafe_allow_html=True,
        )

    @staticmethod
    def nav_trigger_js(nav_id: str) -> str:
        """
        Returns a JS snippet defining triggerNav_<nav_id>(), which finds
        the matching render_nav_trigger() button in the parent page (by
        its unique label text) and clicks it for real.
        """
        label = f"NAVTRIGGER-{nav_id}"
        return f"""
        function triggerNav_{nav_id}() {{
            const buttons = window.parent.document.querySelectorAll("button");
            for (const b of buttons) {{
                if (b.innerText.trim() === "{label}") {{
                    b.click();
                    return;
                }}
            }}
            console.warn("triggerNav_{nav_id}: hidden button not found");
        }}
        """

    def render_nav_trigger_with_value(self, nav_id: str, target_page: str,
                                        value_session_key: str, default_value=1):
        """
        Like render_nav_trigger, but also carries a typed number through to
        the next page via st.session_state, for pages like PlayerNumberPage
        where a value needs to travel along with the navigation.

        Pairs with nav_trigger_with_value_js(nav_id, value_session_key) in
        your JS - it sets the hidden number_input's value (using the
        React-safe native setter trick) THEN clicks the hidden button, all
        synchronously, so the value is already updated before Streamlit
        processes the click.
        """
        label = f"NAVTRIGGER-{nav_id}"
        container_key = f"hidden_nav_{nav_id}"
        with st.container(key=container_key):
            value = st.number_input("", key=f"hiddenval_{nav_id}", value=default_value, label_visibility="collapsed")
            if st.button(label, key=f"navbtn_{nav_id}"):
                st.session_state[value_session_key] = value
                st.query_params["page"] = target_page
                st.rerun()
        st.markdown(
            f"""
            <style>
                div[class*="st-key-{container_key}"] {{
                    position: absolute;
                    left: -9999px;
                    top: -9999px;
                }}
            </style>
            """,
            unsafe_allow_html=True,
        )

    @staticmethod
    def nav_trigger_with_value_js(nav_id: str) -> str:
        """
        Returns JS defining setAndTriggerNav_<nav_id>(value) - sets the
        hidden number_input's value using the native-setter trick (needed
        because React tracks input state internally and a plain
        `.value = x` assignment gets silently ignored/overwritten), then
        clicks the hidden button, both synchronously.
        """
        label = f"NAVTRIGGER-{nav_id}"
        return f"""
        function setAndTriggerNav_{nav_id}(value) {{
            const doc = window.parent.document;

            // Find the hidden number_input by its container's key-based class
            const container = doc.querySelector('div[class*="st-key-hidden_nav_{nav_id}"]');
            if (!container) {{ console.warn("hidden container not found for {nav_id}"); return; }}
            const input = container.querySelector('input[type="number"]');
            if (!input) {{ console.warn("hidden input not found for {nav_id}"); return; }}

            // React tracks <input> state via its own internal value
            // tracker, so a plain `input.value = x` gets silently
            // overwritten. Using the native setter + dispatching a real
            // "input" event bypasses that and properly updates React's
            // state (and therefore Streamlit's session_state).
            const nativeSetter = Object.getOwnPropertyDescriptor(
                window.parent.HTMLInputElement.prototype, "value"
            ).set;
            nativeSetter.call(input, value);
            input.dispatchEvent(new Event("input", {{ bubbles: true }}));

            // Now click the hidden submit button, same as a normal nav trigger.
            const buttons = doc.querySelectorAll("button");
            for (const b of buttons) {{
                if (b.innerText.trim() === "{label}") {{
                    b.click();
                    return;
                }}
            }}
            console.warn("triggerNav button not found for {nav_id}");
        }}
        """

    def __init__(self, assets_subfolder: str):
        self.assets = AssetManager(assets_subfolder)
        # Will be None until app.py has run its wiring step and stored
        # a controller in session_state — see app.py for that setup.
        self.controller = st.session_state.get("controller")

    def render(self):
        """
        Subclasses MUST override this — it's what actually draws the
        page's UI (HTML components, Streamlit widgets, etc.).
        """
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement its own render() method"
        )