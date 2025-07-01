from tkinter import Tk, messagebox, simpledialog, Canvas, Label, ALL, Button, Frame
import random
import os

GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 100
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"
SCORE_FILE = "best_score.txt"

# Create window
window = Tk()
window.title("Snake game")
window.resizable(False, False)

score = 0
best_score = 0
direction = 'down'
restart_button = None

# Load best score if it exists
def load_best_score():
    global best_score
    try:
        if os.path.exists(SCORE_FILE):
            with open(SCORE_FILE, "r") as file:
                best_score = int(file.read().strip())
    except:
        best_score = 0

# Save best score
def save_best_score():
    with open(SCORE_FILE, "w") as file:
        file.write(str(best_score))

# Load best score at start
load_best_score()

# Create score frame
score_frame = Frame(window)
score_frame.pack()

label = Label(score_frame, text="Score: {}".format(score), font=('consolas', 30))
label.grid(row=0, column=0, padx=20)

best_score_label = Label(score_frame, text="Best Score: {}".format(best_score), font=('consolas', 30))
best_score_label.grid(row=0, column=1, padx=20)

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()


class Snake:

    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(
                x, y, 
                x + SPACE_SIZE, y + SPACE_SIZE, 
                fill=SNAKE_COLOR, 
                tag="snake"
            )
            self.squares.append(square)


class Food:

    def __init__(self):

        x = random.randint(0, int((GAME_WIDTH / SPACE_SIZE)-1)) * SPACE_SIZE
        y = random.randint(0, int((GAME_HEIGHT / SPACE_SIZE) - 1)) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(
            x, y, 
            x + SPACE_SIZE, y + SPACE_SIZE, 
            fill=FOOD_COLOR, 
            tag="food"
        )


def next_turn(snake, food):

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(
        x, y, 
        x + SPACE_SIZE, y + SPACE_SIZE, 
        fill=SNAKE_COLOR
    )

    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:

        global score, best_score

        score += 1

        label.config(text="Score: {}".format(score))
        
        # Update best score if needed
        if score > best_score:
            best_score = score
            best_score_label.config(text="Best Score: {}".format(best_score))
            save_best_score()

        canvas.delete("food")

        food = Food()

    else:

        del snake.coordinates[-1]

        canvas.delete(snake.squares[-1])

        del snake.squares[-1]

    if check_collisions(snake):
        game_over()

    else:
        window.after(SPEED, next_turn, snake, food)


def change_direction(new_direction):

    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction


def check_collisions(snake):

    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False


def game_over():
    global restart_button
    
    canvas.delete(ALL)
    canvas.create_text(
        int(canvas.winfo_width()/2),
        int(canvas.winfo_height()/2),
        text="GAME OVER",
        font=('consolas', 70),
        fill="red",
        tag="gameover"
    )
    
    # Display final score
    canvas.create_text(
        int(canvas.winfo_width()/2),
        int(canvas.winfo_height()/2) + 50,
        text=f"Score: {score}",
        font=('consolas', 30),
        fill="white",
        tag="final_score"
    )
    
    restart_button = Button(window, text="Restart", font=('consolas', 20), command=restart_game)
    restart_button_window = canvas.create_window(
        int(canvas.winfo_width()/2), 
        int(canvas.winfo_height()/2) + 120,
        window=restart_button
    )


def restart_game():
    global score, direction, restart_button
    
    # Reset game variables
    score = 0
    direction = 'down'
    
    # Update score label
    label.config(text="Score: {}".format(score))
    
    # Clear canvas
    canvas.delete(ALL)
    
    # Remove restart button
    if restart_button:
        restart_button.destroy()
        restart_button = None
    
    # Create new snake and food
    snake = Snake()
    food = Food()
    
    # Start game
    next_turn(snake, food)


window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop()
