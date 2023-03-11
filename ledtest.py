import asyncio

async def blinkonboardled(ledobject, count):
    # Blink the onboard LED a number of times
    for i in range(count):
        ledobject.value = True
        await asyncio.sleep(1)
        ledobject.value = False
        await asyncio.sleep(1)
    print("Onboard LED testing complete")