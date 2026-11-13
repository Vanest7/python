from enum import Enum
import keyboard
import random
import time
from queue import Empty, Queue

BOARD_WIDTH = 10
BOARD_HEIGHT = 20

# Define an enumeration for movement directions
class Movement(Enum):
    down = 1
    right = 2
    left = 3
    rotate = 4

# Initialize the game screen with emojis
screen = [
    ["🔲"] * BOARD_WIDTH
    for _ in range(BOARD_HEIGHT)
]
rotations = [[(1,1),(0,0),(-2,0),(-1,-1)],
                [(0,1),(-1,0),(0,-1),(1,-2)],
                [(0,2),(1,1),(-1,1),(-2,0)],
                [(0,1),(1,0),(2,-1),(1,-2)]] 
pieces = [
    [
        ["🔳", "🔲", "🔲"],
        ["🔳", "🔳", "🔳"]
    ],
    [
        ["🔳", "🔳"],
        ["🔳", "🔳"]
    ],
    [
       ["🔲", "🔲", "🔳"],
       ["🔳", "🔳", "🔳"]
    ],
    [
        ["🔲", "🔳", "🔲"],
        ["🔳", "🔳", "🔳"]
    ],
    [
        ["🔳", "🔳", "🔳","🔳"]
    ],
    [
        ["🔳", "🔳", "🔲"],
        ["🔲", "🔳", "🔳"]
    ],
    [
        ["🔲", "🔳", "🔳"],
        ["🔳", "🔳", "🔲"]
    ]

]
rotation = 0 
occupied_positions = []
game_over = False
total_lines = 0
next_piece = None


def resetGameState(screen: list) -> list:
    """Reset the board and all fixed-block state."""
    global rotation, game_over, total_lines

    occupied_positions.clear()
    rotation = 0
    game_over = False
    for row in screen:
        row[:] = ["🔲"] * len(row)
    return screen


# Function to choose pieces
def chooseRandomPieces (pieces):
    return random.choice(pieces)

# Function to insert a new piece into the board    
def insertPiece(screen: list, piece: list) -> list:
    for row_index, row in enumerate(piece):
        for column_index, cell in enumerate(row):
            if cell == "🔳":
                screen[row_index][column_index] = cell

    return screen

# Function to print the game screen   
def printScreen(screen: list):
    score = total_lines * 100

    preview = [
        "Next piece",
        "┌────────┐",
    ]

    for row_index in range(4):
        cells = []

        for column_index in range(4):
            occupied = (
                next_piece is not None
                and row_index < len(next_piece)
                and column_index < len(next_piece[row_index])
                and next_piece[row_index][column_index] == "🔳"
            )

            cells.append("██" if occupied else "  ")

        preview.append("│" + "".join(cells) + "│")

    preview.append("└────────┘")

    lines = [
        f"Tetris | Score: {score} | Lines: {total_lines}",
        "",
    ]

    for row_index, row in enumerate(screen):
        side_panel = preview[row_index] if row_index < len(preview) else ""
        lines.append("".join(row) + "    " + side_panel)

    print(
        "\033[2J\033[H" + "\n".join(lines),
        end="",
        flush=True,
    )
    
# Function to check if the piece has reached the bottom row
def reachedBottom(screen: list) -> bool:
    for row_index, row in enumerate(screen):
        for column_index, cell in enumerate(row):
            if cell == "🔳":
                next_row = row_index + 1

                if next_row >= len(screen):
                    return True

                if screen[next_row][column_index] == "⬛":
                    return True

    return False
