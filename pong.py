# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
ball_pos = [WIDTH / 2, HEIGHT / 2]
paddle1_vel = 0 
paddle2_vel = 0

def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
  
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    if direction == RIGHT:
        x = random.randrange(2, 4) 
        y = random.randrange(-3, -1)
    if direction == LEFT:
        x = random.randrange(-4, -2) 
        y = random.randrange(-3, -1)   
    ball_vel = [x, y]
    
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    paddle1_pos = 200
    paddle2_pos = 200
    score1 = 0
    score2 = 0
    spawn_ball(RIGHT)

#define paddle1 and paddle2 co-ordinates
def get_paddle_ord(center_x, center_y):
    x0 = center_x
    x1 = center_x + PAD_WIDTH
    y0 = center_y - HALF_PAD_HEIGHT
    y1 = center_y + HALF_PAD_HEIGHT
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]

# Make paddle bounce back at the edges
def get_pad_pos(paddle_pos, paddle_vel):
    if (paddle_pos + paddle_vel) > 40 and \
            (paddle_pos + paddle_vel) < 360:
             paddle_pos += paddle_vel
    else:
             paddle_pos -= paddle_vel
    return paddle_pos


def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, paddle1_vel
    #paddle1_pos = [(0, 160), (4, 160), (4, 240), (0, 240) ]
    #paddle2_pos = [(596, 160), (600, 160), (600, 240), (596, 240)]  
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0]+= ball_vel[0]
    ball_pos[1]+= ball_vel[1]
    
    #left wall
    if (ball_pos[0] <= BALL_RADIUS + PAD_WIDTH):
        if ((paddle1_pos - HALF_PAD_HEIGHT) <= ball_pos[1] <= (paddle1_pos + HALF_PAD_HEIGHT)):
            ball_vel[0] = -1.1 * ball_vel[0]
        else:
            spawn_ball(RIGHT)
            score2 += 1
    #right wall
    if (ball_pos[0] >= (WIDTH - 1) - (BALL_RADIUS + PAD_WIDTH)):
        if ((paddle2_pos - HALF_PAD_HEIGHT) <= ball_pos[1] <= (paddle2_pos + HALF_PAD_HEIGHT)):
            ball_vel[0] = -1.1 * ball_vel[0]
        else:
            spawn_ball(LEFT)
            score1 += 1        
    #top wall    
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
    #bottom wall
    if ball_pos[1] >= (HEIGHT - 1) - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]               
        
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")
    
    # update paddle's vertical position, keep paddle on the screen    
    paddle1_pos = get_pad_pos(paddle1_pos, paddle1_vel)
    paddle2_pos = get_pad_pos(paddle2_pos, paddle2_vel)
    
    # draw paddles
    canvas.draw_polygon(get_paddle_ord(0, paddle1_pos), 8, 'White')    
    canvas.draw_polygon(get_paddle_ord(592, paddle2_pos), 8, 'White')
    
    # draw scores
    canvas.draw_text(str(score1), (150,50), 25, "Blue")
    canvas.draw_text(str(score2), (450,50), 25, "Blue")
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    acc = 3
    if key==simplegui.KEY_MAP["w"]:
        paddle1_vel -= acc
    elif key==simplegui.KEY_MAP["s"]:
        paddle1_vel += acc
    elif key==simplegui.KEY_MAP["up"]:
        paddle2_vel -= acc
    elif key==simplegui.KEY_MAP["down"]:
        paddle2_vel += acc
    
def keyup(key):
    global paddle1_vel, paddle2_vel
    paddle1_vel = 0
    paddle2_vel = 0


def restart_handler():
    new_game()    
    
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", restart_handler)
frame.add_label("Welcome to Pong")
frame.add_label("Left Player - press w for Up, s for down")
frame.add_label("Right Player - press up arrow for Up, down arrow for down")

# start frame
new_game()
frame.start()
