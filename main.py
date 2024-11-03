import pygame
import sys
import os
os.system('clear')
os.environ['SDL_VIDEO_WINDOW_POS'] = str(1240) + "," + str(0)
pygame.init()
backgroundColor = [5,5,5]

#define window specifications
WIDTH = 900
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
canvas = pygame.Surface((WIDTH-(128+6+64), HEIGHT))
pygame.display.set_caption('Draw!')
font = pygame.font.SysFont("monospace", 32)
clock = pygame.time.Clock()
FPS = 60
pygame.font.init()

icon_paths = ['icons/pen.png', 'icons/eraser.png']
icons = []
icon_buttons = []
SAVE_NAME = 'canvas.png'

#store brushes and input states
brushSize = 25
eraserMode = False
penDown = False
mouseDown = False
shiftDown = False
brushColor = [255,255,255]


sliders = []
slider_buttons = []
class slider():
    def __init__(self, name, x,y, value, length, isHeld, low, high):
        self.name = name
        self.x = x
        self.y = y
        self.value = value
        self.length = length
        self.isHeld = isHeld
        self.low = low
        self.high = high
        sliders.append(self)

#initialize sliders
brushSlider = slider('Brush Width', 128+32, 16, 0, 128, False, 1, 100)
redSlider = slider('Red', 32+6, HEIGHT - 158, 0, 128, False, 0, 255)
greenSlider = slider('Green', (128+64)/2, HEIGHT - 158, 0, 128, False, 0, 255)
blueSlider = slider('Blue', 128+64-32-6, HEIGHT - 158, 0, 128, False, 0, 255)

for slider in sliders:
    slider_buttons.append(pygame.Rect(slider.x-8, slider.y-8, 16, 16))

#returns the normalized value from a slider
def normalize(slider):
    return slider.value * (slider.high - slider.low) + slider.low

def initIcons(): #initialize icons and icon buttons
    global icons, icon_buttons
    for path in icon_paths:
        img = pygame.image.load(path)
        img = pygame.transform.scale(img, [32,32])
        icons.append(img)

        icon_wrap = 3
        col = 0
        row = 0
        for icon in icons:
            icon_buttons.append(pygame.Rect(16 + (col*48), 16 + (row * 48), 32, 32))
            col+=1
            if(col>=icon_wrap):
                col = 0
                row += 1
    
        
def drawSideBar(): #draws the sidebar and updates sliders
    global brushSize
    sidebar_bg = pygame.Rect(0,0,128+64, HEIGHT)
    pygame.draw.rect(screen, [35,35,35], sidebar_bg)

    divider = pygame.Rect(128+64, 0, 6, HEIGHT)
    pygame.draw.rect(screen, [75,75,75], divider)

    #draw icons
    icon_wrap = 3
    col = 0
    row = 0
    for icon in icons:
        screen.blit(icon, (16 + (col*48), 16 + (row * 48)))
        col+=1
        if(col>=icon_wrap):
            col = 0
            row += 1

    drawColorPanel()

    #update sliders
    mouse_pos = pygame.mouse.get_pos()
    for button in slider_buttons:
        index = slider_buttons.index(button)
        if button.collidepoint(mouse_pos) and mouseDown:
            sliders[index].isHeld = True

    #draw sliders
    for slider in sliders:
        pygame.draw.line(screen, [75,75,75], (slider.x, slider.y), (slider.x, slider.y+slider.length), 6)
        pygame.draw.circle(screen, [100,100,100], (slider.x+1, slider.y + (slider.value*slider.length)), 8)

        if not mouseDown:
            slider.isHeld = False
        if slider.isHeld:
            slider.value = min(max((mouse_pos[1] - slider.y)/slider.length, 0), 1)
            button = slider_buttons[sliders.index(slider)]
            button.y = (slider.value*slider.length)+slider.y-8

    #update slider values
    brushSize = round(normalize(brushSlider))
    brushColor[0] = round((1-redSlider.value) * (redSlider.high - redSlider.low))
    brushColor[1] = round((1-greenSlider.value) * (greenSlider.high - greenSlider.low))
    brushColor[2] = round((1-blueSlider.value) * (blueSlider.high - blueSlider.low))

last_pos = pygame.mouse.get_pos()
def drawBrush():
    global last_pos, penDown
    mouse_pos = pygame.mouse.get_pos()
    adj_pos = [mouse_pos[0]-128-64, mouse_pos[1]]
    adj_last_pos = [last_pos[0]-128-64, last_pos[1]]

    if mouse_pos[0] <= (128+64): #if mouse is beyond the canvas, disable the pen
        penDown = False
        
    if penDown and not eraserMode: #pen
        pygame.draw.circle(screen, brushColor, mouse_pos, (brushSize/2)-2)
        pygame.draw.circle(canvas, brushColor, adj_pos, (brushSize/2)-2)
        
        pygame.draw.line(screen, brushColor, last_pos, mouse_pos, brushSize)
        pygame.draw.line(canvas, brushColor, adj_last_pos, adj_pos, brushSize)
        
    if penDown and eraserMode: #eraser
        pygame.draw.circle(screen, backgroundColor, mouse_pos, (brushSize/2)-2)
        pygame.draw.circle(canvas, backgroundColor, adj_pos, (brushSize/2)-2)
        
        pygame.draw.line(screen, backgroundColor, last_pos, mouse_pos, brushSize)
        pygame.draw.line(canvas, backgroundColor, adj_last_pos, adj_pos, brushSize)
        
    last_pos = pygame.mouse.get_pos()

def drawColorPanel():
    color_panel_bg = pygame.Rect(0, HEIGHT-(128+64), 128+64+6, 128+64)
    pygame.draw.rect(screen, brushColor, color_panel_bg)
    pygame.draw.rect(screen, [75,75,75], color_panel_bg, 6)

initIcons()
screen.fill(backgroundColor)
canvas.fill(backgroundColor)
run = True
while run:
    drawBrush()
    drawSideBar()
    pygame.display.flip()
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            penDown = True
            mouseDown = True
            mouse_pos = pygame.mouse.get_pos()
            for button in icon_buttons[::2]:
                if button.collidepoint(mouse_pos): #if icon clicked:
                    if icon_buttons.index(button) == 0:
                        eraserMode = False
                    if icon_buttons.index(button) == 2:
                        eraserMode = True
                        
        if event.type == pygame.MOUSEBUTTONUP:
            penDown = False
            mouseDown = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                pygame.image.save(canvas, SAVE_NAME)
                
            if event.key == pygame.K_p:
                print(clock.get_fps())
                
            if event.key == pygame.K_r: #reset canvas
                screen.fill(backgroundColor)
                canvas.fill(backgroundColor)

            if event.key == pygame.K_n: #name piece
                SAVE_NAME = input('Save as: ')
                SAVE_NAME += '.png'
                pygame.image.save(canvas, SAVE_NAME)
                print(f'Saved as \'{SAVE_NAME}\'')
