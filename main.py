import board
import digitalio
import asyncio
import neopixel
import ledtest
import pixeltest

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
obpixel = neopixel.NeoPixel(board.GP28, 1)

async def testing():
    print("Testing onboard LED and onboard neopixel")
    # Create the testing tasks
    obled_task = asyncio.create_task(ledtest.blinkonboardled(obled, 3))
    neopixel_task = asyncio.create_task(pixeltest.testsingleneopixel(obpixel))
    # Run the tasks
    await asyncio.gather(obled_task, neopixel_task)
    print("Testing complete")

async def pixeltest():
    print("Testing neopixel")
    # Create the testing tasks
    neopixel_task = asyncio.create_task(pixeltest.testsingleneopixel(obpixel))
    # Run the tasks
    await asyncio.gather(neopixel_task)
    print("Testing complete")

############################
### --- Main program --- ###
############################

# Define the main function
async def main():
    # Run the testing function
    await testing()
# Run the main function
asyncio.run(main())

### --- End of program --- ###