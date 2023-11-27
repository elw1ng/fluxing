
from datetime import datetime
from colorama import init, Fore
init(autoreset=True)


def debug_log(debug_mode=True,
              app_name="",
              text="",
              variable="",
              scenario_start="",
              scenario_end="",
              condition="",
              color="green"):
    """Печатает логи различных состояний в нужном цвете. Принимает аргументы:

              debug_mode - включение/выключение функции;
              app_name - имя приложения;
              text - комментарий;
              variable - значение переменной, лучше записывать как: f{x=};
              scenario_start - запускающийся сценарий;
              scenario_end - завершающийся сценарий;
              condition - условие в завершающемся сценарии;
              color - цвет текста (white, blue, red, green, yellow).
              """

    if debug_mode:
        text_color = ""
        match color:
            case "white":
                text_color = Fore.WHITE
            case "blue":
                text_color = Fore.BLUE
            case "red":
                text_color = Fore.RED
            case "green":
                text_color = Fore.GREEN
            case "yellow":
                text_color = Fore.YELLOW
            case _:
                text_color = Fore.RESET

        time = datetime.now()
        time_now = time.strftime("%H:%M:%S")

        pref = "DEBUGGER: "
        app_name = ("Приложение: " + str(app_name) + ". ") if app_name != "" else ""
        scenario_start = ("Начало сценария: " + str(scenario_start) + ". ") if scenario_start != "" else ""
        scenario_end = ("Конец сценария: " + str(scenario_end) + ". ") if scenario_end != "" else ""
        condition = ("Условие: " + str(condition) + ". ") if condition != "" else ""
        text = ("Комментарий: " + str(text) + ". ") if text != "" else ""
        variable = ("Значение переменной: " + str(variable) + ". ") if variable != "" else ""

        print(text_color + f"{app_name}{pref}{scenario_end}{scenario_start}{condition}{variable}{text} || {time_now}")


if __name__ == "__main__":
    x = 10
    debug_log(True, variable=f"{x=}")
