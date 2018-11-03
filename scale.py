from hx711 import HX711
import configparser

class Scale():

    '''
    Initialization for the scale class.
    Params:
            pin1, pin2 = GPIO pins the scale is hooked up to
            reference_unit = the reference unit got from calibrating the scale according to the hx711 library
    '''
    def __init__(self, pin1, pin2, reference_unit):
        self.hx = HX711(pin1, pin2)
        self.hx.set_reading_format("LSB", "MSB")
        self.hx.set_reference_unit(reference_unit)
        self.hx.reset()
        self.hx.tare()
        self.parser = configparser.SafeConfigParser()

    '''
    Scale calibration. Saves the value measured to the config file
    '''
    def calibrate(self, config, val):
        self.parser.read(config)
        val = str(val)
        self.parser.set('creds', 'weight', val)
        with open('config.ini', 'w') as configfile:
            self.parser.write(configfile)

    '''
    Scale reset
    '''
    def reset(self):
        self.hx.reset()
        self.hx.tare()

    '''
    Scale hard reset. Resets the scale and the configuration.
    '''
    def hard_reset(self, config):
        self.parser.read(config)
        self.parser.set('creds', 'weight', '0')
        with open('config.ini', 'w') as configfile:
            self.parser.write(configfile)
        self.hx.reset()
        self.hx.tare()

    '''
    Fetching the pot weight from the configfile.
    '''
    def get_pot_weight(self, config):
        self.parser.read(config)
        val = self.parser.getint('creds', 'weight')
        return val

    '''
    Returns all the values needed for the reply message
    Return:
            pot_weight = weight of the pot
            val = weight on the scale
            dl = desiliters of liquid in the pot
            cups = how many 2dl cups of liquid there is
    '''
    def get_values(self, config):
        pot_weight = self.get_pot_weight(config)
        val = max(0, int(self.hx.get_weight(5))) - pot_weight
        dl = val / 100.00
        cups = dl / 2
        return pot_weight, val, dl, cups
