from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random
import time

# Camera-related variables
cheat_shoot_timer = 0
theta = math.pi/2
r = 400
camera_z = 500
camera_pos = (r* math.cos(theta), r * math.sin(theta), camera_z)
player_rotation_angle = 0
player_life = 5
missed = 0
player_pos = [0 , 0 , 0]

bullet_list = []
bullet_speed = 600 
fovY = 120 

enemies_list = []
timer = 0.0
score = 0
cheat_mode = False
camera_follow_gun = False
cheat_bullets = []

for i in range(5):
    x = random.uniform(-590,590)
    y = random.uniform(-590,590)
    z = 50
    enemies_list.append([x,y,z])

enemy_speed = 30

game_over = False

first_person_mode = False
last_frame = time.time()

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1,1,1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()

    gluOrtho2D(0, 1000, 0, 800) 

    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    

    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def draw_grid():

    initial_x = 600
    initial_y = 600
    GRID_x = initial_x
    GRID_y = initial_y
    length = (initial_x+initial_y) / 13

    color = True
    glBegin(GL_QUADS)
    for i in range(13):
        for j in range(13):
            if not color :
                glColor3f(0.7, 0.5, 0.95)
            else:
                glColor3f(1, 1, 1)
            glVertex3f(-GRID_x, GRID_y, 0)
            glVertex3f(-GRID_x + length, GRID_y, 0)
            glVertex3f(-GRID_x + length, GRID_y - length, 0)
            glVertex3f(-GRID_x, GRID_y -  length, 0)
            
            GRID_x -= length    # ekhane length - korsi karon, jokhon glVertex3f e nitesi tokhon negative GROD_x nitesi (Example: GRID_x = 600,  jokhon vertext e nei tokhon -600 hishebe nei. As a result if i subtract the length, 600 - length = 509, jeta hoye jabe vertex e -509 (which will be more left as more left means more positive))
            color = not color
        GRID_x = initial_x
        GRID_y -= length 
    
    #boundary walls
    glColor3f(0, 1, 0)
    glVertex3f(-initial_x, initial_y, 0)
    glVertex3f(-initial_x, initial_y - (13 * length), 0)
    glVertex3f(-initial_x,initial_y - (13*length), 100)
    glVertex3f(-initial_x, initial_y, 100)        
    
    glColor3f(0, 0, 1)
    glVertex3f(initial_x, initial_y, 0)
    glVertex3f(initial_x, initial_y - (13 * length), 0)
    glVertex3f(initial_x,initial_y - (13*length), 100)
    glVertex3f(initial_x, initial_y, 100)    

    
    glColor3f(67/255, 234/255, 240/255)
    glVertex3f(-initial_x, initial_y - (13 * length), 0)
    glVertex3f(-initial_x + (13 * length), initial_y - (13 * length)  , 0)
    glVertex3f(-initial_x + (13 * length),initial_y - (13 * length), 100)
    glVertex3f(-initial_x, initial_y - (13 * length), 100) 
    
    glColor3f(1,1,1)
    glVertex3f(-initial_x, initial_y , 0)
    glVertex3f(-initial_x + (13 * length), initial_y   , 0)
    glVertex3f(-initial_x + (13 * length),initial_y , 100)
    glVertex3f(-initial_x, initial_y , 100)       
    glEnd()
    



def draw_bullets(x,y,z, x_dir, y_dir):
    
        

    glPushMatrix()
    glColor3f(1,0,0)
    

    
    glTranslatef(x,y,z)

    
    glutSolidCube(8)

    glPopMatrix()
    
    
def draw_enemies(x,y,z):
    global timer
    glPushMatrix()
    glColor3f(1,0,0)
    glTranslatef(x,y,z)
    pulse_scale = 0.8 + 0.3 * math.sin(2.0 * timer)  # Scale between 0.7 and 1.3
    glScalef(pulse_scale, pulse_scale, pulse_scale)
    gluSphere(gluNewQuadric(), 50, 10, 10)
    
    glPopMatrix()
    
    glPushMatrix()
    glColor3f(0,0,0)
    glTranslatef(x,y,z+25)
    glScalef(pulse_scale, pulse_scale, pulse_scale)
    gluSphere(gluNewQuadric(), 20, 10, 10)
    glPopMatrix()


