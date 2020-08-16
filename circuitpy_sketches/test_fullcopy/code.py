import digitalio
import terminalio
import board
import displayio
import adafruit_il0398
from babel.babelflash import FlashBabel
from adafruit_display_text import label
import time

displayio.release_displays()
bcs = digitalio.DigitalInOut(board.D4)
bcs.direction = digitalio.Direction.OUTPUT
bcs.value = True
sdcs = digitalio.DigitalInOut(board.D5)
sdcs.direction = digitalio.Direction.OUTPUT
sdcs.value = True
srcs = digitalio.DigitalInOut(board.D6)
srcs.direction = digitalio.Direction.OUTPUT
srcs.value = True

spi = board.SPI()  # Uses SCK and MOSI
epd_cs = board.D9
epd_dc = board.D10
epd_reset = board.A4
epd_busy = board.A3

# Create the displayio connection to the display pins
display_bus = displayio.FourWire(spi, command=epd_dc, chip_select=epd_cs,
                                 reset=epd_reset, baudrate=1000000)
time.sleep(1)  # Wait a bit

# Create the display object - the third color is red (0xff0000)
DISPLAY_WIDTH = 300
DISPLAY_HEIGHT = 400

display = adafruit_il0398.IL0398(display_bus, width=DISPLAY_WIDTH,
                                 height=DISPLAY_HEIGHT,
                                 rotation=270, busy_pin=epd_busy,
                                 highlight_color=0xFFFFFF)

babel = FlashBabel(bcs)

display.show(None)
text = """Short sayings:
जान है तो जहान है
風向轉變時,有人築牆,\n有人造風車
Один в поле не воин.
ἄνθρωπος μέτρον
"""
# text = "ありがとございます"
# text = "Helloworld"
text_group = displayio.Group(max_size=10, scale=2, x=120, y=150)
text_area = label.Label(babel.font, text=text, color=0xFF0000) #babel.font
text_group.append(text_area)
text_area.x = -50
text_area.y = 0
display.show(text_group)
display.refresh()

while True:
    pass