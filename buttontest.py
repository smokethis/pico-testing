import asyncio

async def monitorbuttons(button1, button2, button3):
    print("Waiting for button press")
    while True:
        if not button1.value:
            return "1"
        if not button2.value:
            return "2"
        if not button3.value:
            return "3"
        await asyncio.sleep(0.1)