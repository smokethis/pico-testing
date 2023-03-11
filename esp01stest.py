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


async def wifipingtest(ipaddress):
    """"
    This function scans for available WiFi AP, connects to the speicifed AP and
    ping the specified IP address.

    Parameters:
        ipaddress (string): The IP address to ping.
    """
    # Get wifi details and more from a secrets.py file
    try:
        from my_secrets import secrets
    except ImportError:
        print("All secret keys are kept in secrets.py, please add them there!")
        raise


    # Initialize UART connection to the ESP8266 WiFi Module.
    RX = board.GP17
    TX = board.GP16
    uart = busio.UART(TX, RX, receiver_buffer_size=2048)  # Use large buffer as we're not using hardware flow control.

    esp = adafruit_espatcontrol.ESP_ATcontrol(uart, 115200, debug=False)
    requests.set_socket(socket, esp)

    print("Resetting ESP module")
    esp.soft_reset()
    print("ESP Firmware Version:", esp.version)

    first_pass = True
    try:
        if first_pass:
            print("\nScanning nearby WiFi AP...")
            for ap in esp.scan_APs():
                print(ap)
            print("\nConnecting...")
            esp.connect(secrets)
            print("IP address:", esp.local_ip)
            
            print()
            first_pass = False

    except (ValueError, RuntimeError, adafruit_espatcontrol.OKError) as e:
        print("Failed, retrying\n", e)
    
    # Run a ping test 3 times
    for i in range(3):
        print("Pinging 8.8.8.8...", end="")
        print(esp.ping(ipaddress))
        await asyncio.sleep(1)