def draw_player():
    global player_pos, player_rotation_angle, game_over, player_life, first_person_mode
    x,y,z = player_pos

    glPushMatrix()
    glTranslatef(x, y, z)

    glTranslatef(- 46.1538462,46.1538462, 0)
    glRotatef(player_rotation_angle, 0, 0, 1)
    
    if missed >= 10 or player_life <= 0 :
        glRotatef(-90,1,0,0)
        game_over = True
        first_person_mode = False
    
    #body
    glPushMatrix()
    glColor3f(50/255, 168/255, 82/255)
    

    
    glTranslatef(0, 0, 50)
    glScale(0.7,0.4, 1)
    glutSolidCube(50)
    glPopMatrix()
    

   
    #legs
    glPushMatrix()  # Save the current matrix state
    glColor3f(0, 0, 1)
    glTranslatef(10, 0, 0)  
    gluCylinder(gluNewQuadric(), 5, 10, 30, 10, 10) 
    glPopMatrix()
    
    
    
    
    
    glPushMatrix()
    glTranslatef( - 10, 0, 0)  
    gluCylinder(gluNewQuadric(), 5, 10, 30, 10, 10) 
    glPopMatrix()
    
    
        
    #Hands
    glPushMatrix()  # Save the current matrix state
    glColor3f(247/255, 230/255, 190/255)

    
    glTranslatef(18, -10, 65) 
    glRotatef(90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 10, 5, 20, 10, 10) 
    glPopMatrix()
    
    
    
    
    glPushMatrix()  # Save the current matrix state
    glColor3f(247/255, 230/255, 190/255)
  
    
    glTranslatef(-18, -10, 65) 
    glRotatef(90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 10, 5, 20, 10, 10) 
    glPopMatrix()
        
    
    
    #gun
    glPushMatrix()  # Save the current matrix state
    glColor3f(191/255, 191/255, 191/255)

    
    glTranslatef(0, -10,  65) 
    glRotatef(90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 10, 5, 35, 10, 10) 
    glPopMatrix()
        
    
    
    
    #head
    glPushMatrix()
    glColor3f(0, 0, 0)

    glTranslatef(0, 0, 85)
    gluSphere(gluNewQuadric(), 10, 10, 10)
    glPopMatrix()
    
    

    glPopMatrix()







def keyboardListener(key, x, y):
    global first_person_mode, enemy_speed, cheat_bullets, score, timer, enemies_list, fovY, bullet_speed, bullet_list, missed,player_life,player_pos, player_rotation_angle, game_over, cheat_mode, camera_follow_gun, cheat_shoot_timer, camera_pos
    x, y, z = player_pos
    speed = 20
    x_new, y_new = x, y
    angle_rad = math.radians(player_rotation_angle)

    # Move forward (W key)
    if key == b'w' and game_over == False:
        
        x_new += speed * math.sin(angle_rad)  
        y_new -= speed * math.cos(angle_rad)  
        

    # Move backward (S key)
    if key == b's'  and game_over == False:

        x_new -= speed * math.sin(angle_rad)
        y_new += speed * math.cos(angle_rad)
        

    # Rotate left (A key)
    if key == b'a'  and game_over == False:
        player_rotation_angle += 10



    # Rotate right (D key)
    if key == b'd'  and game_over == False:
        player_rotation_angle -= 10
  
    x_new = max(-600, min(600, x_new))
    y_new = max(-600, min(600, y_new))
        
    player_pos = [x_new, y_new, z]
    # # Toggle cheat mode (C key)
    if key == b'c' and game_over == False:
        cheat_mode = not cheat_mode
        if not cheat_mode:  
            camera_follow_gun = False
    
    if key == b'v' and game_over == False and first_person_mode and cheat_mode:
        camera_follow_gun = not camera_follow_gun    

    # # Reset the game if R key is pressed
    if key == b'r' and game_over == True:
        cheat_shoot_timer = 0
        theta = math.pi/2
        r = 400
        camera_z = 500
        camera_pos = (r* math.cos(theta), r * math.sin(theta), camera_z)
        player_rotation_angle = 0
        player_life = 5
        missed = 0
        player_pos = [0 , 0 , 0]

        bullet_list = []
        bullet_speed = 600
        fovY = 120  

        enemies_list = []
        for i in range(5):
            x = random.uniform(-590,590)
            y = random.uniform(-590,590)
            z = 50
            enemies_list.append([x,y,z])
        timer = 0.0
        score = 0
        cheat_mode = False
        camera_follow_gun = False
        cheat_bullets = []
        
        enemy_speed = 30

        game_over = False

        first_person_mode = False      
        


