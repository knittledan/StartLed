#! /usr/bin/python3

import argparse

class StartLedArgumentParser :
    parser = None
    args = None
    args_dict = dict()

    def __init__(self) :
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('-l', '--led', action = "store", default = None)
        self.parser.add_argument('-t', '--toggle', action = "store_true", default = False)
        self.parser.add_argument('-s', '--speed', action = "store", default = None)
        self.parser.add_argument('-x', '--stop', action = "store_true", default = False)

        self.setArgs(self)
        self.setArgsDict(self)
        

    def setArgs(self) :
        self.args = self.parser.parse_args()

    def setArgsDict(self) :
        self.args_dict = vars(self.args)

    def getArgs(self) :
        return self.args

    def getArgsDict(self) :
        return self.args_dict
