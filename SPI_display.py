import board
import terminalio
import displayio
import busio
import pwmio
import adafruit_focaltouch
import adafruit_ili9341
import adafruit_imageload
from adafruit_display_text import label
from adafruit_display_shapes import circle
from adafruit_button import Button
from adafruit_bitmap_font import bitmap_font


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
#i2c = busio.I2C(sda=board.IO4, scl=board.IO5)
#ft = adafruit_focaltouch.Adafruit_FocalTouch(i2c, debug=False)
pwm = pwmio.PWMOut(board.IO3, duty_cycle=2**16 - 1)

#font = bitmap_font.load_font('/fonts/roboto.bdf')

def draw_background(color_hex):
    #parameters:    color_hex - hex color code. format '0x######'

    color_bitmap = displayio.Bitmap(320, 240, 1)
    color_palette = displayio.Palette(1)
    #color_palette[0] = 0x00FF00  # Bright Green
    color_palette[0] = color_hex
    bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
    splash.append(bg_sprite)

    return

def draw_text(text, scale, x, y, color_hex):
    #parameters:    text - string of what you want displayed
    #               scale - scale of text. try 2 or 3
    #               x - x coordinate of text to be displayed, from 0 to 320
    #               y - y coordinate of text to be displayed, from 0 to 240
    #               color_hex - hex color code. format 0x######
    #returns:       (optional) the index at which the group was added

    text_group = displayio.Group(scale=scale, x=x, y=y)
    text_area = label.Label(terminalio.FONT, text=text, color=color_hex)
    text_group.append(text_area)  # Subgroup for text scaling
    splash.append(text_group)

    return len(splash) - 1

def overwrite_text(text, index, scale=None, color_hex=None, x=None, y=None, font=None):
    #parameters:    text - string of what you want displayed
    #               scale - scale of text. try 2 or 3
    #               x - x coordinate of text to be displayed, from 0 to 320
    #               y - y coordinate of text to be displayed, from 0 to 240
    #               color_hex - hex color code. format 0x######
    #               index - the index of the group to be overwritten

    #text_group = displayio.Group(scale=scale, x=x, y=y)
    #text_area = label.Label(terminalio.FONT, text=text, color=color_hex)
    #text_group.append(text_area)  # Subgroup for text scaling
    splash[index][0].text = text
    if color_hex is not None:
        splash[index][0].color = color_hex
    if scale is not None:
        splash[index].scale = scale
    if x is not None:
        splash[index].x = x
    if y is not None:
        splash[index].y = y
    if font is not None:
        splash[index][0].font = font

    return

def draw_image(filepath, x, y):
    #parameters:    filepath - string for path to file, currently bmp or png. ex: '/purple.bmp'. files are particular - ask Logan for help
    #               x - x coordinate of picture to be displayed, from 0 to 320
    #               y - y coordinate of picture to be displayed, from 0 to 240

    image, palette = adafruit_imageload.load(filepath)
    palette.make_transparent(0)
    tile_grid = displayio.TileGrid(image, pixel_shader=palette)
    tile_grid.x = x
    tile_grid.y = y
    splash.append(tile_grid)

    return

def draw_bitmap(filepath, x, y):
    #parameters:    filepath - string for path to file. ex: '/purple.bmp'. files are particular - ask Logan for help
    #               x - x coordinate of picture to be displayed, from 0 to 320
    #               y - y coordinate of picture to be displayed, from 0 to 240
    # less memory intensive, I think. will have to do some testing

    bitmap = displayio.OnDiskBitmap(filepath)
    bmp = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)
    bmp.x = x
    bmp.y = y
    splash.append(bmp)

    return

def draw_circle(x, y, r, color_hex):
    #parameters:    x - x coordinate of text to be displayed, from 0 to 320
    #               y - y coordinate of text to be displayed, from 0 to 240
    #               r - radius of circle
    #               color_hex - hex color code. format 0x######

    circ = circle.Circle(x0=x, y0=y, r=r, fill=color_hex)
    splash.append(circ)

    return

#fix later
def remove_text():
    splash.pop(-1)

def touch_input():
    #returns:       ft.touches[0] - a dict with the id, and y- and x-coords of the touched point

    if ft.touched: #1 if touched, 0 otherwise
        return ft.touches[0]

def draw_button(x, y, width, height, label):
    #parameters:    x - x coordinate of button to be displayed, from 0 to 320
    #               y - x coordinate of button to be displayed, from 0 to 240
    #               width - width of button to be displayed
    #               height - height of button to be displayed
    #               label - text of button to be displayed

    btn = Button(x=x, y=y, width=width, height=height, label=label, label_font=terminalio.FONT)
    splash.append(btn)

    return

def set_brightness(brightness):
    #parameters:    brightness - the desired brightness of the display, from 0 to 100

    pwm.duty_cycle = int(brightness/100 * (2**16 - 1))

    return
