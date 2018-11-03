from hx711 import HX711
import configparser
import sys

class Scale():

    def __init__(self):
        self.hx = HX711(5, 6)
        self.hx.set_reading_format("LSB", "MSB")
        self.hx.set_reference_unit(1509)
        self.hx.reset()
        self.hx.tare()

    def calibrate(self, config, val):
        parser = configparser.SafeConfigParser()
        parser.read(config)
        val = str(val)
        parser.set('creds', 'weight', val)
        with open('config.ini', 'w') as configfile:
            parser.write(configfile)

    def reset(self):
        self.hx.reset()
        self.hx.tare()

    def hard_reset(self, config):
        parser = configparser.SafeConfigParser()
        parser.read(config)
        parser.set('creds', 'weight', '0')
        with open('config.ini', 'w') as configfile:
            parser.write(configfile)
        self.hx.reset()
        self.hx.tare()

    def get_pot_weight(self, config):
        parser = configparser.SafeConfigParser()
        parser.read(config)
        val = parser.getint('creds', 'weight')
        return val

    def get_values(self, config):
        pot_weight = self.get_pot_weight(config)
        val = max(0, int(self.hx.get_weight(5))) - pot_weight
        dl = val / 100.00
        cups = dl / 2
        return pot_weight, val, dl, cups
