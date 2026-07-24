class PlayerScoreService:
    """Tracks skeletal player scores, free-spin tokens, and turn changes."""

    def __init__(self, message_bus):
        self.message_bus = message_bus
        self.players = [
            {"name": "Player 1", "score": 0, "free_spins": 0},
            {"name": "Player 2", "score": 0, "free_spins": 0},
        ]
        self.current_player_index = 0

    def current_player(self):
        return self.players[self.current_player_index]

    def current_player_name(self):
        return self.current_player()["name"]

    def apply_correct_answer(self, points):
        player = self.current_player()
        player["score"] += points

        self.message_bus.send(
            "Player Score Service",
            "Game Controller",
            "ScoreUpdated",
            {"player": player["name"], "score": player["score"]},
        )

        return player["score"]

    def apply_incorrect_answer(self, points):
        player = self.current_player()
        player["score"] -= points

        self.message_bus.send(
            "Player Score Service",
            "Game Controller",
            "ScoreUpdated",
            {"player": player["name"], "score": player["score"]},
        )

        return player["score"]

    def award_free_spin(self):
        player = self.current_player()
        player["free_spins"] += 1

        self.message_bus.send(
            "Player Score Service",
            "Game Controller",
            "FreeSpinAwarded",
            {"player": player["name"], "free_spins": player["free_spins"]},
        )

    def redeem_free_spin_if_available(self):
        player = self.current_player()

        if player["free_spins"] <= 0:
            self.message_bus.send(
                "Player Score Service",
                "Game Controller",
                "NoFreeSpinAvailable",
                {"player": player["name"]},
            )
            return False

        player["free_spins"] -= 1

        self.message_bus.send(
            "Player Score Service",
            "Game Controller",
            "FreeSpinRedeemed",
            {"player": player["name"], "free_spins": player["free_spins"]},
        )

        return True

    def apply_bankrupt(self):
        player = self.current_player()
        player["score"] = 0

        self.message_bus.send(
            "Player Score Service",
            "Game Controller",
            "BankruptApplied",
            {"player": player["name"], "score": player["score"]},
        )

    def next_turn(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

        self.message_bus.send(
            "Player Score Service",
            "Game Controller",
            "TurnChanged",
            {"current_player": self.current_player_name()},
        )

    def display_scoreboard(self):
        print("\nSCOREBOARD")
        print("-" * 70)
        for player in self.players:
            print(
                f"{player['name']:8} | "
                f"Score: {player['score']:4} | "
                f"Free Spin Tokens: {player['free_spins']}"
            )
        print(f"Current player: {self.current_player_name()}")
