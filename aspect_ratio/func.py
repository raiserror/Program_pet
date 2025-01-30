from symtable import Class
import math as m

def validate_digit_input(new_value):
    if new_value == "":
        return True
    elif new_value.isdigit():
        return True
    else:
        return False

class FuncRatio:
    def __init__(self, w_field, fahrenheit, level_var, metric_var):
        self.w_field = w_field
        self.fahrenheit = fahrenheit
        self.level_var = level_var
        self.metric_var = metric_var

    def F2C(self, *args):
        try:
            IN = self.w_field.get()
            self.fahrenheit.trace_remove("write", self.fahrenheit.trace_id)
            match self.level_var.get():
                case '1:1': self.fahrenheit.set(IN * 1)
                case '4:3': self.fahrenheit.set(int((IN / 4) * 3))
                case '5:4': self.fahrenheit.set(int((IN / 5) * 4))
                case '16:9': self.fahrenheit.set(int((IN / 16) * 9))
                case '16:10': self.fahrenheit.set(int((IN / 16) * 10))
                case '21:9': self.fahrenheit.set(int((IN / 21) * 9))
            self.fahrenheit.trace_id = self.fahrenheit.trace("w", self.C2F)
        except:
            pass

    def C2F(self, *args):
        try:
            IN = self.fahrenheit.get()
            self.w_field.trace_remove("write", self.w_field.trace_id)
            match self.level_var.get():
                case '1:1': self.w_field.set(IN * 1)
                case '4:3': self.w_field.set(int((IN * 4) / 3))
                case '5:4': self.w_field.set(int((IN * 5) / 4))
                case '16:9': self.w_field.set(int((IN * 16) / 9))
                case '16:10': self.w_field.set(int((IN * 16) / 10))
                case '21:9': self.w_field.set(int((IN * 21) / 9))
            self.w_field.trace_id = self.w_field.trace("w", self.F2C)
        except:
            pass