# Function to check the rotation
def pieceRotations(piece)-> list:
    match piece:
        case [['🔳', '🔳'], ['🔳', '🔳']]:
            
            return [
                [(0,0),(0,0),(0,0),(0,0)],
                [(0,0),(0,0),(0,0),(0,0)],
                [(0,0),(0,0),(0,0),(0,0)],
                [(0,0),(0,0),(0,0),(0,0)]]
        case [["🔳", "🔲", "🔲"],
            ["🔳", "🔳", "🔳"]]:
            
            return [
                [(1,1),(0,0),(-2,0),(-1,-1)],
                [(0,1),(-1,0),(0,-1),(1,-2)],
                [(0,2),(1,1),(-1,1),(-2,0)],
                [(0,1),(1,0),(2,-1),(1,-2)]]
        case [["🔲", "🔲", "🔳"],
            ["🔳", "🔳", "🔳"]]:
            
            return [
                [(0,2),(1,1),(0,0),(-1,-1)],
                [(2,-1),(-1,0),(0,-1),(1,-2)],
                [(0,2),(-1,1),(-2,0),(-1,-1)],
                [(0,1),(1,0),(2,-1),(-1,0)]
               ]
        case [
        ["🔲", "🔳", "🔲"],
        ["🔳", "🔳", "🔳"]]:
            
            return [
                [(1,1),(-1,1),(0,0),(-1,-1)],
                [(1,0),(-1,0),(0,-1),(1,-2)],
                [(0,2),(-1,1),(0,0),(-2,0)],
                [(0,1),(1,0),(2,-1),(0,-1)]
                ]
        case [["🔳", "🔳", "🔳","🔳"]]:
            
            return [
                [(0,0),(-1,1),(-2,2),(-3,3)],
                [(0,0),(1,-1),(2,-2),(3,-3)],
                [(0,0),(-1,1),(-2,2),(-3,3)],
                [(0,0),(1,-1),(2,-2),(3,-3)]
                ]
        case [
        ["🔳", "🔳", "🔲"],
        ["🔲", "🔳", "🔳"]]:
            
            return [
                [(1,1),(0,1),(-1,0),(0,-2)],
                [(0,1),(1,0),(0,-1),(1,-2)],
                [(1,1),(-1,1),(0,0),(-2,0)],
                [(0,1),(1,0),(0,-1),(1,-2)]
                ]
        case [
       ["🔲", "🔳", "🔳"],
       ["🔳", "🔳", "🔲"]]:
            
            return [
                [(0,2),(-1,1),(0,0),(-1,-1)],
                [(1,0),(2,-1),(-1,0),(0,-1)],
                [(0,2),(-1,1),(0,0),(-1,-1)],
                [(1,0),(2,-1),(-1,0),(0,-1)]
                ]    

# Function to clean entired rows
def cleanEntiredRows(screen):
    global total_lines;
    rows_to_remove = []
    
    for row_index, row in enumerate(screen):
        if all(cell == "⬛" for cell in row):
            rows_to_remove.append(row_index)

    if rows_to_remove:
        total_lines += len(rows_to_remove)
        removed_rows = set(rows_to_remove)

        def shifted_row(row):
            return row + sum(removed_row > row for removed_row in rows_to_remove)

        new_screen = [
        ["🔲"] * len(screen[0])
        for _ in range(len(screen))
    ]
        for row_index, row in enumerate(screen):
            if row_index not in removed_rows:
                new_screen[shifted_row(row_index)] = row[:]

        occupied_positions[:] = [
            (shifted_row(row), col)
            for row, col in occupied_positions
            if row not in removed_rows
        ]
        screen[:] = new_screen

    return screen


def canPlacePiece(screen: list, piece: list) -> bool:
    """Return whether a piece fits in its initial top-left position."""
    return all(
        row < len(screen)
        and column < len(screen[0])
        and (row, column) not in occupied_positions
        and screen[row][column] != "⬛"
        for row, piece_row in enumerate(piece)
        for column, cell in enumerate(piece_row)
        if cell == "🔳"
    )


# Function to check if game over
def gameOver(screen, piece=None):
    if piece is not None and not canPlacePiece(screen, piece):
        print("----------GAME OVER-----------")
        return True
    if game_over:
        print("----------GAME OVER-----------")
        return True
    return False

