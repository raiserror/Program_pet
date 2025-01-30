from tkinter import *
from func import *

class App:
    def __init__(self, master):
        self.master = master
        frame = Frame(master)  # container widget
        frame.pack()

        note_width = Label(frame, text="Width")
        note_width.grid(row=0, column=0)

        note_height = Label(frame, text="Height")
        note_height.grid(row=1, column=0)

        validate_digit_command = master.register(validate_digit_input)

        self.level_var = StringVar(value='16:9')
        self.metric_var = StringVar(value='px')
        self.w_field = IntVar()
        self.fahrenheit = IntVar()

        self.func_ratio = FuncRatio(self.w_field, self.fahrenheit, self.level_var, self.metric_var)# Создаем экземпляр класса FuncRatio

        self.w_field.trace_id = self.w_field.trace("w", self.func_ratio.C2F)
        entry_width = Entry(frame, validate="key",
                            validatecommand=(validate_digit_command, '%P'), textvariable=self.w_field)

        entry_width.grid(row=0, column=1)

        self.fahrenheit.trace_id = self.fahrenheit.trace("w", self.func_ratio.F2C)
        entry_height = Entry(frame, validate="key",
                            validatecommand=(validate_digit_command, '%P'), textvariable=self.fahrenheit)

        entry_height.grid(row=1, column=1)

        self.display_num = {'1': '1:1', '2': '4:3', '3': '5:4', '4': '16:9', '5': '16:10', '6': '21:9'}
        for i in sorted(self.display_num):
            Radiobutton(frame, text=self.display_num[i], variable=self.level_var,
                        value=self.display_num[i], command=self.func_ratio.F2C).grid(row=3, column=int(i) - 1)




# Root Setup and size
root = Tk()
root.title("Соотношение сторон: Калькулятор")
win_photo = PhotoImage(file='root_icon.png')
root.iconphoto(False, win_photo)
app = App(root)
root.mainloop()