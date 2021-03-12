from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Crane:
    num_columns: int
    box_placements: List[List[str]]
    position: int
    held_box: Optional[str]
   
    def __repr__(self) -> str:
        parts: List[str] = []

        # crane rows
        for _ in range(self.position):
            parts.append("-----")
        parts.append("--|--")
        for _ in range(self.position + 1, self.num_columns):
            parts.append("-----")
        parts.append("\n")
        for _ in range(self.position):
            parts.append("     ")
        parts.append("  |\n")
        for _ in range(self.position):
            parts.append("     ")
        parts.append(" +-+\n")
        for _ in range(self.position):
            parts.append("     ")
        if self.held_box is not None:
            parts.append(f" |{self.held_box}|")
        else:
            parts.append(" | |")
        parts.append("\n\n")

        # box positions
        max_height = max(map(len, self.box_placements))
        for h in range(max_height, 0, -1):
            for i in range(self.num_columns):
                if len(self.box_placements[i]) >= h:
                    parts.append(f"  {self.box_placements[i][h - 1]}  ")
                else:
                    parts.append("     ")
            parts.append("\n")

        # bottom row
        for _ in range(self.num_columns):
            parts.append("-----")
        parts.append("\n\n")

        return "".join(parts)
    
    def go_right(self):
        if self.position < self.num_columns - 1:
            self.position += 1
        else:
           raise RuntimeError("bad move")
    def go_left(self):
        if self.position > 0:
            self.position -= 1      
        else:
           raise RuntimeError("bad move")
    def go_down_and_up(self):
        if self.held_box is not None:
            self.box_placements[self.position].append(self.held_box)
            self.held_box = None
        else:
            if len(self.box_placements[self.position]) > 0:
                self.held_box = self.box_placements[self.position].pop()  
            
    def is_in_place(self, state: List[List[str]]) -> bool:
        return self.box_placements == state



def make_crane(initial_box_placements: List[List[int]]) -> Crane:
    return Crane(
        num_columns = len(initial_box_placements),
        box_placements = initial_box_placements,
        position = 0,
        held_box = None,
    )

GO_LEFT:str = "<--"
GO_RIGHT:str = "-->"
GO_DOWN_AND_UP:str = "\V/"

GO_TO_P1 = "Pr1"
GO_TO_P2 = "Pr2"
GO_TO_P3 = "Pr3"
GO_TO_P4 = "Pr4"

X = "X"
O = "O"
M = "M"

IF_BOX = "*?:"
IF_NO_BOX = "_?:"
IF_BOX_X = "X?:"
IF_BOX_O = "O?:"
IF_BOX_M = "M?:"

@dataclass
class Program:
    P1: List[int]
    P2: List[int]
    P3: List[int]
    P4: List[int]

    def __repr__(self) -> str:
        return self.repr_with_highlight(None, -1)

    def repr_with_highlight(
        self, executed_list: Optional[List[str]], executed_index: int
    ) -> str:
        parts: List[str] = []

        def append_list(list: List[str]) -> None:
            length = len(list)
            if length == 0:
                parts.append("(vide)\n")
            else:
                my_highlight_index = executed_index if list is executed_list else -1
                subparts: List[str] = []
                for i in range(length):
                    subparts.append("|" if i == my_highlight_index else " ")
                    subparts.append(f"{list[i]}")
                    subparts.append("|" if i == my_highlight_index else " ")
                    subparts.append(" ")
                subparts.append("\n")
                parts.append("".join(subparts))

        parts.append("P1:   ")
        append_list(self.P1)
        parts.append("P2:   ")
        append_list(self.P2)
        parts.append("P3:   ")
        append_list(self.P3)
        parts.append("P4:   ")
        append_list(self.P4)
        return "".join(parts)

def make_program(P1: List[str], P2: List[str] = [], P3: List[str] = [], P4: List[str] = []) -> Program:
    return Program(P1, P2, P3, P4)


@dataclass
class Exercise:
    initial_box_placement: List[List[str]]
    target_box_placement: List[List[str]]
    program: Program

