import asyncio
import ledcontroller
import buttoncontroller
from my_secrets import secrets
import msonlinehandler
import adafruit_datetime as datetime
import pixelcontroller
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
    await hardware.esp01s.wifitesting()

# Get next event in a list
async def get_next_event(events):
    now = datetime.datetime.now()
    for event in events:
        # Convert the start time to datetime object from ISO format
        es = datetime.datetime.fromisoformat(event["start"])
        if es > now:
            return event

async def eventprocessing(cal_today):
        
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
        # If there is a nextevent object, display it
        if nextevent != None:
            # Create a line which has the subject
            message.append({"text": nextevent["subject"], "x": 0, "y": 0, "colour": "red", "size": 2})
            # Create a line which has both the start and end times
            message.append({"text": nextevent["start"].strftime("%H:%M") + " - " + nextevent["end"].strftime("%H:%M"), "x": 0, "y": 36, "colour": "black", "size": 2})
        else:
            # Write a message to say there are no more events today
            message.append({"text": "No more events today", "x": 0, "y": 0, "colour": "red", "size": 2})
        # Write the message to the display
        await hardware.epd.writetext(message)
        
        # Fetch the next calendar event
        # nextevent = today
        # await epd.writetodisplay(today)

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
    # If calendar is empty, it will return an empty list
    print("Getting today's calendar...")
    cal_today = await msapi.gettodayscalendar()
    if cal_today != None:
        print("Today's Calendar")
        print(cal_today)
    else:
        print("No events today")
        return
    
    # Get the next event once
    await eventprocessing(cal_today)

    #########################
    ##### Start the main loop
    #########################
    loop = asyncio.get_event_loop()
    # Get the current time
    now = datetime.datetime.now()
    # Return the time rounded up to the nearest 30 minutes
    next30mintime = now.replace(minute=0, second=0, microsecond=0) + datetime.timedelta(minutes=30)
    loop.call_at(next30mintime, eventprocessing(cal_today))
    

    print("Main program complete")

async def pixeltesting():
    await pixelcontroller.testpixelring()


############################
### --- Main program --- ###
############################

# Run testing?
runtest = False

# Run testing if required
if runtest == True:
    asyncio.run(testing())

# Run the main function
asyncio.run(pixeltesting())

##############################
### --- End of program --- ###
##############################