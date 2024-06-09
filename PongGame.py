import arcade

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Pong Game"

PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
PADDLE_SPEED = 10

BALL_SIZE = 20
BALL_SPEED = 4

class Paddle(arcade.SpriteSolidColor):
    def __init__(self, x, y):
        super().__init__(PADDLE_WIDTH, PADDLE_HEIGHT, arcade.color.WHITE)
        self.center_x = x
        self.center_y = y

    def move_up(self):
        if self.top < SCREEN_HEIGHT:
            self.center_y += PADDLE_SPEED

    def move_down(self):
        if self.bottom > 0:
            self.center_y -= PADDLE_SPEED

class Ball(arcade.SpriteSolidColor):
    def __init__(self, x, y):
        super().__init__(BALL_SIZE, BALL_SIZE, arcade.color.WHITE)
        self.center_x = x
        self.center_y = y
        self.change_x = BALL_SPEED
        self.change_y = BALL_SPEED

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Bounce off top and bottom
        if self.top > SCREEN_HEIGHT or self.bottom < 0:
            self.change_y *= -1

        # Reset if it goes out of bounds left or right
        if self.left > SCREEN_WIDTH or self.right < 0:
            self.center_x = SCREEN_WIDTH // 2
            self.center_y = SCREEN_HEIGHT // 2
            self.change_x *= -1

class PongGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.paddle_left = Paddle(50, SCREEN_HEIGHT // 2)
        self.paddle_right = Paddle(SCREEN_WIDTH - 50, SCREEN_HEIGHT // 2)
        self.ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.sound = arcade.load_sound('pong-ball-hit.wav')
        self.holding_w = False
        self.holding_s = False
        self.holding_up = False
        self.holding_down = False
        self.score_left = 0
        self.score_right = 0


    def on_draw(self):
        arcade.start_render()
        self.paddle_left.draw()
        self.paddle_right.draw()
        self.ball.draw()
        arcade.draw_text(f"Score: {self.score_left} - {self.score_right}", 10, 20, arcade.color.WHITE, 20)

    def update(self, delta_time):
        self.ball.update()

        # Ball collision with paddles
        if self.ball.collides_with_sprite(self.paddle_left) or self.ball.collides_with_sprite(self.paddle_right):
            self.ball.change_x *= -1
            arcade.play_sound(self.sound)

          # Ball out of bounds
        if self.ball.left < 0:
            self.score_right += 1
            self.ball.center_x = SCREEN_WIDTH // 2
            self.ball.center_y = SCREEN_HEIGHT // 2
            self.ball.change_x *= -1
        elif self.ball.right > SCREEN_WIDTH:
            self.score_left += 1
            self.ball.center_x = SCREEN_WIDTH // 2
            self.ball.center_y = SCREEN_HEIGHT // 2
            self.ball.change_x *= -1    

         # Move paddles based on key holds
        if self.holding_w and self.paddle_left.top < SCREEN_HEIGHT:
            self.paddle_left.center_y += PADDLE_SPEED
        if self.holding_s and self.paddle_left.bottom > 0:
            self.paddle_left.center_y -= PADDLE_SPEED
        if self.holding_up and self.paddle_right.top < SCREEN_HEIGHT:
            self.paddle_right.center_y += PADDLE_SPEED
        if self.holding_down and self.paddle_right.bottom > 0:
            self.paddle_right.center_y -= PADDLE_SPEED
    

            

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.holding_w = True
        elif key == arcade.key.S:
            self.holding_s = True
        elif key == arcade.key.UP:
            self.holding_up = True
        elif key == arcade.key.DOWN:
            self.holding_down = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W:
            self.holding_w = False
        elif key == arcade.key.S:
            self.holding_s = False
        elif key == arcade.key.UP:
            self.holding_up = False
        elif key == arcade.key.DOWN:
            self.holding_down = False

def main():
     game = PongGame()
     arcade.run()

if __name__ == "__main__":
    main()
