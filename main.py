from game_controller import GameController
from demo_scenario import DemoScenario


def main():
    print("=" * 70)
    print("WHEEL OF JEOPARDY - SKELETAL ARCHITECTURE DEMO")
    print("=" * 70)
    print("This is a console-based driver for the skeletal increment.")
    print("It simulates a short gameplay session and prints subsystem messages.")
    print("The final version can replace this console driver with a web UI.\n")

    controller = GameController()
    scenario = DemoScenario(controller)
    scenario.run()


if __name__ == "__main__":
    main()
