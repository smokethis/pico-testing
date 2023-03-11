import asyncio

async def monitorbuttons(button1, button2, button3):
    """
    This function monitors the three Maker Pi Pico buttons.
    When a button is pressed, it returns the pressed button number as a string.

    Parameters:
        button1 (digitalio.DigitalInOut): The button 1 object
        button2 (digitalio.DigitalInOut): The button 2 object
        button3 (digitalio.DigitalInOut): The button 3 object
    """
    print("Waiting for button press")
    while True:
        if not button1.value:
            return "1"
        if not button2.value:
            return "2"
        if not button3.value:
            return "3"
        await asyncio.sleep(0.1)