from enum import Enum
import keyboard
import random

# Define an enumeration for movement directions
class Movement(Enum):
    down = 1
    right = 2
    left = 3
    rotate = 4

# Initialize the game screen with emojis
screen = [  ["🔳","🔲","🔲","🔲","🔲","🔲","🔲","🔲","🔲","🔲"],
            ["🔳","🔳","🔳","🔲","🔲","🔲","🔲","🔲","🔲","🔲"],
            ["🔲","🔲","🔲","🔲","🔲","🔲","🔲","🔲","🔲","🔲"],
            ["🔲","🔲","🔲","🔲","🔲","🔲","🔲","🔲","🔲","🔲"],
            ["🔲","🔲","🔲","🔲","🔲","🔲","🔲","🔲","🔲","🔲"],
            ["🔲","🔲","🔲","🔲","🔲","🔲","🔲","🔲","🔲","🔲"],
            ["🔲","🔲","🔲","🔲","🔲","🔲","🔲","🔲","🔲","🔲"],
            ["🔲","🔲","🔲","🔲","🔲","🔲","🔲","🔲","🔲","🔲"],
            ["🔲","🔲","🔲","🔲","🔲","🔲","🔲","🔲","🔲","🔲"],
            ["🔲","🔲","🔲","🔲","🔲","🔲","🔲","🔲","🔲","🔲"]
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
# Function to choose pieces
def chooseRandomPieces (pieces):
    return random.choice(pieces)

# Function to insert a new piece into the board    
def insertPiece(screen: list, piece: list) -> list:
    for i in range(len(piece)):
        for j in range(len(piece[0])):
            screen[i][j] = piece[i][j]                   
    return screen

# Function to print the game screen   
def printScreen(screen: list):
    print("\nPantalla tetris:\n")
    for row in screen:
        print("".join(map(str, row)))
    
# Function to check if the piece has reached the bottom row
def reachedBottom(screen:list)-> bool:
    for row in range(len(screen[0])):
        for column in range(len(screen[0])):
            if screen[9][column] == "🔳":
                return True
            if screen[row][column] =="⬛":
                if screen[row-1][column] == "🔳":
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
        
    
# Function for change piece colour if has reached to bottom
def changeColour(screen: list)-> list:
    for row_index, row in enumerate(screen):
        for column_index, item in enumerate(row):
            if item == "🔳":
               screen[row_index][column_index] = "⬛" 
               occupied_positions.append((row_index, column_index))
               print(occupied_positions)
    return screen            

# Function to move the piece on the screen 
def movePiece(screen: list, movement: Movement, rotation: int, rotations: list) -> (list, int, list):
    # paint the blank screen in one line
    new_screen = [["🔲"] * 10 for _ in range(10)]
    
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
                if new_row_index > 9 or new_column_index > 9 or new_column_index < 0:
                 return (screen, rotation, rotations)
                else:
                    new_screen[new_row_index][new_column_index] = "🔳"
    state = reachedBottom(new_screen)
    if state:
        new_screen = changeColour(new_screen)
        new_piece = chooseRandomPieces(pieces)
        new_screen = insertPiece(new_screen, new_piece)
        rotations = pieceRotations(new_piece)
        new_rotation = 0    
    return (new_screen, new_rotation, rotations)


if __name__ == '__main__':

    printScreen(screen)
    while(True):
        event = keyboard.read_event()
        
        if event.name == "esc":
            break
        elif event.event_type == keyboard.KEY_DOWN:
            if event.name == "down":
                (screen, rotation, rotations) = movePiece(screen, Movement.down, rotation, rotations)
            elif event.name == "right":   
                (screen, rotation, rotations) = movePiece(screen, Movement.right, rotation, rotations)
            elif event.name == "left":
                (screen, rotation, rotations) = movePiece(screen, Movement.left, rotation, rotations) 
            elif event.name == "space":
                (screen, rotation, rotations) = movePiece(screen, Movement.rotate, rotation, rotations)  
        printScreen(screen)

    


 







