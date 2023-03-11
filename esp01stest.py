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
        # print("ESP Firmware Version:", self.esp.version)

        first_pass = True
        try:
            if first_pass:
                print("\nScanning nearby WiFi AP...")
                for ap in self.esp.scan_APs():
                    print(ap)
                print("\nConnecting...")
                self.esp.connect(secrets)
                print("IP address:", self.esp.local_ip)
                
                print()
                first_pass = False

        except (ValueError, RuntimeError, adafruit_espatcontrol.OKError) as e:
            print("Failed, retrying\n", e)
        
        # Run a ping test 3 times
        for i in range(3):
            print("Pinging 8.8.8.8...", end="")
            print(self.esp.ping(ipaddress))
            await asyncio.sleep(1)

    async def getrequesttest(self):
        """"
        This function scans for available WiFi AP, connects to the speicifed AP and
        sends a GET request to the HTTPBin website.
        """
        # print("ESP Firmware Version:", self.esp.version)
        try:
                print("\nChecking WiFi connection...")
                while not self.esp.is_connected:
                    print("Connecting...")
                    self.esp.connect(secrets)
                
                print("\nSending HTTPBin message...")
                message = "Hello World from Circuitpython :)"
                get_url = "http://www.httpbin.org"
                get_url += "/anything"
                get_url += "/sendMessage?chat_id="
                get_url += "&text="
                get_url += message
                print("URL = ", get_url)
                r = requests.get(get_url)
                print("Sent OK")
                print("HTTP Response Code: ", r.status_code)
                print("Response text: ", r.text)

        except (ValueError, RuntimeError, adafruit_espatcontrol.OKError) as e:
            print("Failed, retrying\n", e)