from tkinter import * # type: ignore
from tkinter.ttk import * # type: ignore
from cargobot import *
from time import sleep
from threading import Thread
from widgets import CraneView, ProgramView

root = Tk()

exercise = VerticalSort

crane = make_crane(exercise.initial_box_placement)

program = exercise.program

program_view = ProgramView(root)
program_view.grid(row = 1, column = 0, columnspan = 3, sticky = NSEW)

crane_view = CraneView(root, crane)
crane_view.grid(row = 0, column = 0, columnspan = 3, sticky = NSEW)

root.rowconfigure(0, weight = 1)
for i in range(3):
    root.columnconfigure(i, weight = 1)

def pause() -> None:
    sleep(0.05)

def execute_program(program:Program, subprogram:List[str])->None:
    condition = True
    for i, instruction in enumerate(subprogram):
        if crane.is_in_place(exercise.target_box_placement):
            return
        elif not condition:
            condition = True
        else:
                if instruction == GO_LEFT:
                    crane.go_left()
                    update_view(subprogram, i)
                    pause()
                elif instruction == GO_RIGHT:
                    crane.go_right()
                    update_view(subprogram, i)
                    pause()
                elif instruction == GO_DOWN_AND_UP:
                    crane.go_down_and_up()
                    update_view(subprogram, i)
                    pause()
                elif instruction == IF_BOX:
                    condition = crane.held_box is not None
                    pause()
                elif instruction == IF_NO_BOX:
                    condition = crane.held_box is None
                    pause()
                elif instruction == IF_BOX_X:
                    condition = crane.held_box == X
                elif instruction == IF_BOX_M:
                    condition = crane.held_box == M
                elif instruction == IF_BOX_O:
                    condition = crane.held_box == O
                
                else:
                    update_view(subprogram, i)
                    if instruction == GO_TO_P1:
                        pause()
                        execute_program(program, program.P1)
                    elif instruction == GO_TO_P2:
                        pause()
                        execute_program(program, program.P2)
                    elif instruction == GO_TO_P3:
                        pause()
                        execute_program(program, program.P3)
                    elif instruction == GO_TO_P4:
                        pause()
                        execute_program(program, program.P4)

def update_view(executed_list: Optional[List[str]] = None, executed_index: int = -1) -> None:
    program_view.redraw(program, executed_list, executed_index)
    crane_view.update()
    crane_view.redraw()

def go_left():
    crane.go_left()
    update_view()

def go_right():
    crane.go_right()
    update_view()

def go_down_and_up():
    crane.go_down_and_up()
    update_view()

def run() -> None:
    def do_execute() -> None:
        execute_program(program, program.P1)
        update_view(None, -1)
    thread = Thread(target=do_execute)
    thread.start()
    


button_left = Button(root, text = "Left", command = go_left)
button_left.grid(row = 2, column = 0, sticky = NSEW)

button_right= Button(root, text = "Right", command = go_right)
button_right.grid(row = 2, column = 2, sticky = NSEW)

button_middle = Button(root, text = "Down", command = go_down_and_up)
button_middle.grid(row = 2, column = 1, sticky = NSEW)

run = Button(root, text = "Run", command = run)
run.grid(row = 3, column = 0, columnspan = 3, sticky = NSEW)


update_view()
root.mainloop()