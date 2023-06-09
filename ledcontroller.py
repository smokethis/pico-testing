import asyncio
import digitalio
import board

class obled():
    def __init__(self):
        # Set up the onboard LED
        self.obled = digitalio.DigitalInOut(board.LED)
        self.obled.direction = digitalio.Direction.OUTPUT

    async def blinkonboardled(self, count, rate=1):
        """
        Blink the onboard LED.
        Parameters:
            ledobject (digitalio.DigitalInOut): The onboard LED object
            count (int): The number of times to blink the LED
            rate (float): The rate at which to blink the LED
        """
        for i in range(count):
            self.value = True
            await asyncio.sleep(rate)
            self.value = False
            await asyncio.sleep(rate)

    async def blinkonboardledforever(self, rate=0.5):
        """
        Blink the onboard LED forever.
        Parameters:
            ledobject (digitalio.DigitalInOut): The onboard LED object
            rate (float): The rate at which to blink the LED
        """
        # Wait for the task to be cancelled
        while asyncio.CancelledError is False:
            self.value = True
            await asyncio.sleep(rate)
            self.value = False
            await asyncio.sleep(rate)
        # Turn the LED off when the task is cancelled
        self.value = False