from tkinter import Tk, Label, Entry, Button
import tools.jsonOper
#
#

def main():

    def setting():
        count = 0
        for i in grid_list:
            if count == 0:
                if i.get() != "":
                    settings["activate_key"] = i.get()

            if count != 0:
                if i.get() != "":
                    settings[f"key{count}"]["value"] = i.get()

            count += 1


        data["fluxing"] = settings
        tools.jsonOper.saveKeys(data)

    def reset():
        tools.jsonOper.reset()
        exit(0)

    def do():
        setting()
        exit(0)

    data = tools.jsonOper.loadKeysGui()
    settings = data["fluxing"]

    window1 = Tk()
    window1.title("Mortal Online 2 Scripts Spam Settings")
    window1.geometry('1200x600')

    count_row = 0
    for i in settings:
        if i != "base":
            if count_row == 0:

                lbl_name = Label(window1, text="Активация")
                lbl_name.grid(column=0, row=count_row)

                lbl_key = Label(window1, text=f"    {settings[i]}")
                lbl_key.grid(column=1, row=count_row)
                count_row += 1


            else:

                lbl_name = Label(window1, text=f'{settings[i]["name"]}  ')
                lbl_name.grid(column=0, row=count_row)

                lbl_key = Label(window1, text=f'    {settings[i]["value"]}')
                lbl_key.grid(column=1, row=count_row)
                count_row += 1

    text_list = [
                '',
                'Каст на себя',
                'Движение назад',
                'Движение вперед',
                'Движение влево',
                'Движение вправо',
                'Expel Spirit (Изгнание)',
                'Призыв спирита',
                'барьер',
                'кау реген',
                'Время до возвращения на спот при неудачном вызове',
                'Уменьшаем, если отходит вперед, и наоборот',
                'Максимальный отход назад в случае если не успел бот увидеть медузу',
                'За сколько секунд бот перестанет работать если ничего не происходит',
                'чем меньше, тем дальше будет отходить от медузы, и наоборот',
                'путь на файл с изображением Spirit в центре экрана',
                'влияет на опережение прицела',
                'Ваш ID в телеге',
                'Ваш ID2 в телеге',
                'Ваш токен бота',
    ]

    grid_list = [
                 Entry(window1, width=10),
                 Entry(window1, width=10),
                 Entry(window1, width=10),
                 Entry(window1, width=10),
                 Entry(window1, width=10),
                 Entry(window1, width=10),
                 Entry(window1, width=10),
                 Entry(window1, width=10),
                 Entry(window1, width=10),
                 Entry(window1, width=10),
                 Entry(window1, width=10),
                 Entry(window1, width=10),
                 Entry(window1, width=10),
                 Entry(window1, width=10),
                 Entry(window1, width=10),
                 Entry(window1, width=10),
                 Entry(window1, width=10),
                 Entry(window1, width=10),
                 Entry(window1, width=10),
                 Entry(window1, width=10)
                 ]

    row = 0
    for i in grid_list:
        i.grid(column=2, row=row)
        row += 1

    row = 0
    for i in text_list:
        lbl = Label(window1, text=f"{i}")
        lbl.grid(column=3, row=row)
        row += 1

    lbl_pass = Label(window1, text="               ")
    lbl_pass.grid(column=5)
    btn = Button(window1, text="Принять настройки", command=do)
    btn.grid(column=6, row=0)
    btn = Button(window1, text="Сбросить", command=reset)
    btn.grid(column=6, row=2)



    window1.mainloop()


def name():
    return "spam"


if __name__ == "__main__":
    main()



