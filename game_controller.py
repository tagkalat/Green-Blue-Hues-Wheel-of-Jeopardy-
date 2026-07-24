from message_bus import MessageBus
from question_repository import QuestionRepository
from wheel_service import WheelService
from board_service import BoardService
from player_score_service import PlayerScoreService
from announcer_service import AnnouncerService


class GameController:
    """Coordinates communication between all skeletal subsystems."""

    def __init__(self):
        self.message_bus = MessageBus()
        self.question_repository = QuestionRepository(self.message_bus)
        self.wheel_service = WheelService(self.message_bus)
        self.board_service = BoardService(self.message_bus, self.question_repository)
        self.player_score_service = PlayerScoreService(self.message_bus)
        self.announcer_service = AnnouncerService(self.message_bus)

        self.game_started = False
        self.current_question = None
        self.current_category = None
        self.current_value = None

    def start_game(self):
        self.message_bus.send(
            "Console Driver",
            "Game Controller",
            "StartGameRequest",
        )

        self.message_bus.send(
            "Game Controller",
            "Question Repository",
            "LoadCategoriesRequest",
        )
        categories = self.question_repository.load_categories(count=6)

        self.message_bus.send(
            "Game Controller",
            "Board Service",
            "InitializeBoardRequest",
            {"categories": categories},
        )
        self.board_service.initialize_board(categories)

        self.game_started = True
        self.announcer_service.announce(
            "Welcome to Wheel of Jeopardy. Skeletal architecture initialized."
        )

    def spin_wheel(self, forced_result=None):
        if not self.game_started:
            self.announcer_service.announce("Start the game before spinning the wheel.")
            return None

        player_name = self.player_score_service.current_player_name()

        self.message_bus.send(
            "Console Driver",
            "Game Controller",
            "SpinRequest",
            {"player": player_name},
        )

        self.message_bus.send(
            "Game Controller",
            "Wheel Service",
            "SpinWheelRequest",
            {"player": player_name, "forced_result": forced_result},
        )

        result = self.wheel_service.spin(
            self.board_service.active_categories,
            forced_result=forced_result,
        )

        if result in self.board_service.active_categories:
            self.announcer_service.announce(f"{player_name} spun {result}.")
            return result

        if result == "Free Spin":
            self.message_bus.send(
                "Game Controller",
                "Player Score Service",
                "AwardFreeSpinRequest",
                {"player": player_name},
            )
            self.player_score_service.award_free_spin()
            self.announcer_service.announce(
                f"{player_name} earned a free spin token and may spin again."
            )
            return result

        if result == "Lose Turn":
            self.announcer_service.announce(f"{player_name} spun Lose Turn.")
            self._handle_lost_turn(can_use_free_spin=True)
            return result

        if result == "Bankrupt":
            self.message_bus.send(
                "Game Controller",
                "Player Score Service",
                "BankruptPlayerRequest",
                {"player": player_name},
            )
            self.player_score_service.apply_bankrupt()
            self.announcer_service.announce(
                f"{player_name} spun Bankrupt. Score resets and the turn passes."
            )
            self.player_score_service.next_turn()
            return result

        if result == "Player Choice":
            selected_category = self.board_service.active_categories[0]
            self.announcer_service.announce(
                f"{player_name} spun Player Choice. For this skeletal demo, {selected_category} is selected."
            )
            return selected_category

        if result == "Opponents Choice":
            selected_category = self.board_service.active_categories[-1]
            self.announcer_service.announce(
                f"{player_name} spun Opponents Choice. For this skeletal demo, {selected_category} is selected."
            )
            return selected_category

        return result

    def request_question(self, category, value=None):
        if value is None:
            value = self.board_service.first_available_value(category)

        if value is None:
            self.announcer_service.announce(f"No questions remain in {category}. Spin again.")
            return None

        self.message_bus.send(
            "Game Controller",
            "Board Service",
            "QuestionRequest",
            {"category": category, "value": value},
        )

        question = self.board_service.request_question(category, value)

        if question is None:
            self.announcer_service.announce(
                f"No question could be loaded for {category} at {value} points."
            )
            return None

        self.current_question = question
        self.current_category = category
        self.current_value = value
        self.announcer_service.announce(f"Question ready: {category} for {value} points.")
        return question

    def display_current_question(self):
        if self.current_question is None:
            print("\nNo active question is available.")
            return

        print("\nQUESTION")
        print("-" * 70)
        print(f"Category: {self.current_category}")
        print(f"Value: {self.current_value}")
        print(self.current_question["question"])
        for index, choice in enumerate(self.current_question["choices"], start=1):
            print(f"  {index}. {choice}")

    def submit_answer(self, selected_answer):
        if self.current_question is None:
            self.announcer_service.announce("No active question is available to answer.")
            return None

        player_name = self.player_score_service.current_player_name()
        correct_answer = self.current_question["answer"]
        points = self.current_question["value"]

        self.message_bus.send(
            "Console Driver",
            "Game Controller",
            "SubmitAnswer",
            {"player": player_name, "selected_answer": selected_answer},
        )

        if selected_answer == correct_answer:
            self.message_bus.send(
                "Game Controller",
                "Player Score Service",
                "CorrectAnswerRequest",
                {"player": player_name, "points": points},
            )
            new_score = self.player_score_service.apply_correct_answer(points)
            self.announcer_service.announce(
                f"Correct. {player_name}'s score is now {new_score}."
            )
            result = True
        else:
            self.message_bus.send(
                "Game Controller",
                "Player Score Service",
                "IncorrectAnswerRequest",
                {"player": player_name, "points": points},
            )
            new_score = self.player_score_service.apply_incorrect_answer(points)
            self.announcer_service.announce(
                f"Incorrect. The correct answer was {correct_answer}. {player_name}'s score is now {new_score}."
            )
            self._handle_lost_turn(can_use_free_spin=True)
            result = False

        self.current_question = None
        self.current_category = None
        self.current_value = None
        return result

    def _handle_lost_turn(self, can_use_free_spin):
        player_name = self.player_score_service.current_player_name()

        if can_use_free_spin:
            self.message_bus.send(
                "Game Controller",
                "Player Score Service",
                "CheckFreeSpinToken",
                {"player": player_name},
            )
            redeemed = self.player_score_service.redeem_free_spin_if_available()

            if redeemed:
                self.announcer_service.announce(
                    f"{player_name} used a free spin token and keeps the turn."
                )
                return

        self.announcer_service.announce(f"{player_name}'s turn is over.")
        self.player_score_service.next_turn()

    def display_board(self):
        self.board_service.display_board()

    def display_scoreboard(self):
        self.player_score_service.display_scoreboard()

    def show_message_log(self):
        self.message_bus.show_log()
