import asyncio
import ledcontroller
import buttoncontroller
from my_secrets import secrets
import msonlinehandler
import adafruit_datetime as datetime
import pixelcontroller
import calendarhandler
import timehandler
import hardware
import utils
from adafruit_led_animation import color
import time
import writeepd

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
    while True:
        await pixelcontroller.pulsepixel(period, basecolour)
        await asyncio.sleep(interval)

async def getcurrentperiod():
    """ Gets the current period.
    Gets the current period based on the time of day. 
    Returns None if the current period is not during the working day (0800-1700 with 1200-1300 empty).
    Returns:
        int: The current period.
    """
    # Is it the morning or the afternoon?
    if utils.get_current_time() < datetime.time(12, 0):
        # It's the morning, so subtract 8 from the hour
        # Calculate which 15 minute period it is
        # Get the current time
        now = utils.get_current_time()
        # Get the current hour
        hour = now.hour - 8
        # Get the current minute
        minute = now.minute
        # Calculate the period
        period = (hour * 4) + (minute // 15)
        # Return the period
        return period
    elif utils.get_current_time() < datetime.time(17, 0) and utils.get_current_time() > datetime.time(13, 0):
        # It's the afternoon, so subtract 13 from the hour
        # Calculate which 15 minute period it is
        # Get the current time
        now = utils.get_current_time()
        # Get the current hour
        hour = now.hour - 13
        # Get the current minute
        minute = now.minute
        # Calculate the period
        period = (hour * 4) + (minute // 15)
        # Return the period
        return period
    else:
        # The current period is not during the working day
        return None

async def getaadtoken():
    # Get Azure AD token
    print("Getting Azure AD token...")
    # Create task to get the token and flash the onboard LED whilst the task executes
    t_aadtoken = asyncio.create_task(msonlinehandler.aadtoken())
    t_flashled = asyncio.create_task(hardware.obled.blinkonboardledforever(0.5))
    # Wait for the token to be created and then cancel the flash task
    await t_aadtoken
    t_flashled.cancel()

async def gettodayscalendar():
    """ Gets today's calendar.
    Gets today's calendar from Microsoft Graph and returns it as a list. Returns None if there are no events.
    Returns:
        list: A list of events for today.
    """
    # Get today's calendar
    # If calendar is empty, it will return an empty list
    print("Getting today's calendar...")
    t_getcalendar = asyncio.create_task(msonlinehandler.gettodayscalendar())
    cal_output = await t_getcalendar
    if cal_output != None:
        print("Today's Calendar")
        print(cal_output)
        return cal_output
    else:
        print("No events today")
        return None

async def main():

    # Blank all pixels
    hardware.pixelring.fill(color.BLACK)

    # Get the main event loop
    loop = asyncio.get_event_loop()

    print("Starting main program")
    
    print("Connecting to WiFi...")
    hardware.espwifi.esp.connect(secrets)

    # Set the RTC
    print("Setting RTC...")
    await timehandler.set_rtc_time(secrets)

    # Get an aad access token
    # If an exception is raised, catch it and print the error, light the onboard neopixel red and exit
    try:
        loop.run_until_complete(getaadtoken())
    except Exception as e:
        print("Error getting AAD token: {}".format(e))
        hardware.obpixel = (color.RED)
    # Get today's calendar
    # If an exception is raised, catch it and print the error, light the onboard neopixel red and exit
    try:
        cal_today = loop.run_until_complete(gettodayscalendar())
    except Exception as e:
        print("Error getting calendar: {}".format(e))
        hardware.obpixel = (color.RED)
    
    ####### Override the calendar with the test calendar #######
    cal_today = sample_events

    # Print the calendar and wait for input
    print("Today's calendar:")
    print(cal_today)
    input("Press enter to continue")
    
    # Is it the morning or the afternoon?
    if utils.get_current_time() < datetime.time(12, 0):
        # Set the start time to 0800 and the finish time to 1200
        start_time = datetime.time(8, 0)
        finish_time = datetime.time(12, 0)
    else:
        # Set the start time to 1300 and the finish time to 1700
        start_time = datetime.time(13, 0)
        finish_time = datetime.time(17, 0)

    # Map events to periods
    t_periods = asyncio.create_task(mapcalendar(cal_today, start_time, finish_time, datetime.timedelta(minutes=15)))
    # Get the current period
    t_currentperiod = asyncio.create_task(getcurrentperiod())
    # Wait for the tasks to complete
    r_periods = await asyncio.gather(t_periods, t_currentperiod)
    # Get the periods and current period from the results
    periods, currentperiod = r_periods
    # Get the current event
    currentevent = await calendarhandler.eventprocessing(cal_today)
    # Create task to write the current event to the eink display
    t_writeevent = asyncio.create_task(writeepd(currentevent))
    # Illuminate the neopixel ring to show the periods
    t_illuminatering = asyncio.create_task(pixelcontroller.illuminateperiods(periods))
    # Wait for the tasks to complete
    await asyncio.gather(t_writeevent, t_illuminatering)
    
    
    if currentperiod != None:
        # Calculate the time to the next 15-minute mark
        time_to_next_15_minute_mark = (15 - utils.get_current_time.minute % 15) * 60 - utils.get_current_time.second
        print(f"Time to next 15-minute mark: {time_to_next_15_minute_mark} seconds")
        t_flashcurrent = asyncio.wait_for(flashcurrentperiod(currentperiod, color.AMBER, 1), timeout=time_to_next_15_minute_mark)
        try:
            loop.run_until_complete(t_flashcurrent)
        except asyncio.TimeoutError:
            None
        finally:
            # Set the pixel to white
            hardware.pixelring[currentperiod] = color.WHITE
    else:
        print("Not during the working day")

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
asyncio.run(main())

##############################
### --- End of program --- ###
##############################