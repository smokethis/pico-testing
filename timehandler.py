async def set_rtc_time(espwifi, secrets):
    
    import rtc
    import time
    import asyncio
    print("Setting NTP server...")
    espwifi.esp.sntp_config(True, secrets['timezone'], secrets['ntp_server'])
    # Get the time, check the year, if it is 1970 then retry every 10 seconds
    t = espwifi.esp.sntp_time
    while '1970' in t:
        print("Time not set, retrying...")
        t = espwifi.esp.sntp_time
        # print(time)
        await asyncio.sleep(10)
    # Convert the time to a string
    t = t.decode('ascii')
    print("Time received: {}".format(t))
    # Convert the time to a datetime object
    date_time = await convert_time(t)
    # Set the RTC
    boardclock = rtc.RTC()
    boardclock.datetime = time.struct_time((date_time.year, date_time.month, date_time.day, date_time.hour, date_time.minute, date_time.second, date_time.weekday(), 0, -1))

async def convert_time(t):

    # Convert the time to a datetime object using the datetime module
    # Extract individual components
    # day_of_week = t[:3]
    month = t[4:7]
    day = int(t[8:10])
    hour = int(t[11:13])
    minute = int(t[14:16])
    second = int(t[17:19])
    year = int(t[20:])

    # Map month abbreviation to month number
    month_map = {
        'Jan': 1,
        'Feb': 2,
        'Mar': 3,
        'Apr': 4,
        'May': 5,
        'Jun': 6,
        'Jul': 7,
        'Aug': 8,
        'Sep': 9,
        'Oct': 10,
        'Nov': 11,
        'Dec': 12
    }
    month_number = month_map[month]

    # Create datetime object
    from adafruit_datetime import datetime
    date_time = datetime(year, month_number, day, hour, minute, second)

    return date_time