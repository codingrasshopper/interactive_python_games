# template for "Stopwatch: The Game"
import simplegui
# define global variables
count = 0
e = 0
n = 0
m = 0
started = False

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D

#def format(t):
def format(count):
    global d
    a = count // 600
    x = count % 600
    b = x // 100
    y  = x % 100
    c  = y // 10
    d = y % 10
    e = str(a) + ":" + str(b) + str(c) + "." + str(d)
    return e
  
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    global started
    timer.start()
    started = True

def stop():
    global started, m, n ,d
    if started:
        timer.stop()
        started = False
        n = n + 1
        if ( d == 0):
            m = m + 1
    
    
def reset():
    global count, n, m, started
    started = False
    timer.stop()
    count = 0
    n = 0
    m = 0

# define event handler for timer with 0.1 sec interval
def tick():
    global count
    count = count + 1
    
        
    

# define draw handler
def draw(canvas):
    global n
    global m
    canvas.draw_text(format(count), (100,100), 50, "Red")
    canvas.draw_text(str(n), (240,50), 25, "Blue")
    canvas.draw_text("/", (225,50), 25, "Red")
    canvas.draw_text(str(m), (210,50), 25, "Green")



# register event handlers
timer = simplegui.create_timer(100, tick)
# create frame
frame = simplegui.create_frame("Stopwatch", 300, 200)
frame.add_button("Start", start)
frame.add_button("Stop", stop)
frame.add_button("Reset", reset)
frame.set_draw_handler(draw)


# start frame
frame.start()

