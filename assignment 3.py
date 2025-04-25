from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

# Camera-related variables
theta = math.pi/2
r = 400
camera_z = 500
camera_pos = (r* math.cos(theta), r * math.sin(theta), camera_z)
player_rotation_angle = 0

score = 10
player_pos = [0 , 0 , 0]

bullet_list = []
bullet_speed = 10
fovY = 120  # Field of view
# GRID_LENGTH = 600  # Length of grid lines
rand_var = 423

fire = False

first_person_mode = False
def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1,1,1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    
    # Set up an orthographic projection that matches window coordinates
    gluOrtho2D(0, 1000, 0, 800)  # left, right, bottom, top

    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # Draw text at (x, y) in screen coordinates
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    
    # Restore original projection and modelview matrices
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
        for i in range(13):
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

    
    glutSolidCube(5)

    glPopMatrix()
    
    
    
    
    


def draw_player():
    global player_pos, player_rotation_angle
    x,y,z = player_pos
    
    glPushMatrix()
    glTranslatef(x, y, z)

    glTranslatef(- 46.1538462,46.1538462, 0)
    glRotatef(player_rotation_angle, 0, 0, 1)
    
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
    global player_pos, player_rotation_angle
    x, y, z = player_pos
    speed = 15 
    x_new, y_new = x, y
    angle_rad = math.radians(player_rotation_angle)

    # Move forward (W key)
    if key == b'w':
        
        x_new += speed * math.sin(angle_rad)  
        y_new -= speed * math.cos(angle_rad)  
        

    # Move backward (S key)
    if key == b's':

        x_new -= speed * math.sin(angle_rad)
        y_new += speed * math.cos(angle_rad)
        

    # Rotate left (A key)
    if key == b'a':
        player_rotation_angle += 5



    # Rotate right (D key)
    if key == b'd':
        player_rotation_angle -= 5
  
    x_new = max(-600, min(600, x_new))
    y_new = max(-600, min(600, y_new))
        
    player_pos = [x_new, y_new, z]
    # # Toggle cheat mode (C key)
    # if key == b'c':

    # # Toggle cheat vision (V key)
    # if key == b'v':

    # # Reset the game if R key is pressed
    # if key == b'r':


def specialKeyListener(key, x, y):
    global theta,r,z, camera_pos

    

    x, y, z = camera_pos
    
    if not first_person_mode :    # Move camera up (UP arrow key)
        if key == GLUT_KEY_UP and z < 1000:
            z += 10

        # # Move camera down (DOWN arrow key)
        if key == GLUT_KEY_DOWN and z > 10:
            z-=10

        # moving camera left (LEFT arrow key)
        if key == GLUT_KEY_LEFT:
            theta += 0.05  # Small angle decrement for smooth movement

        # moving camera right (RIGHT arrow key)
        if key == GLUT_KEY_RIGHT:
            theta -= 0.05  # Small angle increment for smooth movement

        camera_pos = (r* math.cos(theta), r * math.sin(theta), z)


# def mouseListener(button, state, x, y):
#     global first_person_mode, camera_pos, player_pos, fire, player_rotation_angle, bullet_list
#     """
#     Handles mouse inputs for firing bullets (left click) and toggling camera mode (right click).
#     """
#         # # Left mouse button fires a bullet
  
#     if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        
#         x,y, z = player_pos
#         bullet_x = x - 46.1538462 + math.sin(math.radians(player_rotation_angle)) * (-45)
#         bullet_y = y + 46.1538462 + math.cos(math.radians(player_rotation_angle)) * (-45)
#         bullet_z = z + 65
#         x_dir = math.sin(math.radians(player_rotation_angle))
#         y_dir = -math.cos(math.radians(player_rotation_angle))
#         bullet_list.append([bullet_x,bullet_y,bullet_z, x_dir, y_dir])
        

#         # # Right mouse button toggles camera tracking mode
#     if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
#         first_person_mode = not first_person_mode
        
