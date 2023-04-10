import asyncio
import hardware
from adafruit_led_animation import color

def lerp(begin,end,t):
    return begin + (end - begin) * t

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

async def testpixelring(brightness=0.2):
    """
    Test a neopixel ring.
    Cycles through red, green, blue and off. Then paints a rainbow.
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

async def illuminateperiods(periods, brightness=0.1, colour=color.AMBER):
    """
    Illuminate pixels on the ring based on the periods provided.
    Parameters:
        periods (list): A list of periods to illuminate
        brightness (float): The brightness to set the neopixel (default 0.2)
    """
    # Set the brightness factor
    brightness_factor = 0.4
    # Divide each color component by the brightness factor
    new_color = tuple(int(component * brightness_factor) for component in colour)
    # Set the brightness
    hardware.pixelring.brightness = brightness
    # Set the pixels
    for period in periods:
        pixelnumber = period
        hardware.pixelring[pixelnumber] = new_color

async def pulsepixel(pixelnumber, colour, highcolour=color.WHITE, num_steps=20):
    """
    Pulse a pixel on the ring.
    Parameters:
        pixelnumber (int): The pixel number to pulse
        colour (tuple): The colour to pulse from
        highcolour (tuple): The colour to pulse to (default white)
        num_steps (int): The number of steps to pulse (default 10)
    """
    # Set the brightness factor
    brightness_factor = 0.4
    # Divide each color component by the brightness factor
    new_color = tuple(int(component * brightness_factor) for component in colour)
    
    while True:
        # Loop through each step in the gradient
        for i in range(num_steps):
            # Calculate the current color as a linear interpolation between the two colors
            current_color = (
                int(lerp(new_color[0], highcolour[0], i/num_steps)),
                int(lerp(new_color[1], highcolour[1], i/num_steps)),
                int(lerp(new_color[2], highcolour[2], i/num_steps))
            )
            hardware.pixelring[pixelnumber] = current_color
            # Pause for a short time to see the transition
            await asyncio.sleep(0.1)
        # Set the pixel to the high colour
        hardware.pixelring[pixelnumber] = highcolour
        # Pause for a short time to see the transition
        await asyncio.sleep(0.25)
        # Loop through each step in the gradient
        for i in range(num_steps):
            # Calculate the current color as a linear interpolation between the two colors
            current_color = (
                int(lerp(highcolour[0], new_color[0], i/num_steps)),
                int(lerp(highcolour[1], new_color[1], i/num_steps)),
                int(lerp(highcolour[2], new_color[2], i/num_steps))
            )
            hardware.pixelring[pixelnumber] = current_color
            # Pause for a short time to see the transition
            await asyncio.sleep(0.1)
        # Set the pixel to the low colour
        hardware.pixelring[pixelnumber] = new_color
        # Pause for a short time to see the transition
        await asyncio.sleep(0.25)

async def countdown(count, colour):
    """
    Count down from the number provided using the pixel ring.
    Parameters:
        count (int): The number to count down from in seconds
        colour (tuple): The pixel colour to use for the countdown
    """
    # Set the brightness factor
    brightness_factor = 0.4
    # Divide each color component by the brightness factor
    base_color = tuple(int(component * brightness_factor) for component in colour)
    
    # Use an attractor to get the users attention that a coundown is about to start
    for i in range(16):
        hardware.pixelring[i - 1] = base_color
        await asyncio.sleep(0.1)

    # If the count is less than 16, reduce the number of pixels to illuminate
    if count < 16:
        for pixelnumber in range(count):
            hardware.pixelring[pixelnumber] = base_color
        seconds_per_pixel = 1
    else:
        # Divide the number by 16 to get the number of seconds per pixel
        seconds_per_pixel = count / 16
        # Illuminate the ring
        hardware.pixelring.fill(base_color)

    # Loop through each pixel
    for pixelnumber in range(16):
        # Set the pixel to the base colour
        hardware.pixelring[pixelnumber] = base_color
        # Pulse this pixel to indicate it is active
        asyncio.wait_for((pulsepixel(pixelnumber, colour, colour, 8)), seconds_per_pixel)
        # # Pause for the number of seconds per pixel
        # await asyncio.sleep(seconds_per_pixel)
        # Set this pixel to off
        hardware.pixelring[pixelnumber] = color.BLACK