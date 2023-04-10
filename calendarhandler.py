from adafruit_datetime import datetime
import utils

async def get_next_event(events):
    """
    Get the next event from a list of events.
    Parameters:
        events (list): A list of events in Microsoft Graph format
    Returns:
        The next event
    """
    for event in events:
        if event["start"] > utils.get_current_time():
            return event

async def eventprocessing(cal_today):
        
        # Get the next event
        nextevent = await get_next_event(cal_today)
        print("Next event:")
        print(nextevent)

        # Construct the message to display
        message = []
        # Message must be in dictionary format with the following keys:
        # text - The text to display
        # x - The x position of the text
        # y - The y position of the text
        # colour - The colour of the text (black or red)
        # size - The size of the text (1 = 8px, 2 = 16px, 3 = 24px etc)
        # The message must be a list of dictionaries
        # If there is a nextevent object, display it
        if nextevent != None:
            # Create a line which has the subject
            message.append({"text": nextevent["subject"], "x": 0, "y": 0, "colour": "red", "size": 2})
            # Create a line which has both the start and end times
            message.append({"text": nextevent["start"].strftime("%H:%M") + " - " + nextevent["end"].strftime("%H:%M"), "x": 0, "y": 36, "colour": "black", "size": 2})
        else:
            # Write a message to say there are no more events today
            message.append({"text": "No more events today", "x": 0, "y": 0, "colour": "red", "size": 2})
        # Return the message
        return message