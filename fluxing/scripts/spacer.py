import random
from scripts.base import BaseScript
import pyautogui


class Spacer(BaseScript):

    def __init__(self):
        super().__init__()
        self.name = "spacer"
        self.keyActivate = self.keys[self.name]

    def rest(self):
        self.press("0")
        self.wait(random.uniform(0.05, 0.2))

    def custom(self):

        self.func_repetition(self.rest, 200)



def run():
    script_class = Spacer()
    script_class.custom()


if __name__ == "__main__":
    run()
