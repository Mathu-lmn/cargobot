
from tkinter import * # type: ignore
from tkinter.ttk import * # type: ignore
from cargobot import *
from typing import List

window_background_color = "#ECECEC"

COLUMN_WIDTH = 50
BOX_SIDE_LENGTH = 30
BOX_SPACING = 4
TOP_MARGIN = 10
CRANE_ARM_TOP_Y = TOP_MARGIN + 20
CRANE_ARM_BOTTOM_Y = CRANE_ARM_TOP_Y + 30


class CraneView(Canvas):
    def __init__(self, parent: Tk, crane: Crane) -> None:
        Canvas.__init__(self, parent, width=crane.num_columns * COLUMN_WIDTH, highlightthickness=0)
        self.crane = crane

    def draw_box(self, center_x: int, center_y: int, box: str) -> None:
        if box == "M":
            color = "Tomato"
        elif box == "X":
            color = "steelblue"
        elif box == "O":
            color = "Orange"
        self.create_rectangle(
            center_x - BOX_SIDE_LENGTH // 2,
            center_y - BOX_SIDE_LENGTH // 2,
            center_x + BOX_SIDE_LENGTH // 2,
            center_y + BOX_SIDE_LENGTH // 2,
            outline="grey",
            width=1.5,
            fill=color,
        )
        self.create_text(center_x, center_y, text=box)

    def redraw(self) -> None:
        canvas_height = self.winfo_height()
        canvas_width = self.winfo_width()
        self.delete(ALL)

        self.create_rectangle(0, 0, canvas_width, canvas_height, fill=window_background_color, width=0)

        # dessin de la ligne supérieure
        num_columns = self.crane.num_columns
        width = num_columns * COLUMN_WIDTH
        self.create_line(0, TOP_MARGIN, width, TOP_MARGIN, width=2)

        # dessin de la grue à la bonne position
        position = self.crane.position
        crane_center_x = position * COLUMN_WIDTH + COLUMN_WIDTH // 2
        crane_left_arm_x = crane_center_x - BOX_SIDE_LENGTH // 2 - 4
        crane_right_arm_x = crane_center_x + BOX_SIDE_LENGTH // 2 + 4
        self.create_line(
            crane_center_x, TOP_MARGIN, crane_center_x, CRANE_ARM_TOP_Y, width=2
        )  # vertical
        self.create_line(
            crane_left_arm_x,
            CRANE_ARM_TOP_Y,
            crane_right_arm_x,
            CRANE_ARM_TOP_Y,
            width=2,
        )  # horizontal
        self.create_line(
            crane_left_arm_x,
            CRANE_ARM_TOP_Y,
            crane_left_arm_x,
            CRANE_ARM_BOTTOM_Y,
            width=2,
        )  # bras de gauche
        self.create_line(
            crane_right_arm_x,
            CRANE_ARM_TOP_Y,
            crane_right_arm_x,
            CRANE_ARM_BOTTOM_Y,
            width=2,
        )  # bras de droite

        # boîte dans la grue si nécessaire
        if self.crane.held_box is not None:
            self.draw_box(crane_center_x, 30 + 4 + BOX_SIDE_LENGTH // 2, self.crane.held_box)

        # boîte dans les colonnes
        bottom = canvas_height - 10
        self.create_line(0, bottom + 2, width, bottom + 2)
        for col_index, column in enumerate(self.crane.box_placements):
            for box_index, box in enumerate(column):
                box_center_x = col_index * COLUMN_WIDTH + COLUMN_WIDTH // 2
                box_center_y = (
                    bottom
                    - box_index * (BOX_SIDE_LENGTH + BOX_SPACING)
                    - BOX_SIDE_LENGTH // 2
                    - 2
                )
                self.draw_box(box_center_x, box_center_y, box)



LINE_HEIGHT = 35
INSTRUCTION_BOX_WIDTH = 40
INSTRUCTION_BOX_HEIGHT = 26
INSTRUCTION_BOX_SPACING = 10
LEFT_MARGIN = 40
TOP_MARGIN = 5


class ProgramView(Canvas):
    def __init__(self, parent: Tk) -> None:
        Canvas.__init__(self, parent, height=2 * TOP_MARGIN + 4 * LINE_HEIGHT, highlightthickness=0)

    def redraw(
        self,
        program: Program,
        current_subprogram: Optional[List[str]],
        current_instruction_index: int,
    ) -> None:
        height = self.winfo_height()
        width = self.winfo_width()

        self.delete(ALL)
        self.create_rectangle(0, 0, width, height, fill=window_background_color, width=0)


        # boucle pour les 4 sous-programmes P1 à P4
        for i, subprogram in enumerate(
            [program.P1, program.P2, program.P3, program.P4]
        ):

            # dessin du titre
            instruction_center_y = TOP_MARGIN + i * LINE_HEIGHT + LINE_HEIGHT // 2
            self.create_text(LEFT_MARGIN // 3, instruction_center_y, text=f"P{i + 1}:")

            # dessin de chaque instruction
            for j, instr in enumerate(subprogram):
                instruction_center_x = (
                    LEFT_MARGIN
                    + j * (INSTRUCTION_BOX_SPACING + INSTRUCTION_BOX_WIDTH)
                    + INSTRUCTION_BOX_WIDTH // 2
                )
                instruction_x = instruction_center_x - INSTRUCTION_BOX_WIDTH // 2
                instruction_y = instruction_center_y - INSTRUCTION_BOX_HEIGHT // 2
                instruction_width = INSTRUCTION_BOX_WIDTH
                instruction_height = INSTRUCTION_BOX_HEIGHT

                is_condition: bool = instr in (IF_BOX, IF_NO_BOX, IF_BOX_M, IF_BOX_O, IF_BOX_X)
                if is_condition:
                    margin = 4
                    instruction_y -= margin
                    instruction_width += (
                        margin + INSTRUCTION_BOX_SPACING + INSTRUCTION_BOX_WIDTH
                    )
                    instruction_height += 2 * margin
                    instruction_center_x += margin

                # paramètres d'affichage
                background_color = "white"
                stroke_color = "grey"
                stroke_width = 1
                if subprogram is current_subprogram and j == current_instruction_index:
                    if is_condition:
                        background_color = "yellow"
                    elif instr in (GO_LEFT, GO_RIGHT, GO_DOWN_AND_UP):
                        background_color = "pink"
                    else:
                        background_color = "lightgrey"
                    stroke_width = 3
                    stroke_color = "lightgrey"

                self.create_rectangle(
                    instruction_x,
                    instruction_y,
                    instruction_x + instruction_width,
                    instruction_y + instruction_height,
                    outline=stroke_color,
                    width=stroke_width,
                    fill=background_color,
                )

                self.create_text(
                    instruction_center_x, instruction_center_y, text=str(instr)
                )