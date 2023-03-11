import neopixel
from adafruit_led_animation.animation.colorcycle import ColorCycle
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.animation.rainbow import Rainbow
import time
import board

class Neopixelcontroller:

    def __init__(self, pin, numpixels):
        """
        The constructor for neopixelcontroller class
        
        Parameters:
            pin (board): The pin to use for the neopixel (eg. board.GP28)
            numpixels (int): The number of pixels in the object
        """
        self.pixelobj = neopixel.NeoPixel(pin, numpixels)

    def set_pixel_colour(self, basecolour, pixel=0):
        """
        Set a pixel to a specific colour
        
        Parameters:
            basecolour (tuple): The colour to set the pixel to (eg. (255, 0, 0))
            pixel (int): The pixel number to set the colour of (default 0)
            pixelbrightness (float): The brightness of the pixel (default 0.5)
        """
        self.pixelobj.brightness = 0.2
        self.pixelobj[pixel] = basecolour

    def rainbow_cycle(self, speed, period):
        """
        Set all pixelobj to cycle through a rainbow
        
        Parameters:
            speed (float): The speed to cycle the colours at in seconds (eg. 0.1)
            period (float): The time in seconds to cycle the colours for (eg. 5)
            pixelbrightness (float): The brightness of the pixel (default 0.5)
        """
        self.pixelobj.brightness = 0.2
        # Try to animate the rainbow
        try:
            print("Starting rainbow cycle")
            rainbow = Rainbow(self.pixelobj, speed, period)
            print("Animating rainbow cycle")
            rainbow.animate()
            print("Sleeping for 5 seconds")
            time.sleep(5)
        except Exception as e:
            input("Error: " + str(e))
            return False

    def cycle_pixel_colour(self, colors, speed, pixel):
        """
        Set a pixel to cycle through a list of colours
        
        Parameters:
            colors (list): The list of colours to cycle through (eg. [(255, 0, 0), (0, 255, 0), (0, 0, 255)])
            speed (float): The speed to cycle the colours at in seconds (eg. 0.1)
            pixel (int): The pixel number to cycle the colour of
        """
        self.pixelobj.brightness = 0.5
        colorcycle = ColorCycle(self.pixelobj[pixel], speed, colors)
        colorcycle.animate()

    def pulse_pixel_colour(self, color, speed, pixel):
        """
        Set a pixel to pulse a colour
        
        Parameters:
            color (tuple): The colour to pulse (eg. (255, 0, 0))
            speed (float): The speed to pulse the colour at in seconds (eg. 0.1)
            pixel (int): The pixel number to pulse the colour of
        """
        self.pixelobj.brightness = 0.5
        pulse = Pulse(self.pixelobj[pixel], speed, color)
        pulse.animate()