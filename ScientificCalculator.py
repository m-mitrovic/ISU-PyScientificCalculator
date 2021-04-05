# Python Scientific Calculator made by Mihajlo Mitrovic - ICS4U1 MR. TEDESCO - 2021

import math
from tkinter import *
# from tkmacosx import Button # Interpret py properly for Mac, uncomment if previewing on Mac
from enum import Enum

# Button class that lets me diffrentiate different types of buttons
class ButtonType(Enum):
    number = 0 # Used in the numberpad to insert numbers
    numberDoubleLong = 1 # Used for the elongated 0 button
    calculation = 2 # Used for the * + - / calculations
    calculationDoubleLong = 3 # Used for the elongated enter button
    operator = 4 # Used for clearing (C), +/-, and %
    scientific = 5 # Used for complex math buttons (cos, pi, root...)

# Global Variables
startingX = 4
startingY = 80
buttonSize = 60
buttonPadding = 6

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master=None)
        self.master = master
        self.init_window()
        self.configure(bg="#3d3d3d")
        
    def init_window(self):
        self.function = "Rad"
        self.operation = None

        self.master.title("Scientific Calculator")
        self.pack(fill=BOTH, expand=1)
        
        labelContainer = Frame(self, height=70, width=360, bg="#3d3d3d")
        labelContainer.pack(fill=X, expand=False)
        labelContainer.pack_propagate(0)

        # Wraps text in frame so the numbers dont leave the designated area
        self.inputField = Label(labelContainer, text="0", wraplength=340, font=("Segoe UI", 33), bg="#3d3d3d", fg="white")
        self.inputField.pack()
        labelContainer.place(x=10, y=10)

        buttonRow = 0
        self.button("C", 0, buttonRow, ButtonType.operator)
        self.button("+/-", 1, buttonRow, ButtonType.operator)
        self.button("%", 2, buttonRow, ButtonType.operator)
        self.button("÷", 3, buttonRow, ButtonType.calculation)
        
        buttonRow = 1
        self.button("7", 0, buttonRow, ButtonType.number)
        self.button("8", 1, buttonRow, ButtonType.number)
        self.button("9", 2, buttonRow, ButtonType.number)
        self.button("×", 3, buttonRow, ButtonType.calculation)

        buttonRow = 2
        self.button("4", 0, buttonRow, ButtonType.number)
        self.button("5", 1, buttonRow, ButtonType.number)
        self.button("6", 2, buttonRow, ButtonType.number)
        self.button("-", 3, buttonRow, ButtonType.calculation)
         
        buttonRow = 3
        self.button("1", 0, buttonRow, ButtonType.number)
        self.button("2", 1, buttonRow, ButtonType.number)
        self.button("3", 2, buttonRow, ButtonType.number)
        self.button("+", 3, buttonRow, ButtonType.calculation)

        buttonRow = 4
        self.button("0", 0, buttonRow, ButtonType.numberDoubleLong)
        self.button(".", 2, buttonRow, ButtonType.number)
        self.button("=", 3, buttonRow, ButtonType.calculationDoubleLong)

        self.draw_scientific_column() # Draws last 2 scientific colums

    def button(self, text, x, y, type):
        xCord = startingX+(x*buttonSize)+buttonPadding # Converts the row/column to usable x/y coordinates
        yCord = startingY+(y*buttonSize)+buttonPadding
        buttonType = ButtonType(type)

        # Creates proper button depending on the ButtonType
        if buttonType == ButtonType.number:
            self.add_button(str(text), xCord, yCord)
        elif buttonType == ButtonType.numberDoubleLong:
            self.add_button(str(text), xCord, yCord, (buttonSize*2))
        elif buttonType == ButtonType.calculation:
            self.add_calculation(str(text), xCord, yCord)
        elif buttonType == ButtonType.calculationDoubleLong:
            self.add_calculation(str(text), xCord, yCord, (buttonSize*2))
        elif buttonType == ButtonType.operator:
            self.add_operation(str(text), xCord, yCord)
        elif buttonType == ButtonType.scientific:
            self.add_scientific(str(text), xCord, yCord)

    def add_button(self, text, x=10, y=10, width=buttonSize, height=buttonSize):
        def button_clicked():
            if len(self.inputField["text"]) >= 32:
                # Restricted input over 32 characters
                print("Restricted Input")
            elif self.inputField["text"] == "0" and str(text) != ".":
                self.inputField["text"] = str(text)
            else:
                if str(text) == ".":
                    if self.inputField["text"].find(".") == -1:
                        self.inputField["text"] = str(self.inputField["text"] + text)
                    else:
                        print("DOT already present!")
                else:
                    self.inputField["text"] = str(self.inputField["text"] + text)

        buttonContainer = Frame(self, height=height, width=width)
        buttonContainer.propagate(False)
        button = Button(buttonContainer, text=text, command=button_clicked, font=("Helvetica", 20, "normal"), bg="#ced6e0", fg="black", highlightthickness=0, bd=0)
        button.pack(fill=BOTH, expand=1)
        buttonContainer.place(x=x, y=y)

    def add_calculation(self, text, x=10, y=10, width=buttonSize, height=buttonSize):
            def button_clicked():
                if self.operation is None: 
                    self.result = str(self.inputField["text"])
                    self.operation = str(text)
                    self.inputField["text"] = "0"
                elif str(text) == "=": # Performs different calculations based on the button clicked
                    if self.operation == "+":
                        self.inputField["text"] = "%g" % (float(self.result) + float(self.inputField["text"])) # %g formats the string to remove the trailing zeros
                        self.operation = None
                    elif self.operation == "-":
                        self.inputField["text"] = "%g" % (float(self.result) - float(self.inputField["text"]))
                        self.operation = None
                    elif self.operation == "×":
                        self.inputField["text"] = "%g" % (float(self.result) * float(self.inputField["text"]))
                        self.operation = None
                    elif self.operation == "÷":
                        self.inputField["text"] = "%g" % (float(self.result) / float(self.inputField["text"]))
                        self.operation = None
                    elif self.operation == "xʸ":
                        self.inputField["text"] = "%g" % (math.pow(float(self.result), float(self.inputField["text"])))
                        self.operation = None

            buttonContainer = Frame(self, height=height, width=width)
            buttonContainer.propagate(False)
            button = Button(buttonContainer, text=text, command=button_clicked, font=("Helvetica", 20, "normal"), bg="#575fcf", fg="white",  highlightthickness = 0, bd = 0)
            button.pack(fill=BOTH, expand=1)
            buttonContainer.place(x=x, y=y)

    def add_operation(self, text, x=10, y=10, width=buttonSize, height=buttonSize):
            def button_clicked():
                if str(text) == "C":  # Performs different calculations based on the button clicked
                    self.inputField["text"] = "0"
                    self.operation = None
                elif str(text) == "%":
                     self.inputField["text"] = float(self.inputField["text"]) / 100
                elif str(text) == "+/-":
                    self.inputField["text"] = "%g" % (float(self.inputField["text"]) * -1)

            buttonContainer = Frame(self, height=height, width=width)
            buttonContainer.propagate(False)
            button = Button(buttonContainer, text=text, command=button_clicked, font=("Helvetica", 20, "normal"), bg="#4b4b4b", fg="white", highlightthickness=0, bd=0)
            button.pack(fill=BOTH, expand=1)
            buttonContainer.place(x=x, y=y)

    def add_scientific(self, text, x=10, y=10, width=buttonSize, height=buttonSize):
            def button_clicked():
                if str(text) == "√":  # Performs different calculations based on the button clicked
                    self.inputField["text"] = "%g" % math.sqrt(float(self.inputField["text"]))
                    self.operation = None
                elif str(text) == "sin":
                    self.inputField["text"] = "%g" % math.sin(float(self.inputField["text"]))
                    self.operation = None
                elif str(text) == "cos":
                    self.inputField["text"] = "%g" % math.cos(float(self.inputField["text"]))
                    self.operation = None
                elif str(text) == "tan":
                    self.inputField["text"] = "%g" % math.tan(float(self.inputField["text"]))
                    self.operation = None
                elif str(text) == "sinh":
                    self.inputField["text"] = "%g" % math.sinh(float(self.inputField["text"]))
                    self.operation = None
                elif str(text) == "cosh":
                    self.inputField["text"] = "%g" % math.cosh(float(self.inputField["text"]))
                    self.operation = None
                elif str(text) == "tanh":
                    self.inputField["text"] = "%g" % math.tanh(float(self.inputField["text"]))
                    self.operation = None
                elif str(text) == "x²":
                    self.inputField["text"] = "%g" % math.pow(float(self.inputField["text"]), 2)
                    self.operation = None
                elif str(text) == "x³":
                    self.inputField["text"] = "%g" % math.pow(float(self.inputField["text"]), 3)
                    self.operation = None
                elif str(text) == "xʸ":
                    self.result = str(self.inputField["text"])
                    self.operation = str(text)
                    self.inputField["text"] = "0"
                elif str(text) == "π":
                    self.inputField["text"] = math.pi
                    self.operation = None

            buttonContainer = Frame(self, height=height, width=width)
            buttonContainer.propagate(False)
            button = Button(buttonContainer, text=text, command=button_clicked, font=("Helvetica", 17, "normal"), bg="#4b4b4b", fg="white", highlightthickness=0, bd=0)
            button.pack(fill=BOTH, expand=1)
            buttonContainer.place(x=x, y=y)

    def draw_scientific_column(self):
        buttonContainer = Frame(self, height=buttonSize, width=buttonSize)
        buttonContainer.propagate(False)

        self.radLabel = Button(buttonContainer, text=self.function, command=self.changeScientific, font=("Segoe UI", 17, "normal"), bg="#4b4b4b", fg="white", highlightthickness=0, bd=0)
        self.radLabel.pack(fill=BOTH, expand=1)
        buttonContainer.place(x=startingX+(4*buttonSize)+buttonPadding, y=startingY+buttonPadding)
        self.draw_scientific()
        self.draw_second_scientific()

    def draw_scientific(self):
        xCord = (startingX+(4*buttonSize)+buttonPadding)
        if self.function == "Rad":
            radButtons = ["cos", "sin", "tan"]
            for i in range(len(radButtons)):
                yCord = startingY+((i+1)*buttonSize+1)+buttonPadding
                self.add_scientific(radButtons[i], xCord, yCord)
        else:
            radButtons = ["cosh", "sinh", "tanh"]
            for i in range(len(radButtons)):
                yCord = startingY+((i+1)*buttonSize+1)+buttonPadding
                self.add_scientific(radButtons[i], xCord, yCord)

    def draw_second_scientific(self):
        xCord = (startingX+(5*buttonSize)+buttonPadding)
        radButtons = ["√", "x²", "x³", "xʸ", "π"]
        for i in range(len(radButtons)):
                yCord = startingY+(i*buttonSize+1)+buttonPadding
                self.add_scientific(radButtons[i], xCord, yCord)

    def changeScientific(self):
        if self.function == "Rad":
            self.function = "Hyp"
            self.draw_scientific_column()
        else:
            self.function = "Rad"
            self.draw_scientific_column()

root = Tk()
root.geometry("380x395")
root.resizable(False, False)
app = Window(root)
root.mainloop()