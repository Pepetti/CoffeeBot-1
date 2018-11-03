from hx711 import HX711
import configparser
import sys

class Scale():

    def __init__(self, pin1, pin2, reference_unit):
        self.hx = HX711(pin1, pin2)
        self.hx.set_reading_format("LSB", "MSB")
        self.hx.set_reference_unit(reference_unit)
        self.hx.reset()
        self.hx.tare()
        self.parser = configparser.SafeConfigParser()

    def calibrate(self, config, val):
        self.parser.read(config)
        val = str(val)
        self.parser.set('creds', 'weight', val)
        with open('config.ini', 'w') as configfile:
            self.parser.write(configfile)

    def reset(self):
        self.hx.reset()
        self.hx.tare()

    def hard_reset(self, config):
        self.parser.read(config)
        self.parser.set('creds', 'weight', '0')
        with open('config.ini', 'w') as configfile:
            self.parser.write(configfile)
        self.hx.reset()
        self.hx.tare()

    def get_pot_weight(self, config):
        self.parser.read(config)
        val = self.parser.getint('creds', 'weight')
        return val

    def get_values(self, config):
        pot_weight = self.get_pot_weight(config)
        val = max(0, int(self.hx.get_weight(5))) - pot_weight
        dl = val / 100.00
        cups = dl / 2
        return pot_weight, val, dl, cups
