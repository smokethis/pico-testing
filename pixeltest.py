import asyncio

async def testsingleneopixel(pixelobj, brightness=0.2):
    """
    Test a single neopixel.
    Cycles through red, green, blue and off.
    Parameters:
        pixelobj (neopixel.NeoPixel): The neopixel object to test
        brightness (float): The brightness to set the neopixel (default 0.2)
    """
    print("Testing single neopixel")
    # Set the brightness
    pixelobj.brightness = brightness
    # Test the onboard neopixel
    pixelobj[0] = (255, 0, 0)
    await asyncio.sleep(1)
    pixelobj[0] = (0, 255, 0)
    await asyncio.sleep(1)
    pixelobj[0] = (0, 0, 255)
    await asyncio.sleep(1)
    pixelobj[0] = (0, 0, 0)
    print("Single neopixel testing complete")