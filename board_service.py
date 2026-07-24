class BoardService:
    """Represents the Jeopardy-style board state."""

    def __init__(self, message_bus, question_repository):
        self.message_bus = message_bus
        self.question_repository = question_repository
        self.active_categories = []
        self.available_values = {}

    def initialize_board(self, categories):
        self.active_categories = categories
        self.available_values = {
            category: self.question_repository.get_values_for_category(category)
            for category in categories
        }

        self.message_bus.send(
            "Board Service",
            "Console Driver",
            "BoardReady",
            {
                "categories": self.active_categories,
                "available_values": self.available_values,
            },
        )

    def display_board(self):
        print("\nQUESTION BOARD STATE")
        print("-" * 70)

        if not self.active_categories:
            print("Board has not been initialized yet.")
            return

        for category in self.active_categories:
            values = self.available_values.get(category, [])
            values_text = ", ".join(str(value) for value in values) if values else "All used"
            print(f"{category:12} : {values_text}")

    def request_question(self, category, value):
        self.message_bus.send(
            "Board Service",
            "Question Repository",
            "GetQuestionRequest",
            {"category": category, "value": value},
        )

        question = self.question_repository.get_question(category, value)

        if question is not None:
            self.mark_question_used(category, value)
            self.message_bus.send(
                "Board Service",
                "Game Controller",
                "QuestionReady",
                {"category": category, "value": value},
            )

        return question

    def mark_question_used(self, category, value):
        if category in self.available_values and value in self.available_values[category]:
            self.available_values[category].remove(value)

            self.message_bus.send(
                "Board Service",
                "Game Controller",
                "BoardStateUpdated",
                {"category": category, "removed_value": value},
            )

    def first_available_value(self, category):
        values = self.available_values.get(category, [])
        return values[0] if values else None
