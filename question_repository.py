import json
from pathlib import Path


class QuestionRepository:
    """Stub question repository. Later this can become a database layer."""

    def __init__(self, message_bus, data_file="data/questions.json"):
        self.message_bus = message_bus
        self.data_file = Path(data_file)
        self.categories = self._load_questions()

    def _load_questions(self):
        with open(self.data_file, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data["categories"]

    def load_categories(self, count=6):
        selected_categories = [category["name"] for category in self.categories[:count]]

        self.message_bus.send(
            "Question Repository",
            "Game Controller",
            "CategoriesLoaded",
            {"categories": selected_categories},
        )

        return selected_categories

    def get_values_for_category(self, category_name):
        category = self._find_category(category_name)
        if category is None:
            return []
        return [question["value"] for question in category["questions"]]

    def get_question(self, category_name, value):
        category = self._find_category(category_name)

        if category is None:
            self.message_bus.send(
                "Question Repository",
                "Board Service",
                "CategoryNotFound",
                {"category": category_name},
            )
            return None

        for question in category["questions"]:
            if question["value"] == value:
                self.message_bus.send(
                    "Question Repository",
                    "Board Service",
                    "QuestionReturned",
                    {"category": category_name, "value": value},
                )
                return question

        self.message_bus.send(
            "Question Repository",
            "Board Service",
            "QuestionNotFound",
            {"category": category_name, "value": value},
        )
        return None

    def _find_category(self, category_name):
        for category in self.categories:
            if category["name"].lower() == category_name.lower():
                return category
        return None
