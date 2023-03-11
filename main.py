import board
import digitalio
import asyncio
import neopixel
import ledtest
import pixeltest
import buttoncontroller
import esp01s
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

# Create the ESP01S object
obwifi = esp01s.esp01()

async def ledtesting():
    print("Testing onboard LED and onboard neopixel")
    # Create the testing tasks
    obled_task = asyncio.create_task(ledtest.blinkonboardled(obled, 3))
    neopixel_task = asyncio.create_task(pixeltest.testsingleneopixel(obpixel))
    # Run the tasks
    await asyncio.gather(obled_task, neopixel_task)
    print("Testing complete")

async def wifitesting():
    # Testing WiFi connection and pin
    print("Testing WiFi connection...")
    await obwifi.wifipingtest("8.8.8.8")
    # Testing GET request
    print("Testing GET request...")
    # Check for a response from HTTPBin and print the body if it's OK
    response = await obwifi.getrequest("https://httpbin.org/anything")
    if response.status_code == 200:
        print("Response OK")
        print("Body: {}".format(response.text))
    else:
        print("Response failed")
        print("Status code: {}".format(response.status_code))

# Define the main function
async def testing():
    # Await the testing function
    await ledtesting()
    # Await the buttontest function
    try:
        response = await buttoncontroller.monitorbuttons(button1, button2, button3)
        print("Button {} was pressed".format(response))
    except Exception as e:
        print("Error: {}".format(e))
    # Await the wifitesting function
    await wifitesting()

async def main():
    print("Starting main program")

############################
### --- Main program --- ###
############################

# Run testing?
runtest = False

# Run testing if required
if runtest == True:
    asyncio.run(testing())

# Run the main function
asyncio.run(main())

##############################
### --- End of program --- ###
##############################