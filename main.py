import board
import digitalio
import asyncio
import time
from pixelcontroller import neopixelobject

# Set up the onboard LED
obled = digitalio.DigitalInOut(board.LED)
obled.direction = digitalio.Direction.OUTPUT

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

# Set up the onboard neopixel
obpixel = neopixelobject(board.GP28, 1)

async def blinkonboardled(count):
    # Blink the onboard LED a number of times
    for i in range(count):
        obled.value = True
        await asyncio.sleep(1)
        obled.value = False
        await asyncio.sleep(1)
    print("Onboard LED testing complete")

async def testsingleneopixel():
    # Test the onboard neopixel
    obpixel.set_pixel_colour((255, 0, 0), 0)
    await asyncio.sleep(1)
    obpixel.set_pixel_colour((0, 255, 0), 0)
    await asyncio.sleep(1)
    obpixel.set_pixel_colour((0, 0, 255), 0)
    await asyncio.sleep(1)
    obpixel.set_pixel_colour((0, 0, 0), 0)
    print("Onboard neopixel testing complete")



### --- Main program --- ###

# Define the main function
async def main():
    print("Testing onboard LED and onboard neopixel")
    # Create the testing tasks
    obled_task = asyncio.create_task(blinkonboardled(3))
    obpixel_task = asyncio.create_task(testsingleneopixel())
    # Run the tasks
    await asyncio.gather(obled_task, obpixel_task)
    print("Testing complete")

    obpixel.pulse_pixel_colour((255, 0, 0), 0.1, 0)
    time.sleep(5)
    
# Run the main function
asyncio.run(main())

### --- End of program --- ###