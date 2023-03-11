import board
import digitalio
import asyncio
import neopixel
import ledtest
import pixeltest
import buttoncontroller
import esp01stest
import busio

# Set up the onboard LED
obled = digitalio.DigitalInOut(board.LED)
obled.direction = digitalio.Direction.OUTPUT

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

async def testing():
    print("Testing onboard LED and onboard neopixel")
    # Create the testing tasks
    obled_task = asyncio.create_task(ledtest.blinkonboardled(obled, 3))
    neopixel_task = asyncio.create_task(pixeltest.testsingleneopixel(obpixel))
    # Run the tasks
    await asyncio.gather(obled_task, neopixel_task)
    print("Testing complete")

async def pulsetesting():
    print("Testing onboard neopixel pulse")
    # Create the testing tasks
    neopixel_task = asyncio.create_task(pixeltest.pulseneopixel(obpixel))
    # Run the tasks
    await asyncio.gather(neopixel_task)
    print("Testing complete")

############################
### --- Main program --- ###
############################

# Define the main function
async def main():
    # Await the testing function
    # await testing()
    # # Await the pulsetesting function
    # await pulsetesting()
    # # Await the buttontest function
    # try:
    #     response = await buttoncontroller.monitorbuttons(button1, button2, button3)
    #     print("Button {} was pressed".format(response))
    # except Exception as e:
    #     print("Error: {}".format(e))
    # Await the esp01stest function
    # try:
    # await esp01stest.wifipingtest("8.8.8.8")
    # except:
    #     print("Error: {}".format(e))
    # Try to send a GET request to HTTPBin
    # await esp01stest.getrequesttest()
    crapwifi = esp01stest.esp01()
    await crapwifi.wifipingtest("8.8.8.8")
    await crapwifi.getrequesttest()

# Run the main function
asyncio.run(main())

##############################
### --- End of program --- ###
##############################