def mouseListener(button, state, x, y):
    global first_person_mode, camera_pos, player_pos, fire, player_rotation_angle, bullet_list
    """
    Handles mouse inputs for firing bullets (left click) and toggling camera mode (right click).
    """
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        x, y, z = player_pos
        # Convert player rotation angle to radians


        # Account for the player's model offset (same as in draw_player)
   

        # Base position of the player after offset
        x = x  -46.1538462
        y = y + 46.1538462 

        # Gun position relative to the player (from draw_player: glTranslatef(0, -10, 65))


        # Rotate the gun offset according to player_rotation_angle
        # The gun's position in the player's local coordinate system after rotation
        rotated_gun_x = 0 * math.cos(math.radians(player_rotation_angle)) - (-60) * math.sin(math.radians(player_rotation_angle))
        rotated_gun_y = 0 * math.sin(math.radians(player_rotation_angle)) + (-60) * math.cos(math.radians(player_rotation_angle))

        # Calculate bullet starting position (from the gun's tip)
        bullet_x = x + rotated_gun_x
        bullet_y = y + rotated_gun_y
        bullet_z = z + 65

        # Bullet direction (same as player's facing direction)
        x_dir = math.sin(math.radians(player_rotation_angle))
        y_dir = -math.cos(math.radians(player_rotation_angle))

        # Add bullet to the list
        bullet_list.append([bullet_x, bullet_y, bullet_z, x_dir, y_dir])

    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        first_person_mode = not first_person_mode

def setupCamera():
    global camera_pos,player_pos, first_person_mode, player_rotation_angle
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
        y = y+46.1538462
        # Compute forward direction based on player_rotation_angle
        theta = math.radians(player_rotation_angle)
        forward_x = math.sin(theta)  # x-component of forward direction
        forward_y = -math.cos(theta)  # y-component of forward direction
        distance = 50  # Distance to look-at point

        gluLookAt(x, y-5, z+100,  # Camera position (head height, slightly behind)
                  x + forward_x * distance, y + forward_y * distance, z+100,  # Look-at target
                  0, 0, 1)  # Up vector (z-axis)
        


def idle():
    global bullet_speed, score, bullet_list
    """
    Idle function that runs continuously:
    - Triggers screen redraw for real-time updates.
    """
    # Ensure the screen updates with the latest changes

        
    GRID_LIMIT = 600
    new_bullet_list = []
    for bullet in bullet_list:
        x, y, z, dir_x, dir_y = bullet
        x += dir_x * bullet_speed
        y += dir_y * bullet_speed
        if -GRID_LIMIT <= x <= GRID_LIMIT and -GRID_LIMIT <= y <= GRID_LIMIT:
            new_bullet_list.append([x, y, z, dir_x, dir_y])
        else:
            score -= 10
            print(f"Score: {score}")
    bullet_list = new_bullet_list
            
    
    
    
    glutPostRedisplay()


def showScreen():
    global fire
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
    draw_text(10, 770, f"A Random Fixed Position Text")
    draw_text(10, 740, f"See how the position and variable change?: {rand_var}")

    
    draw_player()
    
    for i in bullet_list:
        draw_bullets(i[0],i[1], i[2], i[3], i[4])

        
    

    # Swap buffers for smooth rendering (double buffering)
    glutSwapBuffers()


# Main function to set up OpenGL window and loop
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # Double buffering, RGB color, depth test
    glutInitWindowSize(1000, 800)  # Window size
    glutInitWindowPosition(0, 0)  # Window position
    wind = glutCreateWindow(b"3D OpenGL Intro")  # Create the window

    glutDisplayFunc(showScreen)  # Register display function
    glutKeyboardFunc(keyboardListener)  # Register keyboard listener
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)  # Register the idle function to move the bullet automatically

    glutMainLoop()  # Enter the GLUT main loop

if __name__ == "__main__":
    main()