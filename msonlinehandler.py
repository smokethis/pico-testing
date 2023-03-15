from adafruit_datetime import datetime, timedelta
import my_secrets as secrets

class aadtoken():
    # This class is used to get an AAD token from the Azure AD endpoint.
    # The token is used to authenticate with the Microsoft Graph API.
    # The token is valid for 1 hour.
    # The token is stored in the class variable self.token.
    # The token is refreshed when the class method gettoken() is called and the token is less than 5 minutes old.
    
    # Define the class variables
    token = None
    tokenexpiry = None

    # Define the class methods
    async def gettoken(self, obwifi):
        # This function gets an AAD token from the Azure AD endpoint.
        
        # Check if the token is less than 5 minutes old
        if self.tokenexpiry != None and self.tokenexpiry > datetime.now() + timedelta(minutes = 5):
            # Token is less than 5 minutes old, so return the current token
            return self.token
        
        # Token is more than 5 minutes old, so get a new token
        # Define the request parameters
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'grant_type': 'client_credentials',
            'client_id': secrets["clientid"],
            'client_secret': secrets["clientsecret"],
            'resource': 'https://graph.microsoft.com'
        }
        
        # Send the request
        print("Getting AAD token...")
        response = await obwifi.placefullrequest(obwifi.esp01s.requestcontent("POST", "https://login.microsoftonline.com/{}/oauth2/v2.0/token".format(secrets["tenantid"]), headers=headers, data=data))
        print("Done")
        
        # Check the response
        if response.status_code != 200:
            # There was an error, so raise an exception
            raise Exception("Error getting AAD token. Status code: {}. Response: {}".format(response.status_code, response.text))
        
        # Get the token
        self.token = response.json()['access_token']
        self.tokenexpiry = datetime.now() + timedelta(seconds = response.json()['expires_in'])
        
        # Return the token
        return self.token