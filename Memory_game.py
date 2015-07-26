# implementation of card game - Memory

import simplegui
import random
state = 0
y1 = 0 #index of first card exposed
y2 = 0 #index of second card exposed
turns = 0  #counter to keep track of turns
list1 = range(8)  
#print list1
list2 = range(8)
#print list2
l3 = list1 + list2
#print l3
random.shuffle(l3)
#print l3

exposed = [False] * 16

# helper function to initialize globals
def new_game():
    global state, turns, l3, exposed
    state = 0
    turns = 0
    label.set_text("Turns = " + str(turns))
    random.shuffle(l3)
    exposed = [False] * 16   #begin game by face down
    
# define event handlers
def mouseclick(position):
    # add game state logic here
    global state, y1, y2, turns
    y = position[0]//50
  #  print l3[y]--> for debugging
  #  print y--> for debugging

    if exposed[y] == True:
        return
    if state == 0:
        exposed[y] = True
        y1 = y
        state = 1      
       # print "y1 is%s"%y1-->for debugging
    elif state == 1:
        exposed[y] = True
        y2 = y
       # print "y2 is%s"%y2-->for debugging
        turns += 1
        label.set_text("Turns = " + str(turns))
        state = 2            
    else:
        
        if (l3[y1] != l3[y2]):
            exposed[y1] = False
            exposed[y2] = False
        exposed[y] = True
        y1 = y
        state = 1
 
        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    pos = 0
    for idx, task in enumerate(l3):
        if exposed[idx]:
             canvas.draw_text(str(task), (pos, 50), 24, "White")  
        else:
             canvas.draw_polygon(get_coord(pos), 8, 'Black', 'Green')
        pos += 50

#common function to get position of coordinates of rectangle       
def get_coord(pos):
    x0 = pos 
    x1 = pos + 50
    y0 = 0
    y1 = 100
    l = [[x0, y0], [x1, y0], [x1, y1], [x0, y1]]     
    return l
    
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()

