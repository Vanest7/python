from enum import Enum
import keyboard

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
rotation = 0    

 # Function to print the game screen   
def printScreen(screen: list):
    print("\nPantalla tetris:\n")
    for row in screen:
        print("".join(map(str, row)))
    
# Function to check if the piece has reached the bottom row
def reachedBottom(screen:list):
    last_row = screen[9]
    for column in last_row:
        if column == "🔳":
            return True
    return False        
           
# Function to move the piece on the screen ºº
def movePiece(screen: list, movement: Movement, rotation: int) -> (list, int):
    # print the blank screen in one line
    new_screen = [["🔲"] * 10 for _ in range(10)]
    rot_item = 0
    rotations = [[(1,1),(0,0),(-2,0),(-1,-1)],
                [(0,1),(-1,0),(0,-1),(1,-2)],
                [(0,2),(1,1),(-1,1),(-2,0)],
                [(0,1),(1,0),(2,-1),(1,-2)]]
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
                    return (screen, rotation)
                else:
                    new_screen[new_row_index][new_column_index] = "🔳"
    printScreen(new_screen)
    reachedBottom(new_screen)
    return (new_screen, new_rotation)


if __name__ == '__main__':

    printScreen(screen)
    while not reachedBottom(screen):
        event = keyboard.read_event()
        
        if event.name == "esc":
            break
        elif event.event_type == keyboard.KEY_DOWN:
            if event.name == "down":
                (screen, rotation) = movePiece(screen, Movement.down, rotation)
            elif event.name == "right":   
                (screen, rotation) = movePiece(screen, Movement.right, rotation)
            elif event.name == "left":
                (screen, rotation) = movePiece(screen, Movement.left, rotation) 
            elif event.name == "space":
                (screen, rotation) = movePiece(screen, Movement.rotate, rotation)  





 




