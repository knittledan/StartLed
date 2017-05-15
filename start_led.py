#! /usr/bin/python3

import sys
from time import sleep
import pifacedigitalio
from start_led_argument_parser import StartLedArgumentParser

class StartLed :
    flashSpeedLimit = None
    pfio = pifacedigitalio.PiFaceDigital()
    piFaceListener = None
    toggle_value = None
    flash_speed = None
    start_led_pin = None
    flash_stop = None
    highSpeed = None
    lowSpeed = None

    def __init__(self, args: dict):
        pifacedigitalio.init()
        self.start_listener()
        self.start_led(args)

    def start_listener(self) :
        self.piFaceListener = pifacedigitalio.InputEventListener(chip = self.pfio)
        self.piFaceListener.register(0, pifacedigitalio.IODIR_BOTH, self.listenerCallback())
        self.piFaceListener.activate()

    def listenerCallback(self) :
        pass

    def start_led(self, args: dict) :
        self.setFlashProperties(args)
        self.flashLed()
        self.close()

    def transform_flash_led_args_input(self) :
        self.start_led_pin = int(input("LED number: "))
        self.toggle_value = int(input("Toggle on (1) or off (0): "))
        if self.toggle_value == 1 :
            self.flash_speed = int(input("Set flash speed (1-10): "))
            self.flash_stop = False
        else :
            self.flash_speed = 0
            self.flash_stop = True

    def transform_flash_led_arguments_main(self, args: dict) :
        if not args.speed and not args.stop :
            args.stop = True
        self.toggle_value = args.toggle
        self.flash_speed = args.speed
        self.start_led_pin = args.led
        self.flash_stop = args.stop

    def toggleLed(self) :
        #this is the non-oop way
        #pifacedigitalio.digital_write(pin, i)
        #output_pins and leds seem to be the same array, leds has methods
        #self.pfio.output_pins[pin].value = i
        if self.toggle_value == 0 :
            self.pfio.leds[self.start_led_pin].turn_off()
        else :
            self.pfio.leds[self.start_led_pin].turn_on()
            self.pfio.leds[self.start_led_pin].set_high()

    def setFlashProperties(self, args: dict) :
        self.setFlashSpeedProperties(args)
        self.setSleepTime()

    def setFlashSpeedProperties(self, args: dict) :
        self.setFlashSpeedLimit()
        self.setFlashHighSpeed()
        self.setFlashLowSpeed()
        if not args :
            self.transform_flash_led_args_input()
        else :
            self.transformFlashLedArgsMain(self, args)
        self.transformFlashSpeed()

    def setFlashHighSpeed(self) :
        self.highSpeed = self.flashSpeedLimit - 1

    def setFlashLowSpeed(self) :
        self.lowSpeed = 1

    def setFlashSpeedLimit(self) :
        self.flashSpeedLimit = 11

    def transformFlashSpeed(self) :
        if self.flash_speed > self.highSpeed :
            self.flash_speed = self.highSpeed
        elif self.flash_speed < self.lowSpeed :
            self.flash_speed = self.lowSpeed

    def setSleepTime(self) :
        self.sleepTime = self.flashSpeedLimit - self.flash_speed

    def flashLed(self) :
        self.toggleLed()
        if self.flash_stop :
            return
        sleep(self.sleepTime)
        self.flipToggle()
        self.flashLed()

    def flipToggle(self) :
        if self.toggle_value == 1 :
            self.toggle_value = 0
        else :
            self.toggle_value = 1

    def readInput(self) :
        #pifacedigitalio.digital_read(0)
        print(self.pfio.output_pins[self.start_led_pin].value)

    def togglePinPullups(self, pinNumber, pinState) :
        digital_write_pullup(pinNumber, pinState)

    def close(self) :
        self.pfio.deinit_board()

    def shutOffAllLeds(self) :
        self.pfio.output_port.all_off()


def main() :
    try :
        args_dict = StartLedArgumentParser().args_dict
        startled = StartLed
        startled.start_led(startled, args_dict)
    except pifacedigitalio.core.NoPiFaceDigitalError as e :
        excinfo = sys.exc_info()
        print (e, excinfo.tb_lineno)
        sys.exit(1)
    except KeyboardInterrupt as ki:
        startled.start_led(startled, args_dict)
    except ImportError as e:
        print (e)
        sys.exit(1)


if __name__ == '__main__' :
    main()






