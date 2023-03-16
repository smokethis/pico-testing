# *****************************************************************************
# * | File        :	  Pico_ePaper-2.66-B.py
# * | Author      :   Waveshare team
# * | Function    :   Electronic paper driver
# * | Info        :
# *----------------
# * | This version:   V1.0
# * | Date        :   2021-05-14
# # | Info        :   python demo
# -----------------------------------------------------------------------------
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documnetation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to  whom the Software is
# furished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

import time
import busio
import digitalio
import board
import adafruit_framebuf

# Display resolution
EPD_WIDTH       = 152
EPD_HEIGHT      = 296

WF_PARTIAL_2IN66 =[
0x00,0x40,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x80,0x80,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x40,0x40,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x80,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x0A,0x00,0x00,0x00,0x00,0x00,0x02,0x01,0x00,0x00,
0x00,0x00,0x00,0x00,0x01,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x22,0x22,0x22,0x22,0x22,0x22,
0x00,0x00,0x00,0x22,0x17,0x41,0xB0,0x32,0x36,
]

class EPD_2in9_B:
    def __init__(self):

        # create the spi device and pins we will need
        spi = busio.SPI(board.GP14, MOSI=board.GP11)
        ecs = digitalio.DigitalInOut(board.GP13)
        # Make ecs an output pin type
        ecs.direction = digitalio.Direction.OUTPUT
        dc = digitalio.DigitalInOut(board.GP10)
        # Make dc an output pin type
        dc.direction = digitalio.Direction.OUTPUT
        srcs = None    # can be None to use internal memory
        rst = digitalio.DigitalInOut(board.GP9)   # can be None to not use this pin
        # Make rst an output pin type
        rst.direction = digitalio.Direction.OUTPUT
        busy = digitalio.DigitalInOut(board.GP8)   # can be None to not use this pin

        self.reset_pin = rst
        
        self.busy_pin = busy
        self.cs_pin = ecs
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT
        self.lut = WF_PARTIAL_2IN66
        
        self.spi = spi
        self.dc_pin=dc
        
        self.buffer_black = bytearray(self.height * self.width // 8)
        self.buffer_red = bytearray(self.height * self.width // 8)
        self.imageblack = adafruit_framebuf.FrameBuffer(self.buffer_black, self.width, self.height, adafruit_framebuf.MHMSB)
        self.imagered = adafruit_framebuf.FrameBuffer(self.buffer_red, self.width, self.height, adafruit_framebuf.MHMSB)
        self.rotate = 1
        self.init()

    def digital_read(self, pin):
        return pin.value()

    def delay_ms(self, delaytime):
        time.sleep(delaytime / 1000.0)

    def spi_writebyte(self, data):
        while not self.spi.try_lock():
            pass
        self.spi.configure(baudrate=4000000)
        self.spi.write(bytes(data))

    def module_exit(self):
        self.digital_write(self.reset_pin, 0)

    # Hardware reset
    def reset(self):
        self.reset_pin.value = True
        self.delay_ms(50)
        self.reset_pin.value = False
        self.delay_ms(2)
        self.reset_pin.value = True

    def send_command(self, command):
        self.dc_pin.value = False
        self.cs_pin.value = False
        while not self.spi.try_lock():
            pass
        self.spi.configure(baudrate=4000000)
        self.spi.write(bytearray([command]))
        self.spi.unlock()
        self.cs_pin.value = True

    def send_data(self, data):
        self.dc_pin.value = True
        self.cs_pin.value = False
        while not self.spi.try_lock():
            pass
        self.spi.configure(baudrate=4000000)
        self.spi.write(bytes([data]))
        self.spi.unlock()
        self.cs_pin.value = True        
        
    def SetWindow(self, x_start, y_start, x_end, y_end):
        self.send_command(0x44)
        self.send_data((x_start>>3) & 0x1f)
        self.send_data((x_end>>3) & 0x1f)
        
        self.send_command(0x45)
        self.send_data(y_start&0xff)
        self.send_data((y_start&0x100)>>8)
        self.send_data((y_end&0xff))
        self.send_data((y_end&0x100)>>8)
        
    def SetCursor(self, x_start, y_start):
        self.send_command(0x4E)
        self.send_data(x_start & 0x1f)
        
        self.send_command(0x4f)
        self.send_data(y_start&0xff)
        self.send_data((y_start&0x100)>>8)
        
    def ReadBusy(self):
        print('e-Paper busy')
        time.sleep(0.05)
        while(self.busy_pin.value == 1):      # 0: idle, 1: busy
            time.sleep(0.01)    
        print('e-Paper busy release')
        time.sleep(0.05)
        
    def TurnOnDisplay(self):
        self.send_command(0x20)
        self.ReadBusy()
        
    def init(self):
        print('init')
        self.reset()
        self.ReadBusy()
        self.send_command(0x12)  
        self.ReadBusy()#waiting for the electronic paper IC to release the idle signal

        self.send_command(0x11)
        self.send_data(0x03)

        self.SetWindow(0, 0, self.width-1, self.height-1)
        
        self.send_command(0x21)    #resolution setting
        self.send_data (0x00)  
        self.send_data (0x80)  
        
        
        self.SetCursor(0,0)
        self.ReadBusy()
    
        
    def display(self):
        high = self.height
        if( self.width % 8 == 0) :
            wide =  self.width // 8
        else :
            wide =  self.width // 8 + 1
        self.send_command(0x24)
        for j in range(0, high):
            for i in range(0, wide):
                self.send_data(self.buffer_black[i + j * wide])   
        self.send_command(0x26)
        for j in range(0, high):
            for i in range(0, wide):
                self.send_data(~self.buffer_red[i + j * wide] & 0xFF)   

        self.TurnOnDisplay()

    
    def Clear(self, colorblack, colorred):
        high = self.height
        if( self.width % 8 == 0) :
            wide =  self.width // 8
        else :
            wide =  self.width // 8 + 1
        self.send_command(0x24)
        for j in range(0, high):
            for i in range(0, wide):
                self.send_data(colorblack)
        self.send_command(0x26)
        for j in range(0, high):
            for i in range(0, wide):
                self.send_data(~colorred & 0xFF)
                                
        self.TurnOnDisplay()

    def sleep(self):
        self.send_command(0X10) # deep sleep
        self.send_data(0x01)
        
if __name__=='__main__':
    epd = EPD_2in9_B()
    epd.Clear(0xff, 0xff)
    
    epd.imageblack.fill(0xff)
    epd.imagered.fill(0xff)
    epd.imageblack.text("Waveshare", 0, 10, 0x00)
    epd.imagered.text("ePaper-2.66-B", 0, 25, 0x00)
    epd.imageblack.text("RPi Pico", 0, 40, 0x00)
    epd.imagered.text("Hello World", 0, 55, 0x00)
    epd.display()
    epd.delay_ms(2000)
    
    epd.imagered.vline(10, 90, 40, 0x00)
    epd.imagered.vline(90, 90, 40, 0x00)
    epd.imageblack.hline(10, 90, 80, 0x00)
    epd.imageblack.hline(10, 130, 80, 0x00)
    epd.imagered.line(10, 90, 90, 130, 0x00)
    epd.imageblack.line(90, 90, 10, 130, 0x00)
    epd.display()
    epd.delay_ms(2000)
    
    epd.imageblack.rect(10, 150, 40, 40, 0x00)
    epd.imagered.fill_rect(60, 150, 40, 40, 0x00)
    epd.display()
    epd.delay_ms(2000)

        
    epd.Clear(0xff, 0xff)
    epd.delay_ms(2000)
    print("sleep")
    epd.sleep()