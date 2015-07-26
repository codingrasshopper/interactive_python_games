# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5
started = False
rock_group = set()
missile_group = set()
explosion_group = set()


class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.s2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.7)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

def process_sprite_group(sprite_group, canvas):
    remove_set = set()
    for sprite in sprite_group:
        sprite.draw(canvas)
        if sprite.update():
            remove_set.add(sprite)
    if remove_set:
        sprite_group.difference_update(remove_set)

#for object and group collision        
def group_collide(sprite_group, other_object):
    remove_set = set()
    for sprite in sprite_group:
        if sprite.collide(other_object):
            remove_set.add(sprite)
            explosion_group.add(Sprite(sprite.get_position(), sprite.get_velocity(), 0, 0, explosion_image, explosion_info, explosion_sound))
    if remove_set:
        sprite_group.difference_update(remove_set)
       # print remove_set
    return len(remove_set)	

#For group colliding with groups
def group_group_collide(group1, group2):
    remove_set = set()
    for sprite in group1:
      if group_collide(group2, sprite)> 0:
           remove_set.add(sprite)
    if remove_set:
        group1.difference_update(remove_set)
    return len(remove_set)
        
# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
       # canvas.draw_circle(self.pos, self.radius, 1, "White", "White")
        if self.thrust:
            canvas.draw_image(ship_image, (130, 45), (90, 90), (self.pos[0], self.pos[1]), (100, 100), self.angle)
            ship_thrust_sound.play()
            ship_thrust_sound.set_volume(.2)  
        else:
            canvas.draw_image(ship_image, (45, 45), (90, 90), (self.pos[0], self.pos[1]), (100, 100), self.angle)
            ship_thrust_sound.pause()
            
    def update(self):
        #print self.pos
        global a_missile
        self.pos[0] += self.vel[0]       
        self.pos[1] += self.vel[1]
        self.pos[0] %= WIDTH
        self.pos[1] %= HEIGHT
        self.vel[0] *= (1-0.005)   #ship velocity
        self.vel[1] *= (1-0.005)
        self.angle += self.angle_vel
        forward = angle_to_vector(self.angle)
        if self.thrust:
            self.vel[0] += 0.05 *forward[0]   #velocity of ship with thrusters
            self.vel[1] += 0.05 *forward[1]  
        
    def inc_ang_vel(self):
        self.angle_vel = 0
        self.angle_vel += 0.1 
        my_ship.update()
        
    def dec_ang_vel(self):
        self.angle_vel = 0
        self.angle_vel -= 0.1  
        my_ship.update()
        
    def thrust_modify(self, on):
        if on == 1:              #set self.thrust depending on keypress
            self.thrust = True
        else:
           self.thrust = False
     
    def zero_angle_vel(self):
        self.angle_vel = 0
        
    def shoot(self):
        global missile_group
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] +self.radius*forward[0], self.pos[1]+ self.radius*forward[1]]
        missile_vel = [self.vel[0] + 5*forward[0], self.vel[1] +5*forward[1]]
        missile_group.add(Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound))
        
    def get_radius(self):
        return self.radius
    
    def get_position(self):
        return self.pos    
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.age = 0
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        
        if sound:
            sound.rewind()
            sound.play()
            
    def draw(self, canvas):
       # canvas.draw_circle(self.pos, self.radius, 1, "Red", "Red")
       # canvas.draw_image(asteroid_image, (45, 45), (90, 90), (self.pos[0], self.pos[1]), (100, 100), self.angle)
       # canvas.draw_image(asteroid_image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        if self.animated:
            canvas.draw_image(self.image, [self.image_center[0] + self.age % self.lifespan  * self.image_size[0],
                                           self.image_center[1]], self.image_size, self.pos, self.image_size) #explosion image
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)    #else normal image
            #canvas.draw_image(missile_image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        
        
    def update(self):
        self.angle += self.angle_vel
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH     #to bounce back if goes out of screen
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT 
        if self.age > self.lifespan:    #if age>lifespan, remove it  
            return True
        else:
            self.age += 1
        return False
        
    def get_radius(self):
        return self.radius
    
    def get_position(self):
        return self.pos
    
    def get_velocity(self):
        return self.vel
    
    def collide(self, other_object):
        return dist(self.pos, other_object.get_position()) <= self.radius + other_object.get_radius()
    
    
    
