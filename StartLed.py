#! /usr/bin/python3

import sys
from time import sleep
import pifacedigitalio
from StartLedArgumentParser import StartLedArgumentParser

class StartLed :
    flashSpeedLimit = None
    pfio = pifacedigitalio.PiFaceDigital()
    piFaceListener = None
    toggleValue = None
    flashSpeed = None
    startLedPin = None
    flashStop = None
    highSpeed = None
    lowSpeed = None
    
    def __init__(self, args = dict()) :
        pifacedigitalio.init()
        self.startListener(self)
        self.startLed(self, args)

    
    def startListener(self) :
        self.piFaceListener = pifacedigitalio.InputEventListener(chip = self.pfio)
        self.piFaceListener.register(0, pifacedigitalio.IODIR_BOTH, self.listenerCallback(self))
        self.piFaceListener.activate()

    def listenerCallback(self) :
        pass

    def startLed(self, args = dict()) :
        self.setFlashProperties(self, args)
        self.flashLed(self)
        self.close(self)

    def transformFlashLedArgsInput(self) :
        self.startLedPin = int(input("LED number: "))
        self.toggleValue = int(input("Toggle on (1) or off (0): "))
        if self.toggleValue == 1 :
            self.flashSpeed = int(input("Set flash speed (1-10): "))
            self.flashStop = False
        else :
            self.flashSpeed = 0
            self.flashStop = True

    def transformFlashLedArgumentsMain(self, args) :
        if not args.speed and not args.stop :
            args.stop = True
        self.toggleValue = args.toggle
        self.flashSpeed = args.speed
        self.startLedPin = args.led
        self.flashStop = args.stop

    def toggleLed(self) :
        #this is the non-oop way
        #pifacedigitalio.digital_write(pin, i)
        #output_pins and leds seem to be the same array, leds has methods
        #self.pfio.output_pins[pin].value = i
        if self.toggleValue == 0 :
            self.pfio.leds[self.startLedPin].turn_off()
        else :
            self.pfio.leds[self.startLedPin].turn_on()
            self.pfio.leds[self.startLedPin].set_high()

    def setFlashProperties(self, args = dict()) :
        self.setFlashSpeedProperties(self, args)
        self.setSleepTime(self)

    def setFlashSpeedProperties(self, args = dict()) :
        self.setFlashSpeedLimit(self)
        self.setFlashHighSpeed(self)
        self.setFlashLowSpeed(self)
        if not args :
            self.transformFlashLedArgsInput(self)
        else :
            self.transformFlashLedArgsMain(self, args)
        self.transformFlashSpeed(self)

    def setFlashHighSpeed(self) :
        self.highSpeed = self.flashSpeedLimit - 1

    def setFlashLowSpeed(self) :
        self.lowSpeed = 1

    def setFlashSpeedLimit(self) :
        self.flashSpeedLimit = 11

    def transformFlashSpeed(self) :
        if self.flashSpeed > self.highSpeed :
            self.flashSpeed = self.highSpeed
        elif self.flashSpeed < self.lowSpeed :
            self.flashSpeed = self.lowSpeed

    def setSleepTime(self) :
        self.sleepTime = self.flashSpeedLimit - self.flashSpeed

    def flashLed(self) :
        self.toggleLed(self)
        if self.flashStop :
            return
        sleep(self.sleepTime)
        self.flipToggle(self)
        self.flashLed(self)

    def flipToggle(self) :
        if self.toggleValue == 1 :
            self.toggleValue = 0
        else :
            self.toggleValue = 1
    
    def readInput(self) :
        #pifacedigitalio.digital_read(0)
        print(se1f.pfio.output_pins[self.startLedPin].value)

    def togglePinPullups(self, pinNumber, pinState) :
        digital_write_pullup(pinNumber, pinState)

    def close(self) :
        self.pfio.deinit_board()

    def shutOffAllLeds(self) :
        self.pfio.output_port.all_off()


def main() :
    try :
        args_dict = StartLedArgumentParser.getArgsDict(StartLedArgumentParser)
        startled = StartLed
        startled.startLed(startled, args_dict)
    except pifacedigitalio.core.NoPiFaceDigitalError as e :
        excinfo = sys.exc_info()
        print (e, excinfo.tb_lineno)
        sys.exit(1)
    except KeyboardInterrupt as ki :
        startled.startLed(startled, args_dict)
    except ImportError as e:
        print (e)
        sys.exit(1)
    

if __name__ == '__main__' : main()




    

