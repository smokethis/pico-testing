import board
import digitalio
import asyncio
import neopixel
import ledcontroller
import pixeltest
import buttoncontroller
import esp01s
from my_secrets import secrets
import msonlinehandler
import writeepd
import adafruit_datetime as datetime
import timehandler



async def ledtesting():
    print("Testing onboard LED and onboard neopixel")
    # Create the testing tasks
    obled_task = asyncio.create_task(obled.blinkonboardled(obled, 3))
    neopixel_task = asyncio.create_task(pixeltest.testsingleneopixel(obpixel))
    # Run the tasks
    await asyncio.gather(obled_task, neopixel_task)
    print("Testing complete")

async def wifitesting():
    # Testing WiFi connection and pin
    print("Testing WiFi connection...")
    await espwifi.wifipingtest("8.8.8.8")
    # Testing GET request
    print("Testing GET request...")
    # Check for a response from HTTPBin and print the body if it's OK
    response = await espwifi.getrequest("https://httpbin.org/anything")
    if response.status_code == 200:
        print("Response OK")
        print("Body: {}".format(response.text))
    else:
        print("Response failed")
        print("Status code: {}".format(response.status_code))

# Define the testing function
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

# Get next event in a list
async def get_next_event(events):
    now = datetime.datetime.now()
    for event in events:
        # Convert the start time to datetime object from ISO format
        es = datetime.datetime.fromisoformat(event["start"])
        if es > now:
            return event

# Define the main function
async def main():
    print("Starting main program")

    print("Setting up devices...")

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
    
    print("Connecting to WiFi...")
    espwifi.esp.connect(secrets)

    # Set the RTC
    print("Setting RTC...")
    await timehandler.set_rtc_time(espwifi, secrets)

    # Get Azure AD token
    print("Getting Azure AD token...")
    msapi = msonlinehandler.aadtoken()
    await msapi.gettoken(espwifi, epd, obled, obpixel)

    # Get today's calendar
    cal_today = await msapi.gettodayscalendar(espwifi)

    # Write the calendar to the console
    print("Today's calendar:")
    print(cal_today)

    # Get the next event
    nextevent = await get_next_event(cal_today)
    print("Next event:")
    print(nextevent)
    # Construct the message to display
    message = []
    # Message must be in dictionary format with the following keys:
    # text - The text to display
    # x - The x position of the text
    # y - The y position of the text
    # colour - The colour of the text (black or red)
    # size - The size of the text (1 = 8px, 2 = 16px, 3 = 24px etc)
    # The message must be a list of dictionaries
    message.append({"text": nextevent["subject"], "x": 0, "y": 0, "colour": "red", "size": 2})
    # Create a line which has both the start and end times
    message.append({"text": nextevent["start"].strftime("%H:%M") + " - " + nextevent["end"].strftime("%H:%M"), "x": 0, "y": 36, "colour": "black", "size": 2})
    # Write the message to the display
    await epd.writetodisplay(message)
    
    # Fetch the next calendar event
    # nextevent = today
    # await epd.writetodisplay(today)

    print("Main program complete")

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