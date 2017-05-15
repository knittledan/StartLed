#! /usr/bin/python3

import argparse


class StartLedArgumentParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('-l', '--led', action="store", default=None)
        self.parser.add_argument('-t', '--toggle', action="store_true",
                                 default=False)
        self.parser.add_argument('-s', '--speed', action="store", default=None)
        self.parser.add_argument('-x', '--stop', action="store_true",
                                 default=False)

    @property
    def args(self):
        return self.parser.parse_args()

    @property
    def args_dict(self):
        return vars(self.args)