def specialKeyListener(key, x, y):
    global theta,r,z, camera_pos, last_frame

    

    x, y, z = camera_pos

    if not first_person_mode and game_over == False :    # Move camera up (UP arrow key)
        if key == GLUT_KEY_UP and z < 1000:
            z += 10

        # # Move camera down (DOWN arrow key)
        if key == GLUT_KEY_DOWN and z > 10:
            z-= 10

        # moving camera left (LEFT arrow key)
        if key == GLUT_KEY_LEFT:
            theta -= 0.05 # Small angle decrement for smooth movement

        # moving camera right (RIGHT arrow key)
        if key == GLUT_KEY_RIGHT:
            theta += 0.05  # Small angle increment for smooth movement

        camera_pos = (r* math.cos(theta), r * math.sin(theta), z)



        
def mouseListener(button, state, x, y):
    global first_person_mode, camera_pos, player_pos, player_rotation_angle, bullet_list, game_over
    """
    Handles mouse inputs for firing bullets (left click) and toggling camera mode (right click).
    """
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and game_over == False:
        x, y, z = player_pos

        bullet_x = x - 46.1538462 + 0 * math.cos(math.radians(player_rotation_angle)) - (-60) * math.sin(math.radians(player_rotation_angle))
        bullet_y = y + 46.1538462  + 0 * math.sin(math.radians(player_rotation_angle)) + (-60) * math.cos(math.radians(player_rotation_angle))
        bullet_z = z + 65

        # Bullet direction (same as player's facing direction)
        x_dir = math.sin(math.radians(player_rotation_angle))
        y_dir = -math.cos(math.radians(player_rotation_angle))

        # Add bullet to the list
        bullet_list.append([bullet_x, bullet_y, bullet_z, x_dir, y_dir])
        print("Player Bullet Fired!")

    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN and game_over == False:
        first_person_mode = not first_person_mode

def setupCamera():
    global camera_pos,player_pos, first_person_mode, player_rotation_angle,camera_follow_gun
    """
    Configures the camera's projection and view settings.
    Uses a perspective projection and positions the camera to look at the target.
    """
    glMatrixMode(GL_PROJECTION)  # Switch to projection matrix mode
    glLoadIdentity()  # Reset the projection matrix
    # Set up a perspective projection (field of view, aspect ratio, near clip, far clip)
    gluPerspective(120, 1.25, 1, 1500) # Think why aspect ration is 1.25?
    glMatrixMode(GL_MODELVIEW)  # Switch to model-view matrix mode
    glLoadIdentity()  # Reset the model-view matrix

    if not first_person_mode:
        # Extract camera position and look-at target
        x, y, z = camera_pos
        gluLookAt(x, y, z,  # Camera position
                0, 0, 0,  # Look-at target
                0, 0, 1)
        # Position the camera and set its orientation
    else:
        
        x, y, z = player_pos
        x = x- 46.1538462 #Since there is always an offset (to centralize the player)
        y = y + 46.1538462
        # Compute forward direction based on player_rotation_angle
        
        if cheat_mode and not camera_follow_gun:
            # In cheat mode without camera follow: Camera is stationary, looking at a fixed point
            gluLookAt(x, y - 5, z + 100,  # Camera position (player's head height)
                      0, 0, z + 100,  # Look at a fixed point (e.g., origin or a point in front)
                      0, 0, 1)  # Up vector
        
        else:
            theta = math.radians(player_rotation_angle)
            forward_x = math.sin(theta)  # x-component of forward direction
            forward_y = -math.cos(theta)  # y-component of forward direction
            distance = 50  # Distance to look-at point

            gluLookAt(x, y-5, z+100,  # Camera position (head height, slightly behind)
                    x + forward_x * distance, y + forward_y * distance, z+100,  # Look-at target
                    0, 0, 1)  # Up vector (z-axis)
        


