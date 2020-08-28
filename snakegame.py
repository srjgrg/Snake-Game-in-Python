import tkinter as tk
from PIL import Image, ImageTk
from random import randint

# Image = loads the image, ImageTk = places it on a tkinter widget

MOVE_INCREMENT = 20  # snake new head position
moves_per_second = 15
GAME_SPEED = 1000 // moves_per_second


class Snake(tk.Canvas):  # inherit from TK.Canvas. Our snake class is now canvas
    def __init__(self):
        super().__init__(width=600, height=620, background="black", highlightthickness=0)  # supper class

        self.snake_positions = [(100, 100), (80, 100), (60, 100)]  # creats where snake going to start
        # seperating elements body by 20 pixels wide
        self.food_position = self.set_new_food_position()
        self.score = 0
        self.direction = "Right"
        self.bind_all("<Key>", self.on_key_press)  # whenever key is press it binds all the key

        self.load_assets()
        self.create_objects()

        self.after(75, self.perform_actions)

    def load_assets(self):  # takes images and import them and store them locally
        try:
            self.snake_body_image = Image.open("./assets/snake.png")  # opens image
            self.snake_body = ImageTk.PhotoImage(self.snake_body_image)  # creates photo image from that using TK class
            # and put it into self.snake body
            self.food_image = Image.open("./assets/food.png")
            self.food = ImageTk.PhotoImage(self.food_image)
        except IOError as error:
            print(error)
            root.destroy()
            raise

    def create_objects(self):
        self.create_text(  # show score on the window
            100, 12, text=f"Score: {self.score} (speed: {moves_per_second})", tag="score", fill="#fff", font=("TkDefaultFont", 10)
        )
        for x_position, y_position in self.snake_positions:
            self.create_image(x_position, y_position, image=self.snake_body, tag="snake")

        self.create_image(*self.food_position, image=self.food, tag="food")
        self.create_rectangle(7, 27, 593, 613, outline="#525d69")  # creates rectangle outline, if snakes touches line
        # the game stops

    def move_snake(self):
        head_x_position, head_y_position = self.snake_positions[0]  # snake head position

        if self.direction == "Left":
            new_head_position = (head_x_position - MOVE_INCREMENT, head_y_position)  # snake new head position
        elif self.direction == "Right":
            new_head_position = (head_x_position + MOVE_INCREMENT, head_y_position)
        elif self.direction == "Down":
            new_head_position = (head_x_position, head_y_position + MOVE_INCREMENT)
        elif self.direction == "Up":
            new_head_position = (head_x_position, head_y_position - MOVE_INCREMENT)

        self.snake_positions = [new_head_position] + self.snake_positions[:-1]  # copies the head and all the other
        # element except the last one

        for segment, position in zip(self.find_withtag("snake"), self.snake_positions):
            self.coords(segment, position)  # finds all element tag "snake" and also its positions

    def perform_actions(self):
        if self.check_collisions():
            self.end_game()
            return

        self.check_food_collision()
        self.move_snake()
        self.after(GAME_SPEED, self.perform_actions)  # calls a functions after 75 milisecond

    def check_collisions(self):
        head_x_position, head_y_position = self.snake_positions[0]

        return (  # check if the snake head has collided or not
                head_x_position in (0, 600)
                or head_y_position in (20, 620)
                or (head_x_position, head_y_position) in self.snake_positions[1:]  # check if snake eat itself
        )

    def on_key_press(self, e):  # return info which keys are pressed
        new_direction = e.keysym
        all_directions = ("Up", "Down", "Left", "Right")
        opposites = ({"Up", "Down"}, {"Left", "Right"})

        if (
                new_direction in all_directions
                and {new_direction, self.direction} not in opposites
        ):
            self.direction = new_direction

    def check_food_collision(self):
        if self.snake_positions[0] == self.food_position:
            self.score += 1
            self.snake_positions.append(self.snake_positions[-1])

            if self.score % 5 == 0:
                global moves_per_second
                moves_per_second += 1

            self.create_image(
                *self.snake_positions[-1], image=self.snake_body, tag="snake"
            )

            self.food_position = self.set_new_food_position()
            self.coords(self.find_withtag("food"), self.food_position)

            score = self.find_withtag("score")
            self.itemconfigure(score,
                               text=f"Score: {self.score} (speed: {moves_per_second})",
                               tag="score")

    def set_new_food_position(self):
        while True:
            x_position = randint(1, 29) * MOVE_INCREMENT
            y_position = randint(3, 30) * MOVE_INCREMENT
            food_position = (x_position, y_position)

            if food_position not in self.snake_positions:
                return food_position

    def end_game(self):  # ends the game and displays the final score
        self.delete(tk.ALL)
        self.create_text(
            self.winfo_width() / 2,
            self.winfo_height() / 2,
            text=f"Game over! You scored {self.score}!",
            fill="#fff",
            font=("TkDefaultFont", 24)
        )


root = tk.Tk()  # creates a main app window
root.title("Snake")  # app title
root.resizable(False, False)  # none resizable window
# root.tk.call("tk", "scaling", 4.0)

board = Snake()  # instances of our snake class
board.pack()  # putting element into the window (tkinter ways of putting elements into another element)

root.mainloop()  # runs the app
