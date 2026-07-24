

class DemoScenario:
    """Runs a scripted mock gameplay session for the skeletal increment."""

    def __init__(self, controller):
        self.controller = controller

    def run(self):
        self._title("STARTUP: INITIALIZE GAME ARCHITECTURE")
        self.controller.start_game()
        self.controller.display_board()
        self.controller.display_scoreboard()

        self._title("TURN 1: PLAYER 1 SPINS SCIENCE AND ANSWERS CORRECTLY")
        self.controller.spin_wheel(forced_result="Science")
        self.controller.request_question(category="Science", value=100)
        self.controller.display_current_question()
        print("\nSCRIPTED ANSWER: Mars")
        self.controller.submit_answer("Mars")
        self.controller.display_scoreboard()

        self._title("TURN 2: PLAYER 1 SPINS FREE SPIN")
        self.controller.spin_wheel(forced_result="Free Spin")
        self.controller.display_scoreboard()

        self._title("TURN 3: PLAYER 1 SPINS HISTORY AND ANSWERS INCORRECTLY")
        self.controller.spin_wheel(forced_result="History")
        self.controller.request_question(category="History", value=100)
        self.controller.display_current_question()
        print("\nSCRIPTED ANSWER: Abraham Lincoln")
        self.controller.submit_answer("Abraham Lincoln")
        self.controller.display_scoreboard()

        self._title("TURN 4: PLAYER 1 SPINS BANKRUPT")
        self.controller.spin_wheel(forced_result="Bankrupt")
        self.controller.display_scoreboard()

        self._title("TURN 5: PLAYER 2 SPINS MOVIES AND ANSWERS CORRECTLY")
        self.controller.spin_wheel(forced_result="Movies")
        self.controller.request_question(category="Movies", value=100)
        self.controller.display_current_question()
        print("\nSCRIPTED ANSWER: The Lion King")
        self.controller.submit_answer("The Lion King")
        self.controller.display_scoreboard()

        self._title("FINAL ARCHITECTURE VALIDATION SUMMARY")
        print("Subsystems demonstrated:")
        print("- Console Driver")
        print("- Game Controller")
        print("- Wheel Service")
        print("- Board Service")
        print("- Question Repository")
        print("- Player Score Service")
        print("- Announcer Service")
        print("- Message Bus")
        print("\nResult: Skeletal subsystem communication validated.")
        print("Future work: Replace the Console Driver with the final web UI.")

        self.controller.show_message_log()

    def _title(self, text):
        print("\n" + "=" * 70)
        print(text)
        print("=" * 70)