def draw(canvas):
    global time, lives, score, rock_group, missile_group, started
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_text("Lives = "+str(lives), [30, 50], 20, 'White')
    canvas.draw_text("Score = "+str(score), [700, 50], 20, 'White')
    
    # draw ship and sprites
    my_ship.draw(canvas)
    #rock_group.draw(canvas)
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    process_sprite_group(explosion_group, canvas)
   # a_missile.draw(canvas)
    
    # update ship and sprites
    my_ship.update()
  #  rock_group.update()
   # a_missile.update()
    
    no_collisions = group_collide(rock_group, my_ship)
    #print no_collisions
    if no_collisions >= 1:
        lives = lives - no_collisions
    no_collisions_spr = group_group_collide(rock_group, missile_group)
    #print no_collisions_spr
    if no_collisions_spr >= 1:
        score = score + no_collisions_spr 
        
    if lives <= 0:                    #restart 
        started = False
        my_ship.pos = [WIDTH / 2, HEIGHT / 2]
        rock_group = set([])
        missile_group = set([])
        my_ship.thrust = False
        my_ship.vel = [0, 0]
        soundtrack.pause()
        my_ship.angle = 0
        my_ship.angle_vel = 0
        
        
    #splash image at beginning and game end    
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())

#Click handler to activate screen once the -click to start- screen is clicked        
def click(pos):
    global score, lives, time, started

    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    w = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    h = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and w and h:
        # start new game
        time = 0.5
        score = 0
        lives = 3
        ship_thrust_sound.rewind()
        soundtrack.rewind()
        missile_sound.rewind()
        explosion_sound.rewind()
        
        soundtrack.play()
        started = True        

def keydown(key):
    global canvas
    if key==simplegui.KEY_MAP["left"]:
        my_ship.dec_ang_vel()
    elif key==simplegui.KEY_MAP["right"]:
        my_ship.inc_ang_vel()
    elif key==simplegui.KEY_MAP["space"]:
        my_ship.shoot()
    elif key==simplegui.KEY_MAP["up"]:   
        my_ship.thrust_modify(1)
        
        
def keyup(key):
    
    my_ship.zero_angle_vel()
    my_ship.thrust_modify(0)   
    
    
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group
    
    rock_pos = [random.randint(0,800), random.randint(0,600)]
    #rock_vel = [random.randint(0,5),random.randint(0,5)]
    #rock_angle_vel = random.choice([0, 0.1, 0.2])
    if random.random() < 0.5:
        hor_normal = -1
        ver_normal = -1
    else:
        hor_normal = 1
        ver_normal = 1
        
   
    rock_vel = [random.random() * .5 - .3 + score / 35 * hor_normal, random.random() * .5 - .3 + score / 35 * ver_normal]
    rock_angle_vel = random.random() * .2 - .1
    if started and dist(rock_pos, my_ship.get_position())> 100 and len(rock_group) < 12:
        rock_group.add(Sprite(rock_pos, rock_vel, 0, rock_angle_vel, asteroid_image, asteroid_info))
    
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
#a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [0.3, 0.4], 0, 0.1, asteroid_image, asteroid_info)
#rock_group = Sprite([WIDTH / 3, HEIGHT / 3], [0.3, 0.4], 0, 0.1, asteroid_image, asteroid_info)
#a_missile = Sprite([ (WIDTH / 3 )+ 10, HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
timer = simplegui.create_timer(1000.0, rock_spawner)
frame.set_mouseclick_handler(click)
frame.add_label('Press *Spacebar* to shoot missile')
frame.add_label('Press *Up Arrow* to turn ON thrusters for spaceship')


# get things rolling
timer.start()
frame.start()
