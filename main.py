import asyncio
import ledcontroller
import buttoncontroller
import esp01s
from my_secrets import secrets
import msonlinehandler
import adafruit_datetime as datetime
import timehandler
import hardware

# Define the testing function
async def testing():
    # Test the onboard LED
    await ledcontroller.blinkonboardled(3)
    # Test onboard buttons
    try:
        response = await buttoncontroller.monitorbuttons(hardware.button1, hardware.button2, hardware.button3)
        print("Button {} was pressed".format(response))
    except Exception as e:
        print("Error: {}".format(e))
    # Do wifitesting function
    await esp01s.wifitesting()

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
    
    print("Connecting to WiFi...")
    hardware.espwifi.esp.connect(secrets)

    # Set the RTC
    print("Setting RTC...")
    await timehandler.set_rtc_time(secrets)

    # Get Azure AD token
    print("Getting Azure AD token...")
    msapi = msonlinehandler.aadtoken()
    await msapi.gettoken()

    # Get today's calendar
    cal_today = await msapi.gettodayscalendar()

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
    await hardware.epd.writetodisplay(message)
    
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