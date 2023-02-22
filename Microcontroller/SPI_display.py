import board
import terminalio
import displayio
import busio
from adafruit_display_text import label
import adafruit_ili9341
import adafruit_imageload
from adafruit_display_shapes import circle
import adafruit_focaltouch

#TODO: display.show() deprecated

displayio.release_displays() #release display resources
spi = busio.SPI(clock=board.IO12, MOSI=board.IO11) #don't change pins for now
tft_cs = board.IO10 #can change pin
tft_dc = board.IO9 #can change pin
tft_reset = board.IO46 #can change pin
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_reset)
display = adafruit_ili9341.ILI9341(display_bus, width=320, height=240)
splash = displayio.Group() #create group
display.show(splash) #show display
i2c = busio.I2C(sda=board.IO4, scl=board.IO5)
ft = adafruit_focaltouch.Adafruit_FocalTouch(i2c, debug=False)

def draw_background(color_hex):
    #parameters:    splash - pass in splash object from other functions
    #               color_hex - hex color code. format '0x######'
    #returns:       splash - store this in variable of same name, pass into new functions
    
    color_bitmap = displayio.Bitmap(320, 240, 1)
    color_palette = displayio.Palette(1)
    #color_palette[0] = 0x00FF00  # Bright Green
    color_palette[0] = color_hex
    bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
    splash.append(bg_sprite)
    
    return

def draw_text(text, scale, x, y, color_hex):
    #parameters:    splash - pass in splash object from other functions
    #               text - string of what you want displayed
    #               scale - scale of text. try 2 or 3
    #               x - x coordinate of text to be displayed, from 0 to 320
    #               y - y coordinate of text to be displayed, from 0 to 240
    #               color_hex - hex color code. format 0x######
    #returns:       splash - store this in variable of same name, pass into new functions
    
    text_group = displayio.Group(scale=scale, x=x, y=y)
    text_area = label.Label(terminalio.FONT, text=text, color=color_hex)
    text_group.append(text_area)  # Subgroup for text scaling
    splash.append(text_group)
    
    return

def draw_image(filepath, x, y):
    #parameters:    splash - pass in splash object from other functions
    #               filepath - string for path to file, currently bmp or png. ex: '/purple.bmp'. files are particular - ask Logan for help
    #               x - x coordinate of picture to be displayed, from 0 to 320
    #               y - y coordinate of picture to be displayed, from 0 to 240
    #returns:       splash - store this in variable of same name, pass into new functions
    
    image, palette = adafruit_imageload.load(filepath)
    palette.make_transparent(0)
    tile_grid = displayio.TileGrid(image, pixel_shader=palette)
    tile_grid.x = x
    tile_grid.y = y
    splash.append(tile_grid)
    
    return

def draw_bitmap(filepath, x, y):
    #parameters:    splash - pass in splash object from other functions
    #               filepath - string for path to file. ex: '/purple.bmp'. files are particular - ask Logan for help
    #               x - x coordinate of picture to be displayed, from 0 to 320
    #               y - y coordinate of picture to be displayed, from 0 to 240
    #returns:       splash - store this in variable of same name, pass into new functions
    
    bitmap = displayio.OnDiskBitmap(filepath)
    bmp = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)
    bmp.x = x
    bmp.y = y
    splash.append(bmp)
    
    return

def draw_circle(x, y, r, color_hex):
    #parameters:    splash - pass in splash object from other functions
    #               x - x coordinate of text to be displayed, from 0 to 320
    #               y - y coordinate of text to be displayed, from 0 to 240
    #               r - radius of circle
    #               color_hex - hex color code. format 0x######
    #returns:       splash - store this in variable of same name, pass into new functions
    
    circ = circle.Circle(x0=x, y0=y, r=r, fill=color_hex)
    splash.append(circ)
    
    return

#fix later
def remove_text():
    splash.pop(-1)

def touch_input():
    if ft.touched: #1 if touched, 0 otherwise
        return ft.touches[0]