from scripts.base import BaseScript
import pydirectinput

class Fluxing(BaseScript):

    def __init__(self):
        super().__init__()
        self.name = "fluxing"
        self.keys = self.keys_data[self.name]
        self.keyActivate = self.keys["activate_key"]

    def custom(self):
        pass


def run():
    script_class = Fluxing()
    script_class.custom()


if __name__ == "__main__":
    run()
