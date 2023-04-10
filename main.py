import asyncio
import ledcontroller
import buttoncontroller
from my_secrets import secrets
import msonlinehandler
import adafruit_datetime as datetime
import pixelcontroller
import timehandler
import hardware
from adafruit_led_animation import color
import time

today = datetime.date.today()

sample_events = [
    {
        'start': datetime.datetime.combine(today, datetime.time(8, 0)),
        'end': datetime.datetime.combine(today, datetime.time(8, 30)),
        'subject': 'Event 1'
    },
    {
        'start': datetime.datetime.combine(today, datetime.time(9, 0)),
        'end': datetime.datetime.combine(today, datetime.time(10, 30)),
        'subject': 'Event 2'
    },
    {
        'start': datetime.datetime.combine(today, datetime.time(10, 30)),
        'end': datetime.datetime.combine(today, datetime.time(11, 0)),
        'subject': 'Event 3'
    },
    {
        'start': datetime.datetime.combine(today, datetime.time(12, 0)),
        'end': datetime.datetime.combine(today, datetime.time(13, 0)),
        'subject': 'Event 4'
    },
    {
        'start': datetime.datetime.combine(today, datetime.time(14, 0)),
        'end': datetime.datetime.combine(today, datetime.time(15, 0)),
        'subject': 'Event 5'
    },
    {
        'start': datetime.datetime.combine(today, datetime.time(16, 0)),
        'end': datetime.datetime.combine(today, datetime.time(17, 0)),
        'subject': 'Event 6'
    }
]


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
    # Test the neopixel ring
    await pixelcontroller.testpixelring()

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

async def flashcurrentperiod(period, basecolour, interval=5):
    """ Flashes the specified pixel white.
    Flashes the specified period white and back again every [interval] seconds, default of 5.
    Args:
        period (int): The current period.
        basecolour (tuple): The base colour of the pixel.
        interval (int): The interval between flashes.
    Returns:
        None
    """
    await pixelcontroller.pulsepixel(period, basecolour)
    await asyncio.sleep(interval)

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
    cal_output = await msapi.gettodayscalendar()
    if cal_output != None:
        print("Today's Calendar")
        print(cal_output)
    else:
        print("No events today")
        return
    
    # Loop through each event
    cal_today = []
    for event in cal_output:
        # Convert the start time to datetime object from ISO format with 8 fractional seconds
        date_str, time_str = event["start"].split('T')
        year, month, day = [int(x) for x in date_str.split('-')]
        # Dump the fractional seconds
        time_str, _ = time_str.split('.')
        hour, minute, second = [int(x) for x in time_str.split(':')]
        es = datetime.datetime(year, month, day, hour, minute, second)
        # Convert the start time to datetime object from ISO format with 8 fractional seconds
        date_str, time_str = event["end"].split('T')
        year, month, day = [int(x) for x in date_str.split('-')]
        # Dump the fractional seconds
        time_str, _ = time_str.split('.')
        hour, minute, second = [int(x) for x in time_str.split(':')]
        ee = datetime.datetime(year, month, day, hour, minute, second)
        # Create a new dictionary object
        newevent = {}
        # Add the start time to the dictionary
        newevent["start"] = es
        # Add the end time to the dictionary
        newevent["end"] = ee
        # Add the subject to the dictionary
        newevent["subject"] = event["subject"]
        # Append the new dictionary to the array
        cal_today.append(newevent)
    
    # Sort the array by the start time
    cal_today = sorted(cal_today, key=lambda k: k["start"])

    # Print the calendar and wait for input
    print("Today's calendar:")
    print(cal_today)
    input("Press enter to continue")
    
    # Get the next event
    nextevent = await get_next_event(cal_today)
    print("Next event:")
    print(nextevent)

    # Get the next event once
    await eventprocessing(cal_today)
    
    # Get the current time
    now = datetime.datetime.now()
        
    # Is it the morning or the afternoon?
    if now < datetime.time(12, 0):
        # Set the start time to 0800 and the finish time to 1200
        start_time = datetime.time(8, 0)
        finish_time = datetime.time(12, 0)
    else:
        # Set the start time to 1300 and the finish time to 1700
        start_time = datetime.time(13, 0)
        finish_time = datetime.time(17, 0)

    # Map events to periods
    periods = await mapcalendar(cal_today, start_time, finish_time, datetime.timedelta(minutes=30))
    
    # Illuminate the neopixel ring to show the periods
    await pixelcontroller.illuminateperiods(periods)

    # Create a pixel pulse loop
    pixelpulseloop = asyncio.get_event_loop()
    pixelpulseloop.create_task(pixelcontroller.pulsepixel(1))

    #########################
    ##### Start the main loop
    #########################
    # loop = asyncio.get_event_loop()

    # # Return the time rounded up to the nearest 5 minutes
    # next5mintime = datetime.datetime.now().replace(minute=0, second=0, microsecond=0) + datetime.timedelta(minutes=5)
    # loop.call_at(next5mintime, eventprocessing(cal_today))

    print("Main program complete")

async def mapcalendar(calendar, start_time, end_time, time_period_duration):
    """ Maps events in a calendar to periods.
    Maps events in a calendar to periods. The start and end times and period duration are provided as arguments.
    Args:
        calendar (list): A list of events in the calendar.
        start_time (datetime.time): The start time of the first period.
        end_time (datetime.time): The end time of the last period.
        time_period_duration (datetime.timedelta): The duration of each period.
    Returns:
        list: A list of period numbers.
    """
    # Initialise a list to hold the periods
    periods = []

    # Loop through all the events in the calendar
    for event in calendar:
        # Check if the event falls within the specified time period
        if start_time <= event['start'].time() < end_time:
            # Calculate the time difference between the event start time and the start time of the first time period
            time_diff = datetime.datetime.combine(event['start'].date(), event['start'].time()) - datetime.datetime.combine(event['start'].date(), start_time)

            # Loop through each time period between the event start time and end time
            period_start_time = event['start']
            while period_start_time < event['end']:
                # Divide the time difference by the time period duration and round up to get the period number
                period_number = -(-time_diff // time_period_duration)

                # Print the period number for the current time period
                print(f"Event {event['subject']} occupies period {period_number} ({period_start_time.time()} to {period_start_time + time_period_duration}).")
                
                # Increment the period start time by the duration of a time period
                period_start_time += time_period_duration
                
                # Update the time difference to reflect the new start time
                time_diff = datetime.datetime.combine(event['start'].date(), period_start_time.time()) - datetime.datetime.combine(event['start'].date(), start_time)

                # Add the period number to the list of periods
                periods.append(period_number)
    # Return the list of periods
    return periods

############################
### --- Main program --- ###
############################

# Run testing?
runtest = False

# Run testing if required
if runtest == True:
    asyncio.run(testing())

# Run the main function
# asyncio.run(main())

# Blank all pixels
hardware.pixelring.fill(color.BLACK)

bobbins = asyncio.run(mapcalendar(sample_events, datetime.time(8, 0), datetime.time(12, 0), datetime.timedelta(minutes=15)))
asyncio.run(pixelcontroller.illuminateperiods(bobbins, 0.1))
# Create a pixel pulse task
loop = asyncio.get_event_loop()
# Run the pulse task 3 times
# for i in range(3):
#     print(f"Running pulse task {i}")
#     pulsetask = loop.create_task(pixelcontroller.pulsepixel(3, color.AMBER))
#     loop.run_until_complete(pulsetask)
#     time.sleep(2)

asyncio.run(pixelcontroller.countdown(30, color.GREEN))

##############################
### --- End of program --- ###
##############################