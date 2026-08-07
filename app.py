import streamlit as st

from screens.titlePage import TitlePage
from screens.gameRulesPage import GameRulesPage
from screens.customUploadPage import CustomUploadPage
from screens.playerNumberPage import PlayerNumberPage
from screens.wheelPage import WheelPage
from screens.freeSpinPage import FreeSpinPage
from screens.lostTurnPage import LostTurnPage
from screens.bankruptPage import BankruptPage
from screens.categoryPage import CategoryPage
from screens.questionPage import QuestionPage
from screens.answerPage import AnswerPage
from screens.winnerPage import WinnerPage
from screens.playerChoicePage import PlayersChoicePage
from screens.opponentChoicePage import OpponentChoicePage

st.set_page_config(page_title="Wheel of Jeopardy", layout="wide")


def create_game_controller():
    """
    Builds and wires up a fresh GameController with all its backend
    dependencies. This is app.py's own setup step (main.py is kept
    separate, for backend testing/demos).

    NOTE: placeholder wiring below — swap in your real imports/constructor
    args once you share game_controller.py's actual interface.
    """
    from game_controller import GameController
    # from wheel_service import WheelService
    # from board_service import BoardService
    # from player_score_service import PlayerScoreService
    # from announcer_service import AnnouncerService
    # from question_repository import QuestionRepository
    # from message_bus import MessageBus

    return GameController(
        # wheel_service=WheelService(),
        # board_service=BoardService(),
        # player_score_service=PlayerScoreService(),
        # announcer_service=AnnouncerService(),
        # question_repository=QuestionRepository(),
        # message_bus=MessageBus(),
    )


# Only build the controller ONCE per session — Streamlit reruns this whole
# script on every click, so without this check you'd wipe game state
# (scores, current question, etc.) on every single interaction.
if "controller" not in st.session_state:
    st.session_state.controller = create_game_controller()

# Maps the "page" query param -> the page class that handles it.
# Add a new entry here every time you build a new page.
PAGES = {
    "title": TitlePage,
    "gameRules": GameRulesPage,
    "customUploadpage": CustomUploadPage,
    "playerNumberPage": PlayerNumberPage,
    "wheel": WheelPage,
    "freeSpinPage": FreeSpinPage,
    "lostTurnPage": LostTurnPage,
    "bankruptPage": BankruptPage,
    "categoryPage": CategoryPage,
    "questionPage": QuestionPage,
    "answerPage": AnswerPage,
    "winnerPage": WinnerPage,
    "playersChoicePage": PlayersChoicePage,
    "opponentChoicePage": OpponentChoicePage,
}

current_page_name = st.query_params.get("page", "title")

page_class = PAGES.get(current_page_name, TitlePage)  # fall back to title if unknown
page_class().render()