def idle():
    global last_frame, cheat_bullets, cheat_shoot_timer,player_rotation_angle,game_over, player_life, timer, enemies_list, bullet_speed, missed, bullet_list, player_pos, enemy_speed, bullet_hit,score
    delta_time = time.time() - last_frame
    last_frame = time.time()
    # Ensure the screen updates with the latest changes
    if not game_over:
        cheat_shoot_timer += 5.4 * delta_time
        if cheat_mode:  # Rotate player continuously in cheat mode
            player_rotation_angle += 180 * delta_time
            if cheat_shoot_timer >= 0.5:
                cheat_shoot_timer = 0.0
                px, py, pz = player_pos
                gun_x =  px - 46.1538462 + 0 * math.cos(math.radians(player_rotation_angle)) - (-60) * math.sin(math.radians(player_rotation_angle))
                gun_y = py + 46.1538462  + 0 * math.sin(math.radians(player_rotation_angle)) + (-60) * math.cos(math.radians(player_rotation_angle))
                gun_z = pz + 65
                facing_x = math.sin(math.radians(player_rotation_angle))
                facing_y = -math.cos(math.radians(player_rotation_angle))
                temp_enemies_list = enemies_list[:]
                for enemy in temp_enemies_list[:]:
                    ex, ey, ez = enemy
                    # Vector from gun to enemy
                    to_enemy_x = ex - gun_x
                    to_enemy_y = ey - gun_y
                    # Normalize the vector
                    distance = math.sqrt(to_enemy_x**2 + to_enemy_y**2)
                    if distance == 0:
                        continue
                    to_enemy_x /= distance
                    to_enemy_y /= distance
                    # Dot product to find angle
                    dot = facing_x * to_enemy_x + facing_y * to_enemy_y
                    angle = math.acos(max(-1.0, min(1.0, dot))) * 180 / math.pi
                    if angle <= 10:  # Within ±10 degrees
                        bullet_x = gun_x
                        bullet_y = gun_y
                        bullet_z = gun_z
                        dir_x = to_enemy_x
                        dir_y = to_enemy_y
                        bullet_list.append([bullet_x, bullet_y, bullet_z, dir_x, dir_y])

                        break  # Hit only one enemy per shot
        enemy_hitbox = 50
        player_hitbox = 20
        timer +=  1.2 * delta_time
        GRID_LIMIT = 600
        new_bullet_list = []
        temp_enemies_list1 = enemies_list[:] 
        for bullet in bullet_list:
            x, y, z, dir_x, dir_y = bullet
            if [x, y, z] in cheat_bullets:
                cheat_bullets.remove([x, y, z])
            x += dir_x * bullet_speed * delta_time
            y += dir_y * bullet_speed * delta_time
            bullet_hit = False
            for enemy in temp_enemies_list1[:]:  # Iterate over copy to allow safe removal
                enemy_x, enemy_y, enemy_z = enemy
                distance = math.sqrt((x - enemy_x)**2 + (y - enemy_y)**2)
                if distance <= enemy_hitbox:
                    score+=1
                    # Bullet hits enemy: remove both and spawn new enemy
                    temp_enemies_list1.remove(enemy)
                    bullet_hit = True
                    # Spawn new enemy at random position
                    new_x = random.uniform(-590, 590)
                    new_y = random.uniform(-590, 590)
                    temp_enemies_list1.append([new_x, new_y, 50])
                    break  # Stop checking this bullet against other enemies
            # Add bullet to new list if it didn't hit an enemy and is within grid
            if not bullet_hit and -GRID_LIMIT <= x <= GRID_LIMIT and -GRID_LIMIT <= y <= GRID_LIMIT:
                new_bullet_list.append([x, y, z, dir_x, dir_y])
            elif not bullet_hit:
                missed += 1
                print( f"Bullet Missed: {missed}")
        bullet_list = new_bullet_list
        enemies_list = temp_enemies_list1
        player_x, player_y, _ = player_pos
        new_enemies_list = []
        for enemy in enemies_list:
            enemy_x, enemy_y, enemy_z = enemy
            # Calculate distance to player
            distance = math.sqrt((player_x - enemy_x)**2 + (player_y - enemy_y)**2)
            # Check for collision
            if distance > player_hitbox:
                # Move enemy towards player if no collision
                dx = player_x - enemy_x
                dy = player_y - enemy_y
                if distance > 5:  # Avoid division by zero
                    dir_x = dx / distance
                    dir_y = dy / distance
                    enemy_x += dir_x * enemy_speed * delta_time
                    enemy_y += dir_y * enemy_speed * delta_time
                    enemy_x = max(-GRID_LIMIT, min(GRID_LIMIT, enemy_x))
                    enemy_y = max(-GRID_LIMIT, min(GRID_LIMIT, enemy_y))
                    new_enemies_list.append([enemy_x, enemy_y, enemy_z])
                    
            else:
                # Enemy touches player: remove enemy and spawn a new one
                new_x = random.uniform(-590, 590)
                new_y = random.uniform(-590, 590)
                new_enemies_list.append([new_x, new_y, 50])
                player_life -= 1
                print( f"Remaining Player Life: {player_life}")
            # If distance <= COLLISION_RADIUS, enemy vanishes (not added to new_enemies_list)
        enemies_list = new_enemies_list

    glutPostRedisplay()
 

