from tkinter import Tk, Label, Button
from ultralytics1.settings import attackerGUI, destroyerPickaxeGUI


#
#


def destroyer_pickaxe_GUI():
    destroyerPickaxeGUI.main()

def do():
    exit(0)

def attacker_GUI():
    attackerGUI.main()


def main():
    def reset():
        TARTANISD.tools.jsonOper.reset()
        exit(0)

    window = Tk()
    window.title("Mortal Online 2 Scripts HUB")
    window.geometry('250x400')

    count_row = 0

    lbl_name = Label(window, text=f'{attackerGUI.name()}')
    lbl_name.grid(column=0, row=0)

    lbl_key = Button(window, text=f'Настройка', command=attacker_GUI)
    lbl_key.grid(column=1, row=0)

    lbl_name = Label(window, text=f'{destroyerPickaxeGUI.name()}')
    lbl_name.grid(column=0, row=1)

    lbl_key = Button(window, text=f'Настройка', command=destroyer_pickaxe_GUI)
    lbl_key.grid(column=1, row=1)

    lbl_pass = Label(text="               ")
    lbl_pass.grid(column=5)
    btn = Button(window, text="Закрыть", command=do)
    btn.grid(column=1, row=6)
    window.mainloop()


if __name__ == "__main__":
    main()



