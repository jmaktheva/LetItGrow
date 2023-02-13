import board
import terminalio
import displayio
import busio
from adafruit_display_text import label
import adafruit_ili9341
import adafruit_imageload

def startup():
    #returns:   display - store this in variable of same name, pass into new functions

    displayio.release_displays() #release display resources
    #spi = busio.SPI() #ESP32 doesn't have an SPI() on busio for some reason
    #spi = busio.SPI(clock=board.IO12, MOSI=board.IO11, MISO=board.IO13)
    spi = busio.SPI(clock=board.IO12, MOSI=board.IO11) #don't change pins
    tft_cs = board.IO10 #can change pins
    tft_dc = board.IO46 #can change pins
    display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=board.IO14)
    display = adafruit_ili9341.ILI9341(display_bus, width=320, height=240)
    
    return display

def splash(display):
    #parameters:    display - pass in display object from startup()
    #               color_hex - hex color code. format 0x######
    #returns:       splash - store this in variable of same name, pass into new functions
    
    splash = displayio.Group()
    display.show(splash)
    
    return splash

def draw_background(splash, color_hex):
    #parameters:    splash - pass in splash object from other functions
    #               color_hex - hex color code. format '0x######'
    #returns:       splash - store this in variable of same name, pass into new functions
    
    color_bitmap = displayio.Bitmap(320, 240, 1)
    color_palette = displayio.Palette(1)
    #color_palette[0] = 0x00FF00  # Bright Green
    color_palette[0] = color_hex
    bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
    splash.append(bg_sprite)
    return splash

def draw_text(splash, text, scale, x, y, color_hex):
    #parameters:    splash - pass in splash object from other functions
    #               text - string of what you want displayed
    #               scale - scale of text. try 2 or 3
    #               x - x coordinate of text to be displayed, from 0 to 320
    #               y - y coordinate of text to be displayed, from 0 to 240
    #               color_hex - hex color code. format 0x######
    #returns:       splash - store this in variable of same name, pass into new functions
    
    #text_group = displayio.Group(scale=3, x=60, y=60)
    text_group = displayio.Group(scale=scale, x=x, y=y)
    #text = "Let It Grow"
    #text_area = label.Label(terminalio.FONT, text=text, color=0xD80621)
    text_area = label.Label(terminalio.FONT, text=text, color=color_hex)
    text_group.append(text_area)  # Subgroup for text scaling
    splash.append(text_group)
    
    return splash

#TODO: load other file types? memory error
def draw_image(splash, filepath, width, height, x, y):
    #parameters:    splash - pass in splash object from other functions
    #               filepath - string for path to file. ex: '/purple.bmp'
    #               width - width of picture
    #               height - height of picture
    #               x - x coordinate of picture to be displayed, from 0 to 320
    #               y - y coordinate of picture to be displayed, from 0 to 240
    #returns:       splash - store this in variable of same name, pass into new functions
    bitmap, palette = adafruit_imageload.load(filepath, bitmap=displayio.Bitmap, palette=displayio.Palette)
    bmp = displayio.TileGrid(bitmap, pixel_shader=palette, width=1, height=1, tile_width=width, tile_height=height, default_tile=0)
    splash.append(bmp)
    bmp.x = x
    bmp.y = y
    
    return splash