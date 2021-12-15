import pygame as pg
import os

pg.init()
os.putenv('SDL_VIDEODRIVER', 'fbcon') #display on piTFT
os.putenv('SDL_FBDEV', '/dev/fb0') 
os.putenv('SDL_MOUSEDRV', 'TSLIB') #track mouse click on piTFT
os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen') 

pg.mouse.set_visible(True)

def search(second_page,first_page):
    screen = pg.display.set_mode((320,240))
    font = pg.font.Font(None, 32)
    my_font=pg.font.Font(None,15)
    clock = pg.time.Clock()
    input_box = pg.Rect(60, 70, 140, 32)
    color_inactive = pg.Color('lightskyblue3')
    color_active = pg.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    t=""
    done = False

    while not done and second_page:
        for event in pg.event.get():
            if(event.type is pg.MOUSEBUTTONUP):
                pos=pg.mouse.get_pos()
                x,y=pos
                #print(x,y)
                if y>200 and x>270:
                    print("return")
                    second_page=False
                    first_page=True
            #if event.type == pg.QUIT:
                #done = True
            if event.type == pg.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            if event.type == pg.KEYDOWN:
                if active:
                    if event.key == pg.K_RETURN:
                        print(text)
                        t=text
                        done = True
                        #text = ''
                    elif event.key == pg.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill((0, 0, 0))
        # Render the current text.
        txt_surface = font.render(text, True, color)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        # Blit the text.
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        # Blit the input_box rect.
        pg.draw.rect(screen, color, input_box, 2)
        
        s = font.render("search:", True, (255,255,255))
        screen.blit(s, (20,40))
        
        r = my_font.render("return", True, (255,255,255))
        screen.blit(r, (290,225))
        
        pg.display.flip()
        clock.tick(30)
    return t,second_page,first_page


if __name__ == '__main__':
    pg.init()
    search()
    pg.quit()
