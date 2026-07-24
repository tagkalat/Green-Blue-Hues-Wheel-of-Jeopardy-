from copy import deepcopy
from datetime import datetime
import time


USE_COLOR = True
MESSAGE_DELAY_SECONDS = 0.65


class ConsoleColor:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    GRAY = "\033[90m"
    CYAN = "\033[96m"
    MAGENTA = "\033[95m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    WHITE = "\033[97m"


class MessageBus:
    """Logs subsystem-to-subsystem messages for the skeletal increment."""

    def __init__(self):
        self.messages = []
        self.sequence = 1
        self.header_printed = False

    def send(self, sender, receiver, message_type, payload=None):
        if payload is None:
            payload = {}

        message = {
            "sequence": self.sequence,
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "sender": sender,
            "receiver": receiver,
            "message_type": message_type,
            "payload": deepcopy(payload),
        }

        self.messages.append(message)
        self.sequence += 1

        # Print immediately so the narrated demo shows communication live.
        if not self.header_printed:
            self._print_log_header("LIVE SUBSYSTEM MESSAGES")
            self.header_printed = True

        print(self.format_message(message), flush=True)
        time.sleep(MESSAGE_DELAY_SECONDS)

        return message

    def format_message(self, message):
        number = self._color(f"{message['sequence']:02d}", ConsoleColor.GRAY)
        sender = self._color(
            f"{message['sender']:<24}",
            self._get_subsystem_color(message["sender"])
        )
        receiver = self._color(
            f"{message['receiver']:<24}",
            self._get_subsystem_color(message["receiver"])
        )
        message_type = self._color(
            f"{message['message_type']:<24}",
            ConsoleColor.GREEN
        )

        payload_summary = self._summarize_payload(message["payload"])

        if payload_summary:
            payload_text = self._color(payload_summary, ConsoleColor.YELLOW)
            return f"{number} | {sender} → {receiver} | {message_type} | {payload_text}"

        return f"{number} | {sender} → {receiver} | {message_type}"

    def show_log(self):
        print()
        self._print_log_header("FULL SUBSYSTEM MESSAGE LOG")

        if not self.messages:
            print("No messages have been sent yet.")
            return

        for message in self.messages:
            print(self.format_message(message))

    def _print_log_header(self, title):
        print("\n" + "=" * 105)
        print(self._color(title, ConsoleColor.BOLD))
        print("=" * 105)
        print(
            f"{'No':<2} | "
            f"{'Sender':<24} → "
            f"{'Receiver':<24} | "
            f"{'Message Type':<24} | "
            f"Payload Summary"
        )
        print("-" * 105)

    def _summarize_payload(self, payload):
        if not payload:
            return ""

        summary_parts = []

        for key, value in payload.items():
            if isinstance(value, list):
                items = ", ".join(str(item) for item in value)
                summary_parts.append(f"{key}: [{items}]")

            elif isinstance(value, dict):
                dict_items = ", ".join(
                    f"{dict_key}: {dict_value}"
                    for dict_key, dict_value in value.items()
                )
                summary_parts.append(f"{key}: {{{dict_items}}}")

            else:
                summary_parts.append(f"{key}: {value}")

        return "; ".join(summary_parts)

    def _get_subsystem_color(self, subsystem_name):
        color_map = {
            "Console Driver": ConsoleColor.CYAN,
            "Game Controller": ConsoleColor.MAGENTA,
            "Wheel Service": ConsoleColor.BLUE,
            "Board Service": ConsoleColor.GREEN,
            "Question Repository": ConsoleColor.YELLOW,
            "Player Score Service": ConsoleColor.RED,
            "Announcer Service": ConsoleColor.WHITE,
        }

        return color_map.get(subsystem_name, ConsoleColor.WHITE)

    def _color(self, text, color):
        if not USE_COLOR:
            return text

        return f"{color}{text}{ConsoleColor.RESET}"