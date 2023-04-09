import asyncio
from adafruit_led_animation.animation.pulse import Pulse
import hardware

async def testsingleneopixel(brightness=0.2):
    """
    Test a single neopixel.
    Cycles through red, green, blue and off.
    Parameters:
        pixelobj (neopixel.NeoPixel): The neopixel object to test
        brightness (float): The brightness to set the neopixel (default 0.2)
    """
    print("Testing single neopixel")
    # Set the brightness
    hardware.obpixel.brightness = brightness
    # Test the onboard neopixel
    hardware.obpixel[0] = (255, 0, 0)
    await asyncio.sleep(1)
    hardware.obpixel[0] = (0, 255, 0)
    await asyncio.sleep(1)
    hardware.obpixel[0] = (0, 0, 255)
    await asyncio.sleep(1)
    hardware.obpixel[0] = (0, 0, 0)
    print("Single neopixel testing complete")

async def pulseneopixel(brightness=0.2):
    """
    Test neopixel object with a pulse animation.
    Parameters:
        pixelobj (neopixel.NeoPixel): The neopixel object to test
        brightness (float): The brightness to set the neopixel (default 0.2)
    """
    print("Testing neopixel pulse")
    # Set the brightness
    hardware.obpixel.brightness = brightness
    pulse = Pulse(hardware.obpixel, speed=0.5, period=5, color=(255, 0, 0))
    pulse.animate()
    await asyncio.sleep(5)
    print("Neopixel pulse testing complete")

async def testpixelring(brightness=0.2):
    """
    Test a neopixel ring.
    Cycles through red, green, blue and off.
    Parameters:
        pixelobj (neopixel.NeoPixel): The neopixel object to test
        brightness (float): The brightness to set the neopixel (default 0.2)
    """
    print("Testing neopixel ring")
    # Set the brightness
    hardware.pixelring.brightness = brightness
    # Test the neopixel ring
    hardware.pixelring.fill((255, 0, 0))
    await asyncio.sleep(1)
    hardware.pixelring.fill((0, 255, 0))
    await asyncio.sleep(1)
    hardware.pixelring.fill((0, 0, 255))
    await asyncio.sleep(1)
    hardware.pixelring.fill((0, 0, 0))
    print("Neopixel ring testing complete")