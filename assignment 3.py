from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

# Camera-related variables
theta = math.pi/2
r = 400
z = 500
camera_pos = (r* math.cos(theta), r * math.sin(theta), z)


player_pos = (0 - 46.1538462, 0 + 46.1538462, 0)
fovY = 120  # Field of view
# GRID_LENGTH = 600  # Length of grid lines
rand_var = 423



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
    glVertex3f(-initial_x,initial_y - (13*length), 60)
    glVertex3f(-initial_x, initial_y, 60)        
    
    glColor3f(0, 0, 1)
    glVertex3f(initial_x, initial_y, 0)
    glVertex3f(initial_x, initial_y - (13 * length), 0)
    glVertex3f(initial_x,initial_y - (13*length), 60)
    glVertex3f(initial_x, initial_y, 60)    

    
    glColor3f(67/255, 234/255, 240/255)
    glVertex3f(-initial_x, initial_y - (13 * length), 0)
    glVertex3f(-initial_x + (13 * length), initial_y - (13 * length)  , 0)
    glVertex3f(-initial_x + (13 * length),initial_y - (13 * length), 60)
    glVertex3f(-initial_x, initial_y - (13 * length), 60) 
    
    glColor3f(1,1,1)
    glVertex3f(-initial_x, initial_y , 0)
    glVertex3f(-initial_x + (13 * length), initial_y   , 0)
    glVertex3f(-initial_x + (13 * length),initial_y , 60)
    glVertex3f(-initial_x, initial_y , 60)       
    glEnd()
    












def draw_shapes():
    global player_pos
    x,y,z = player_pos
    
    #body
    glPushMatrix()
    glColor3f(50/255, 168/255, 82/255)
    glTranslatef(x, y, z+50)
    glScale(0.7,0.4, 1)
    glutSolidCube(50)
    glPopMatrix()
    

   
    #legs
    glPushMatrix()  # Save the current matrix state
    glColor3f(0, 0, 1)
    glTranslatef(x+10, y, z)  
    gluCylinder(gluNewQuadric(), 5, 10, 30, 10, 10) 
    glPopMatrix()
    
    
    glPushMatrix()
    glTranslatef(x - 10, y, z)  
    gluCylinder(gluNewQuadric(), 5, 10, 30, 10, 10) 
    glPopMatrix()
    
    
        
    #Hands
    glPushMatrix()  # Save the current matrix state
    glColor3f(247/255, 230/255, 190/255)
    glTranslatef(x+18, y-10, z + 65) 
    glRotatef(90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 10, 5, 30, 10, 10) 
    glPopMatrix()
    
    glPushMatrix()  # Save the current matrix state
    glColor3f(247/255, 230/255, 190/255)
    glTranslatef(x-18, y-10, z + 65) 
    glRotatef(90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 10, 5, 30, 10, 10) 
    glPopMatrix()
        
    
    
    
    
    
    #head
    glPushMatrix()
    glColor3f(0, 0, 0)
    glTranslatef(x, y, z+85)
    gluSphere(gluNewQuadric(), 10, 10, 10)
    glPopMatrix()
    
    
    
    
    
    
    # glColor3f(1, 1, 0)
    # gluCylinder(gluNewQuadric(), 40, 5, 150, 10, 10)  # parameters are: quadric, base radius, top radius, height, slices, stacks
    # glTranslatef(100, 0, 100) 
    # glRotatef(90, 0, 1, 0)  # parameters are: angle, x, y, z
    # gluCylinder(gluNewQuadric(), 40, 5, 150, 10, 10)

    # glColor3f(0, 1, 1)
    # glTranslatef(300, 0, 100) 
    # gluSphere(gluNewQuadric(), 80, 10, 10)  # parameters are: quadric, radius, slices, stacks

      # Restore the previous matrix state


def keyboardListener(key, x, y):
    """
    Handles keyboard inputs for player movement, gun rotation, camera updates, and cheat mode toggles.
    """
    # # Move forward (W key)
    # if key == b'w':  

    # # Move backward (S key)
    # if key == b's':

    # # Rotate gun left (A key)
    # if key == b'a':

    # # Rotate gun right (D key)
    # if key == b'd':

    # # Toggle cheat mode (C key)
    # if key == b'c':

    # # Toggle cheat vision (V key)
    # if key == b'v':

    # # Reset the game if R key is pressed
    # if key == b'r':


def specialKeyListener(key, x, y):
    global theta,r,z, camera_pos

    

    x, y, z = camera_pos
    
    # Move camera up (UP arrow key)
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


def mouseListener(button, state, x, y):
    global first_person_mode
    """
    Handles mouse inputs for firing bullets (left click) and toggling camera mode (right click).
    """
        # # Left mouse button fires a bullet
        # if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:

        # # Right mouse button toggles camera tracking mode
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        first_person_mode = not first_person_mode


def setupCamera():
    global camera_pos
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

    
    # Extract camera position and look-at target
    x, y, z = camera_pos
    # Position the camera and set its orientation
    gluLookAt(x, y, z,  # Camera position
              0, 0, 0,  # Look-at target
              0, 0, 1)  # Up vector (z-axis)


def idle():
    """
    Idle function that runs continuously:
    - Triggers screen redraw for real-time updates.
    """
    # Ensure the screen updates with the latest changes
    glutPostRedisplay()


def showScreen():
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
    # # Draw the grid (game floor)
    # glBegin(GL_QUADS)
    
    # glColor3f(1, 1, 1)
    # glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    # glVertex3f(0, GRID_LENGTH, 0)
    # glVertex3f(0, 0, 0)
    # glVertex3f(-GRID_LENGTH, 0, 0)

    # # glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    # # glVertex3f(0, -GRID_LENGTH, 0)
    # # glVertex3f(0, 0, 0)
    # # glVertex3f(GRID_LENGTH, 0, 0)


    # glColor3f(0.7, 0.5, 0.95)
    # # glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    # # glVertex3f(-GRID_LENGTH, 0, 0)
    # # glVertex3f(0, 0, 0)
    # # glVertex3f(0, -GRID_LENGTH, 0)

    # glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    # glVertex3f(GRID_LENGTH, 0, 0)
    # glVertex3f(0, 0, 0)
    # glVertex3f(0, GRID_LENGTH, 0)
    # glEnd()

    # Display game info text at a fixed screen position
    draw_text(10, 770, f"A Random Fixed Position Text")
    draw_text(10, 740, f"See how the position and variable change?: {rand_var}")

    draw_shapes()

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