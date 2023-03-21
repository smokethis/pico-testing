################################################################################
# Scan for available WiFi AP, connect to the speicifed AP and ping 8.8.8.8.
# This is modified from Adafruit's esp_atcontrol_simpletest.py.
#
# Hardware:
# - Maker Pi Pico or Maker Pi RP2040
# - ESP8266 WiFi module with Espressif AT Firmware v2.2.0 and above.
#
# Dependencies:
# - adafruit_requests
# - adafruit_espatcontrol
#
# Instructions:
# - Copy the lib folder to the CIRCUITPY device.
# - Modify the keys in secrets.py and copy to the CIRCUITPY device.
# - Make sure the UART pins are defined correctly according to your hardware.
#
#
# Author: Cytron Technologies
# Website: www.cytron.io
# Email: support@cytron.io
################################################################################

import asyncio
import board
import busio
import adafruit_requests as requests
import adafruit_espatcontrol.adafruit_espatcontrol_socket as socket
from adafruit_espatcontrol import adafruit_espatcontrol

# Get wifi details and more from a secrets.py file
try:
    from my_secrets import secrets
except ImportError:
    print("All secret keys are kept in secrets.py, please add them there!")
    raise

class requestcontent:
    def __init__(self, method, url, data = None, json = None, headers = None, stream = False, timeout = 1):
        """
        This class is used to store the request content.

        Parameters:
        -----------
        method (str): The HTTP method to use for the request.
        url (str): The URL for the request.
        data (str): (optional) Dictionary, list of tuples or bytes to send in the body of the request.
        json (dict[str,str]): (optional) json to send in the body of the request.
        headers (dict[str,str]): (optional) Dictionary of HTTP Headers to send with the request.
        stream (bool): (optional) Whether to immediately download the response content.
        timeout (float): (optional) How many seconds to wait for the server to send data before giving up.
        """
        self.method: str = method
        self.url: str = url
        self.data: str = data # Can only have data or json defined not both.
        self.json: dict[str,str] = json # Can only have data or json defined not both.
        self.headers: dict[str,str] = headers
        self.stream: bool = stream
        self.timeout: float = timeout
        # Make data and json arguments mutually exclusive
        if data is not None and json is not None:
            raise ValueError("data and json arguments are mutually exclusive, please only define one of them.")

class esp01:
    def __init__ (self):
        # Initialize UART connection to the ESP8266 WiFi Module.
        RX = board.GP17
        TX = board.GP16
        self.uart = busio.UART(TX, RX, receiver_buffer_size=2048)  # Use large buffer as we're not using hardware flow control.
        self.esp = adafruit_espatcontrol.ESP_ATcontrol(self.uart, 115200, debug=False)
        requests.set_socket(socket, self.esp)
        print("Resetting ESP module")
        self.esp.soft_reset()

    async def wifipingtest(self, ipaddress):
        """"
        This function scans for available WiFi AP, connects to the speicifed AP and
        ping the specified IP address.

        Parameters:
            ipaddress (string): The IP address to ping.
        """
        try:
            print("\nScanning nearby WiFi AP...")
            for ap in self.esp.scan_APs():
                print(ap)
            print("\nConnecting...")
            self.esp.connect(secrets)
            print("IP address:", self.esp.local_ip)
            
            print()

        except (ValueError, RuntimeError, adafruit_espatcontrol.OKError) as e:
            print("Failed, \n", e)
        
        # Run a ping test 3 times
        for i in range(3):
            print("Pinging ", ipaddress, "...", end="")
            print(self.esp.ping(ipaddress))
            await asyncio.sleep(1)

    async def getrequest(self, url):
        """"
        This function sends a GET request to the specified url and returns the response.

        Parameters:
            url (string): The URL to send the GET request to.
        """
        try:
                print("\nChecking WiFi connection...")
                while not self.esp.is_connected:
                    print("Connecting...")
                    self.esp.connect(secrets)
                
                print("\nSending GET request...")
                print("URL = ", url)
                r = requests.get(url)
                print("Sent OK")
                return r
        
        except (ValueError, RuntimeError, adafruit_espatcontrol.OKError) as e:
            print("Failed, \n", e)
    
    async def postrequest(self, url):
        """"
        This function sends a POST request to the specified url and returns the response.

        Parameters:
            url (string): The URL to send the POST request to.
        """
        try:
                print("\nChecking WiFi connection...")
                while not self.esp.is_connected:
                    print("Connecting...")
                    self.esp.connect(secrets)
                
                print("\nSending POST request...")
                print("URL = ", url)
                r = requests.post(url)
                print("Sent OK")
                return r
        
        except (ValueError, RuntimeError, adafruit_espatcontrol.OKError) as e:
            print("Failed, \n", e)
    
    async def placefullrequest(self, content):
        try:
                print("\nChecking WiFi connection...")
                while not self.esp.is_connected:
                    print("Connecting...")
                    self.esp.connect(secrets)
                
                print("\nSending request...")
                print("Method = ", content.method)
                print("URL = ", content.url)
                if content.method == "GET":
                    r = requests.get(content.url, data = content.data, json = content.json, headers = content.headers, stream = content.stream, timeout = content.timeout)
                elif content.method == "POST":
                    r = requests.post(content.url, data = content.data, json = content.json, headers = content.headers, stream = content.stream, timeout = content.timeout)
                elif content.method == "PUT":
                    r = requests.put(content.url, data = content.data, json = content.json, headers = content.headers, stream = content.stream, timeout = content.timeout)
                elif content.method == "DELETE":
                    r = requests.delete(content.url, data = content.data, json = content.json, headers = content.headers, stream = content.stream, timeout = content.timeout)
                elif content.method == "HEAD":
                    r = requests.head(content.url, data = content.data, json = content.json, headers = content.headers, stream = content.stream, timeout = content.timeout)
                else:
                    raise ValueError("Unsupported HTTP method. Use GET, POST, PUT, DELETE or HEAD.")
                print("Sent OK")
                return r
        except (ValueError, RuntimeError, adafruit_espatcontrol.OKError) as e:
            print("Failed, \n", e)

    async def wifitesting(self):
        # Testing WiFi connection and pin
        print("Testing WiFi connection...")
        await self.wifipingtest("8.8.8.8")
        # Testing GET request
        print("Testing GET request...")
        # Check for a response from HTTPBin and print the body if it's OK
        response = await self.getrequest("https://httpbin.org/anything")
        if response.status_code == 200:
            print("Response OK")
            print("Body: {}".format(response.text))
        else:
            print("Response failed")
            print("Status code: {}".format(response.status_code))