GoLeft = Exercise(
    initial_box_placement = [
        [],
        [X, X, X],
        [O, O, O],
        [M, M, M]
    ],
    target_box_placement = [
        [X, X, X],
        [O, O, O],
        [M, M, M],
        []
    ],
    program = make_program(
        P1 = [IF_NO_BOX, GO_RIGHT, GO_DOWN_AND_UP, IF_BOX, GO_LEFT, GO_TO_P1]
    )
)
EndlessLoop = Exercise(
    initial_box_placement = [
        [X],
        [O, X, O, X],
        [M, M, M],
        [],
        []
    ],
    target_box_placement = [],
    program = make_program(
        P1 = [GO_RIGHT, GO_RIGHT, GO_TO_P2],
        P2 = [GO_DOWN_AND_UP, GO_RIGHT, GO_DOWN_AND_UP, GO_LEFT, GO_TO_P2]
    )
)

AllRight = Exercise(
    initial_box_placement = [
        [],
        [],
        [X, X, X],
        [X],
        [],
        [],
        [X, X]
    ],
    target_box_placement = [
        [X, X, X, X, X, X],
        [],
        [],
        [],
        [],
        [],
        []
    ],
    program = make_program(
        P1 = [GO_TO_P2, GO_TO_P2, GO_TO_P2, GO_TO_P2, GO_TO_P2, GO_TO_P2],
        P2 = [GO_TO_P3, GO_DOWN_AND_UP],
        P3 = [GO_RIGHT, GO_DOWN_AND_UP, IF_NO_BOX, GO_TO_P3, GO_LEFT]
    )
)

AllRightSelective = Exercise(
    initial_box_placement = [
        [],
        [X],
        [X, O, O],
        [X],
        [X, O],
        [X],
        [O, O, O, O]
    ],
    target_box_placement = [
        [O, O, O, O, O, O, O],
        [X],
        [X],
        [X],
        [X],
        [X],
        []
    ],
    program = make_program(
        P1 = [GO_TO_P2],
        P2 = [GO_TO_P3, GO_DOWN_AND_UP, GO_TO_P2],
        P3 = [GO_RIGHT, GO_DOWN_AND_UP, IF_BOX_X, GO_DOWN_AND_UP, IF_NO_BOX, GO_TO_P3, GO_LEFT]
    )
)

MultiSort = Exercise(
    initial_box_placement = [
        [],
        [X, M, O, X, M, M],
        [],
        [O, O, X, X, M, O],
        []
    ],
    target_box_placement = [
        [X, X, X, X],
        [],
        [O, O, O, O],
        [],
        [M, M, M, M]
    ],
    program = make_program(
        P1 = [IF_BOX_X, GO_DOWN_AND_UP, GO_TO_P4, IF_BOX_O, GO_DOWN_AND_UP, GO_TO_P4, IF_BOX_M, GO_DOWN_AND_UP, GO_TO_P2],
        P2 = [GO_LEFT, GO_LEFT, GO_LEFT, GO_LEFT, GO_TO_P1],
        P4 = [GO_RIGHT, IF_NO_BOX, GO_DOWN_AND_UP, GO_RIGHT]
    )
)

VerticalSort = Exercise(
    initial_box_placement = [
        [],
        [X, O, X, O, O],
        [O, X, O],
        [X, O, O, X],
        [O, X],
        [O, X, X, X, O],
        []
    ],
    target_box_placement = [
        [],
        [X, X, O, O, O],
        [X, O, O],
        [X, X, O, O],
        [X, O],
        [X, X, X, O, O],
        []
    ],
    program = make_program(
        P1 = [GO_RIGHT, GO_DOWN_AND_UP, GO_TO_P2, GO_TO_P1],
        P2 = [IF_BOX_X, GO_TO_P3, IF_BOX_O, GO_TO_P4, GO_DOWN_AND_UP, IF_BOX, GO_TO_P2, GO_TO_P3, IF_BOX_O, GO_TO_P3, IF_NO_BOX, GO_TO_P4, GO_DOWN_AND_UP],
        P3 = [GO_LEFT, GO_DOWN_AND_UP, GO_RIGHT],
        P4 = [GO_RIGHT, GO_DOWN_AND_UP, GO_LEFT]
    )
)