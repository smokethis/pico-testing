import asyncio

async def blinkonboardled(ledobject, count):
    """
    Blink the onboard LED.
    Parameters:
        ledobject (digitalio.DigitalInOut): The onboard LED object
        count (int): The number of times to blink the LED
    """
    print("Testing onboard LED")
    for i in range(count):
        ledobject.value = True
        await asyncio.sleep(1)
        ledobject.value = False
        await asyncio.sleep(1)
    print("Onboard LED testing complete")