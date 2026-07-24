import random


class WheelService:
    """Wheel subsystem. Supports forced results so the demo is repeatable."""

    SPECIAL_SECTORS = [
        "Lose Turn",
        "Free Spin",
        "Bankrupt",
        "Player Choice",
        "Opponents Choice",
    ]

    def __init__(self, message_bus):
        self.message_bus = message_bus

    def spin(self, categories, forced_result=None):
        sectors = categories + self.SPECIAL_SECTORS
        result = forced_result if forced_result is not None else random.choice(sectors)

        self.message_bus.send(
            "Wheel Service",
            "Game Controller",
            "WheelResult",
            {"result": result},
        )

        return result
