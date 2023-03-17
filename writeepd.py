import epd2in66b


class waveshare_eink:
    def __init__(self):
        # Create the Waveshare eink display
        print("Init eink display")
        self.epd = epd2in66b.EPD_2in9_B()
        # self.epd.init()
        self.epd.Clear(0xff, 0xff)
        
    async def epdtesting(self):
        # Run the eink display test
        print("Testing eink display")
        self.epd.Clear(0xff, 0xff)

        self.epd.imageblack.fill(0xff)
        self.epd.imagered.fill(0xff)
        self.epd.imageblack.text("Waveshare", 0, 10, 0x00)
        self.epd.imagered.text("ePaper-2.66-B", 0, 25, 0x00)
        self.epd.imageblack.text("RPi Pico", 0, 40, 0x00)
        self.epd.imagered.text("Hello World", 0, 55, 0x00)
        self.epd.display()
        self.epd.delay_ms(2000)

        self.epd.imagered.vline(10, 90, 40, 0x00)
        self.epd.imagered.vline(90, 90, 40, 0x00)
        self.epd.imageblack.hline(10, 90, 80, 0x00)
        self.epd.imageblack.hline(10, 130, 80, 0x00)
        self.epd.imagered.line(10, 90, 90, 130, 0x00)
        self.epd.imageblack.line(90, 90, 10, 130, 0x00)
        self.epd.display()
        self.epd.delay_ms(2000)

        self.epd.imageblack.rect(10, 150, 40, 40, 0x00)
        self.epd.imagered.fill_rect(60, 150, 40, 40, 0x00)
        self.epd.display()
        self.epd.delay_ms(5000)

            
        self.epd.Clear(0xff, 0xff)
        self.epd.delay_ms(2000)
        print("sleep")
        self.epd.sleep()
    
    async def epdclear(self):
        # Clear the eink display
        print("Clear eink display")
        self.epd.Clear(0xff, 0xff)
    
    async def epdsleep(self):
        # Put the eink display to sleep
        print("Sleep eink display")
        self.epd.sleep()    
  
    async def writetext(self, text: list):
        # Write text to the eink display
        print("Write text to eink display")
        # self.epd.Clear(0xff, 0xff)
        self.epd.imageblack.fill(0xff)
        self.epd.imagered.fill(0xff)
        # Loop through the text dictionary
        for line in text:
            # Check if the line is red or black
            print(line["text"])
            if line["colour"] == "red":
                self.epd.imagered.text(line["text"], line["x"], line["y"], color=0x00, size=line["size"])
            else:
                self.epd.imageblack.text(line["text"], line["x"], line["y"], color=0x00, size=line["size"])
        self.epd.display()
        self.epd.delay_ms(2000)