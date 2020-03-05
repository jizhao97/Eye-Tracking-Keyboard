import tkinter as tk
#import subprocess import call
#Create & Configure root 
root = tk.Tk()
root.title("ELEC 490: Eye Tracking Keybaord")

tk.Grid.rowconfigure(root, 0, weight=1)
tk.Grid.columnconfigure(root, 0, weight=1)

#Create & Configure frame 
frame=tk.Frame(root)
frame.grid(row=0, column=0, sticky='NSEW')

#Program Variabes
eyeDetection = -1
displayTextBoxes = ["a","b","c","d","sentence","e","f","g","h"]

#Buttons
btn_str = [tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar()]

def button_click(buttonNum):
    global btn_str
    global displayTextBoxes
    print("button pressed!")
    displayTextBoxes[4]=displayTextBoxes[4]+displayTextBoxes[buttonNum]
    #displayTextBoxes=guessNextLetter(sentence,8)
    btn_str[4].set(displayTextBoxes[4])
    btn_str[buttonNum].set("button pressed")
    return

def middleButton_click():
    global windowPosition
    global btn_str
    print("middle button pressed!")
    btn_str[4].set("new view")
    return

btn0 =tk.Button(frame,textvariable=btn_str[0], command=lambda: button_click(0))
btn1 =tk.Button(frame,textvariable=btn_str[1],command=lambda: button_click(1))
btn2 =tk.Button(frame,textvariable=btn_str[2],command=lambda: button_click(2))
btn3 =tk.Button(frame,textvariable=btn_str[3],command=lambda: button_click(3))
btn4 =tk.Button(frame,textvariable=btn_str[4],command=lambda: middleButton_click())
btn5 =tk.Button(frame,textvariable=btn_str[5],command=lambda: button_click(5))
btn6 =tk.Button(frame,textvariable=btn_str[6],command=lambda: button_click(6))
btn7 =tk.Button(frame,textvariable=btn_str[7],command=lambda: button_click(7))
btn8 =tk.Button(frame,textvariable=btn_str[8],command=lambda: button_click(8))

button = [btn0,btn1,btn2,btn3,btn4,btn5,btn6,btn7,btn8]

tk.Grid.rowconfigure(frame, 0, weight=1)
tk.Grid.columnconfigure(frame, 0, weight=1)
button[0].grid(row=0, column=0, sticky='NSEW')
tk.Grid.rowconfigure(frame, 0, weight=1)
tk.Grid.columnconfigure(frame, 1, weight=1)
button[1].grid(row=0, column=1,columnspan=2, sticky='NSEW')
tk.Grid.rowconfigure(frame, 0, weight=1)
tk.Grid.columnconfigure(frame, 3, weight=1)
button[2].grid(row=0, column=3, sticky='NSEW')

tk.Grid.rowconfigure(frame, 1, weight=1)
tk.Grid.columnconfigure(frame, 0, weight=1)
button[3].grid(row=1, column=0, rowspan=2, sticky='NSEW')
tk.Grid.rowconfigure(frame, 1, weight=1)
tk.Grid.columnconfigure(frame, 1, weight=1)
button[4].grid(row=1, column=1,columnspan=2, rowspan=2, sticky='NSEW')
tk.Grid.rowconfigure(frame, 1, weight=1)
tk.Grid.columnconfigure(frame, 3, weight=1)
button[5].grid(row=1, column=3, rowspan=2, sticky='NSEW')

tk.Grid.rowconfigure(frame, 3, weight=1)
tk.Grid.columnconfigure(frame, 0, weight=1)
button[6].grid(row=3, column=0, sticky='NSEW')
tk.Grid.rowconfigure(frame, 2, weight=1)
tk.Grid.columnconfigure(frame, 2, weight=1)
button[7].grid(row=3, column=1,columnspan=2, sticky='NSEW')
tk.Grid.rowconfigure(frame, 3, weight=1)
tk.Grid.columnconfigure(frame, 3, weight=1)
button[8].grid(row=3, column=3, sticky='NSEW')

btn_str[0].set("a")

#main loop
root.mainloop()