# Function for change piece colour if has reached to bottom
def changeColour(screen: list)-> list:
    for row_index, row in enumerate(screen):
        for column_index, item in enumerate(row):
            if item == "🔳":
               screen[row_index][column_index] = "⬛" 
               occupied_positions.append((row_index, column_index))
    return screen            

def lockPiece(screen, rotation, rotations):
    global game_over, next_piece

    screen = changeColour(screen)
    screen = cleanEntiredRows(screen)

    new_piece = next_piece

    if not canPlacePiece(screen, new_piece):
        game_over = True
        return screen, rotation, rotations

    screen = insertPiece(screen, new_piece)
    rotations = pieceRotations(new_piece)
    next_piece = chooseRandomPieces(pieces)

    return screen, 0, rotations

# Function to move the piece on the screen 
def movePiece(screen: list, movement: Movement, rotation: int, rotations: list) -> (list, int, list):
    if game_over:
        return screen, rotation, rotations

    if movement is Movement.down and reachedBottom(screen):
        return lockPiece(screen, rotation, rotations)

    # paint the blank screen in one line
    new_screen = [
        ["🔲"] * len(screen[0])
        for _ in range(len(screen))
    ]
    for row, col in occupied_positions:
        new_screen[row][col] = "⬛"

    rot_item = 0
    
    new_rotation = rotation
    if movement is Movement.rotate:
        if rotation == 3:
            new_rotation =  0     
        else:
            new_rotation +=1          

    for row_index, row in enumerate(screen):
        for column_index, item in enumerate(row):
            if item == "🔳":
                new_row_index = 0
                new_column_index = 0
                match movement:
                    case Movement.down:
                        new_row_index  = row_index + 1
                        new_column_index = column_index
                    case Movement.right:
                        new_row_index  = row_index
                        new_column_index = column_index + 1
                    case Movement.left:
                        new_row_index  = row_index
                        new_column_index = column_index - 1
                    case Movement.rotate:            
                        new_row_index  = row_index + rotations[new_rotation][rot_item][0]
                        new_column_index = column_index + rotations[new_rotation][rot_item][1]
                        rot_item += 1
                if not (
                    0 <= new_row_index < len(screen)
                    and 0 <= new_column_index < len(screen[0])
                ):
                    return (screen, rotation, rotations)

                if (new_row_index, new_column_index) in occupied_positions:
                    return (screen, rotation, rotations)

                new_screen[new_row_index][new_column_index] = "🔳"
    
    return (new_screen, new_rotation, rotations)


def getFallInterval():
    return max(0.1, 1.0 * (0.9 ** total_lines))

if __name__ == "__main__":
    screen = resetGameState(screen)

    first_piece = chooseRandomPieces(pieces)
    screen = insertPiece(screen, first_piece)
    rotations = pieceRotations(first_piece)
    next_piece = chooseRandomPieces(pieces)
    events = Queue()
    keyboard_hook = keyboard.hook(events.put)

    movements = {
        "down": Movement.down,
        "right": Movement.right,
        "left": Movement.left,
        "space": Movement.rotate,
    }

    last_fall = time.monotonic()
    printScreen(screen)

    try:
        while not game_over:
            screen_changed = False

            try:
                event = events.get(timeout=0.01)
            except Empty:
                event = None

            if event is not None and event.event_type == keyboard.KEY_DOWN:
                if event.name == "esc":
                    break

                movement = movements.get(event.name)

                if movement is not None:
                    screen, rotation, rotations = movePiece(
                        screen, movement, rotation, rotations
                    )
                    screen_changed = True

                    if movement is Movement.down:
                        last_fall = time.monotonic()

            now = time.monotonic()

            if not game_over and now - last_fall >= getFallInterval():
                screen, rotation, rotations = movePiece(
                    screen, Movement.down, rotation, rotations
                )
                last_fall = now
                screen_changed = True

            if screen_changed:
                printScreen(screen)

        if game_over:
            print(f"\nGAME OVER | Final score: {total_lines * 100}")

    finally:
        keyboard.unhook(keyboard_hook)