def showScreen():
    global missed, game_over, enemies_list, player_life, score
    """
    Display function to render the game scene:
    - Clears the screen and sets up the camera.
    - Draws everything of the screen
    """
    # Clear color and depth buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()  # Reset modelview matrix
    glViewport(0, 0, 1000, 800)  # Set viewport size

    setupCamera()  # Configure camera perspective

    # Draw a random points
 

    
    draw_grid()

    # Display game info text at a fixed screen position
    draw_text(10, 770, f"Player Life Remaining: {player_life}")
    draw_text(10, 740, f"Game Score: {score}")
    draw_text(10, 710, f"Player Bullet Missed: {missed}")
    

    
    
    draw_player()
    if game_over == False:
        for i in bullet_list:
            draw_bullets(i[0],i[1], i[2], i[3], i[4])

    
        for enemy in enemies_list:
            draw_enemies(enemy[0], enemy[1], enemy[2])   
    

    # Swap buffers for smooth rendering (double buffering)
    glutSwapBuffers()


# Main function to set up OpenGL window and loop
def main():
    glutInit()
    print( f"Remaining Player Life: {player_life}")
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # Double buffering, RGB color, depth test
    glutInitWindowSize(1000, 800)  # Window size
    glutInitWindowPosition(0, 0)  # Window position
    wind = glutCreateWindow(b"FPS Shooter Game")  # Create the window

    glutDisplayFunc(showScreen)  # Register display function
    glutKeyboardFunc(keyboardListener)  # Register keyboard listener
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)  # Register the idle function to move the bullet automatically

    glutMainLoop()  # Enter the GLUT main loop

if __name__ == "__main__":
    main()
