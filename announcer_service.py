class AnnouncerService:
    """Produces player-facing messages for the demo."""

    def __init__(self, message_bus):
        self.message_bus = message_bus
        self.announcements = []

    def announce(self, text):
        self.announcements.append(text)

        self.message_bus.send(
            "Announcer Service",
            "Console Driver",
            "AnnouncerMessage",
            {"message": text},
        )

        print(f"\nANNOUNCER: {text}")
