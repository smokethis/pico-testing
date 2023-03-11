import asyncio
from adafruit_led_animation.animation.pulse import Pulse

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

# async def pulseneopixel(pixelobj, brightness=0.2):
#     """
#     Test neopixel object with a pulse animation.
#     PROBABLY ONLY SUPPORT MULTIPLE PIXEL STRINGS
#     Parameters:
#         pixelobj (neopixel.NeoPixel): The neopixel object to test
#         brightness (float): The brightness to set the neopixel (default 0.2)
#     """
#     print("Testing neopixel pulse")
#     # Set the brightness
#     pixelobj.brightness = brightness
#     pulse = Pulse(pixelobj, speed=0.5, period=5, color=(255, 0, 0))
#     pulse.animate()
#     await asyncio.sleep(5)
#     print("Neopixel pulse testing complete")