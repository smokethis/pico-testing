from adafruit_datetime import datetime, timedelta
from my_secrets import secrets
import asyncio
import esp01s
import json

class aadtoken():
    # This class is used to get an AAD access token from the Azure AD endpoint using the device code grant.
    # The token is used to authenticate with the Microsoft Graph API.
    # The token is valid for 1 hour.
    # The token is stored in the class variable self.accesstoken.
    # The token is refreshed when the class method gettoken() is called and the token is less than 5 minutes old.
    def __init__(self):
        # Define the class variables
        self.accesstoken = None
        self.tokenexpiry = None
        self.refreshtoken = None
        self.idtoken = None
        self.scope = None
    
    # Define the class methods
    async def gettoken(self, wifi, epd, led, pixel):
        # This function checks if the access token is less than 5 minutes old.
        # Check if the token is less than 5 minutes old
        if self.tokenexpiry != None and self.tokenexpiry > datetime.now() + timedelta(minutes = 5):
            # Token is less than 5 minutes old, so return the current token
            return self.accesstoken
        # Check if token has expired
        elif self.tokenexpiry != None and self.tokenexpiry < datetime.now():
            # Token has expired, so get a new token
            await self.getnewtokens(wifi, epd, led, pixel)
        # Check for a valid refresh token
        elif self.refreshtoken == None:
            # No refresh token, start new token request
            await self.getnewtokens(wifi, epd, led, pixel)
        elif self.refreshtoken != None:
            # Refresh token exists, so use it to get a new token
            await self.getnewtokenfromrefresh(wifi, epd)

    async def getnewtokens(self, wifi, epd, led, pixel):
        # This function gets a new AAD token from the Azure AD endpoint.
        # Create a task to clear the display
        # cleardisplay = asyncio.create_task(epd.epdclear())
        # Define the request parameters
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'grant_type': 'device_code',
            'client_id': secrets["clientid"],
            'scope': 'User.Read'
        }
        # Flash the onboard LED to indicate the request is being sent
        # ledtask = asyncio.create_task(led.blinkonboardledforever(0.5))
        # asyncio.run(ledtask)
        # Send the request
        print("Getting AAD token...")
        response = await wifi.placefullrequest(esp01s.requestcontent("POST", "https://login.microsoftonline.com/{}/oauth2/v2.0/devicecode".format(secrets["tenantid"]), headers=headers, data=data))
        print("Done")
        
        # Check the response
        if response.status_code != 200:
            # There was an error, so raise an exception
            raise Exception("Error getting AAD token. Status code: {}. Response: {}".format(response.status_code, response.text))
        
        print(response.json())
        # Store response data
        usercode = response.json()['user_code']
        devicecode = response.json()['device_code']
        verifyurl = response.json()['verification_uri']
        interval = response.json()['interval']
        
        # Stop flashing the onboard LED
        # ledtask.cancel()
        # await ledtask

        # Construct the message to display
        message = []
        # Message must be in dictionary format with the following keys:
        # text - The text to display
        # x - The x position of the text
        # y - The y position of the text
        # colour - The colour of the text (black or red)
        # size - The size of the text (1 = 8px, 2 = 16px, 3 = 24px etc)
        # The message must be a list of dictionaries
        message.append({'text': 'Please go to:', 'x': 0, 'y': 0, 'colour': 'black', 'size': 1})
        message.append({'text': verifyurl, 'x': 0, 'y': 20, 'colour': 'red', 'size': 1})
        message.append({'text': 'and enter the code:', 'x': 0, 'y': 40, 'colour': 'black', 'size': 1})
        message.append({'text': usercode, 'x': 0, 'y': 60, 'colour': 'red', 'size': 3})
        
        # Wait for the displaytask to complete 
        # Create a task to display the user code
        # displaytask = asyncio.create_task(epd.writetext(message))
        # asyncio.run(displaytask)
        
        # Start polling for the access token
        # Define the request parameters
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'grant_type': 'urn:ietf:params:oauth:grant-type:device_code',
            'client_id': secrets["clientid"],
            'device_code': devicecode,
            'scope': 'User.Read'
        }

        # Loop requesting the access tokens until it is ready or the user declines the request
        while True:
            print("Polling for AAD token...")
            # Send the request
            response = await wifi.placefullrequest(esp01s.requestcontent("POST", "https://login.microsoftonline.com/{}/oauth2/v2.0/token".format(secrets["tenantid"]), headers=headers, data=data, timeout=interval))
            print("Done")
            # Print the response
            print(response.json())
            # Check the response for expected errors
            if response.status_code == 400 and response.json()['error'] == 'authorization_pending':
                # The token is not ready yet, so wait [interval] seconds and try again
                print("Waiting for user to accept the request... sleeping for {} seconds".format(interval))
                continue
            elif response.status_code == 400 and response.json()['error'] == 'authorization_declined':
                # The user declined the request, so raise an exception
                raise Exception("User declined the request")
            elif response.status_code != 200:
                # There was an unexpected error, so raise an exception
                raise Exception("Error getting AAD token. Status code: {}. Response: {}".format(response.status_code, response.text))
            elif response.status_code == 200:
                # The token is ready, so break out of the loop
                break
            else:
                # There was an unexpected error, so raise an exception
                raise Exception("Error getting AAD token. Status code: {}. Response: {}".format(response.status_code, response.text))
        
        # return response.json()['access_token'], response.json()['refresh_token'], response.json()['id_token'], response.json()['scope'], response.json()['expires_in']
        # self.refreshtoken = response.json()['refresh_token']
        # self.idtoken = response.json()['id_token']
        self.accesstoken = response.json()['access_token']
        self.scope = response.json()['scope']
        self.tokenexpiry = datetime.now() + timedelta(seconds = response.json()['expires_in'])
        # Check if the displaytask is still running
        while displaytask.done() == False:
            # Display task is still running, wait for it to complete
            asyncio.wait(0.1)
        # Display task is complete, so clear the display
        dislplaytask = asyncio.create_task(epd.epdclear())
        asyncio.run(displaytask)
    
    async def gettodayscalendar(self, wifi):
        # Use Microsoft Graph API to get today's calendar events for the user
        # Define the request parameters
        headers = {
            'Authorization': 'Bearer {}'.format(self.accesstoken),
            'Content-Type': 'application/json'
        }
        query = "id,subject,start,end"
        # Send the request
        response = await wifi.placefullrequest(esp01s.requestcontent("GET", "https://graph.microsoft.com/v1.0/me/calendarview?startdatetime={}&enddatetime={}&$select={}".format(datetime.now().strftime("%Y-%m-%dT00:00:00"), datetime.now().strftime("%Y-%m-%dT23:59:59"), query), headers=headers))
        # Check the response
        if response.status_code != 200:
            # There was an error, so raise an exception
            raise Exception("Error getting calendar events. Status code: {}. Response: {}".format(response.status_code, response.text))
        # Return the response
        return json.loads(response.text)