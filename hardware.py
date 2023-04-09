import board
import digitalio
import neopixel
import ledcontroller
import esp01s
import writeepd

# Set up the onboard LED
obled = ledcontroller.obled()

# Set up the onboard neopixel
obpixel = neopixel.NeoPixel(board.GP28, 1)

# Set up the Maker Pi Pico buttons
button1 = digitalio.DigitalInOut(board.GP20)
button1.direction = digitalio.Direction.INPUT
button1.pull = digitalio.Pull.UP

button2 = digitalio.DigitalInOut(board.GP21)
button2.direction = digitalio.Direction.INPUT
button2.pull = digitalio.Pull.UP

button3 = digitalio.DigitalInOut(board.GP22)
button3.direction = digitalio.Direction.INPUT
button3.pull = digitalio.Pull.UP

# Create the ESP01S object
espwifi = esp01s.esp01()

# Create Waveshare eink display
epd = writeepd.waveshare_eink()

# Set up the neopixel ring
pixelring = neopixel.NeoPixel(board.GP1, 16, bpp=4)