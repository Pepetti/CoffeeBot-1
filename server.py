from bot import telegram_chatbot
from hx711 import HX711
import RPi.GPIO as GPIO
import configparser
import datetime
import sys

#GPIO cleanup and setting warnings to false in case the script is started after a crash
GPIO.setwarnings(False)
GPIO.cleanup()

#Bot setup
update_id = None
config = "config.ini"
bot = telegram_chatbot(config)

#Parser setup
parser = configparser.SafeConfigParser()

#Scale setup
hx = HX711(5, 6)
hx.set_reading_format("LSB", "MSB")
hx.set_reference_unit(1509)
hx.reset()
hx.tare()

#Cleanup and exit on KeyboardInterrupt
def cleanAndExit():
    GPIO.cleanup()
    sys.exit()

#Scale reset and hard reset (resets the calibration)
def scale_reset():
    hx.reset()
    hx.tare()

def scale_hard_reset(config):
    parser.read(config)
    parser.set('creds', 'weight', '0')
    with open('config.ini', 'w') as configfile:
        parser.write(configfile)
    hx.reset()
    hx.tare()

#Scale calibration
def scale_calibrate(config, val):
    parser.read(config)
    val = str(val)
    parser.set('creds', 'weight', val)
    with open('config.ini', 'w') as configfile:
        parser.write(configfile)

def get_pot_weight(config):
    parser.read(config)
    val = parser.getint('creds', 'weight')
    return val

#Get timestamp
def get_timestamp():
    date = datetime.datetime.now()
    day = date.strftime("%d")
    month = date.strftime("%m")
    year = date.strftime("%y")
    hour = date.strftime("%H")
    minute = date.strftime("%M")
    timestamp = "[{}/{}/{} {}:{}]".format(day, month, year, hour, minute)
    return timestamp

#Parse incoming message for return ID and shave @ characters from the sendMessage, i want to die btw
def parse_incoming_message(updates):
    if item["message"]["chat"]["type"] == "private":
        message = item["message"]["text"]
        if "@" in message:
            message = message.split("@")
            message = message[0]
        from_ = item["message"]["from"]["id"]
        reply = make_reply(message)
        return reply, from_
    elif item["message"]["chat"]["type"] == "group" or item["message"]["chat"]["type"] == "supergroup":
        message = item["message"]["text"]
        if "@" in message:
            message = message.split("@")
            message = message[0]
        from_ = item["message"]["chat"]["id"]
        reply = "Group commands have been disabled for now.."
        return reply, from_

#Get values necessary for the reply (weight on scale, pot configuration, timestamp, dl, cups)
def get_values(config):
    pot_weight = get_pot_weight(config)
    val = max(0, int(hx.get_weight(5))) - pot_weight
    timestamp = get_timestamp()
    dl = val / 100.00
    cups = dl / 2
    return pot_weight, val, timestamp, dl, cups

#Commands available
commands = ["/start", "/help", "/coffee", "/calibrate", "/calibhelp", "/hreset", "/reset", "/aa"]

#Making the reply message according to user message
def make_reply(msg):
    if msg is not None:
        pot_weight, val, timestamp, dl, cups = get_values(config)

        if msg == "/start" or msg == "/help":
            reply = """{}\nThe basic commands for the bot are:\n /coffee --> Tells you how much coffee there is.\n /help --> Shows you this message
/reset --> Resets the scale (tare)\n/hreset --> Does a hard reset to the scale. !IF YOU DO THIS YOU HAVE TO CALIBRATE THE SCALE AGAIN!
/calibrate --> Calibrates the scale\n/calibhelp --> Help on calibration""".format(timestamp)

        elif msg == "/reset":
            scale_reset()
            reply = "{}\nReset done, replace the pot on the scale.".format(timestamp)

        elif msg == "/hreset":
            scale_hard_reset(config)
            reply = "{}\nHard reset done. You have to redo the calibration for the scale. Information on how to do the calibration type command /calibhelp.".format(timestamp)

        elif msg == "/calibrate":
            reply = "{}\nCalibration done. The weight of the pot is {} grams.".format(timestamp, val)
            scale_calibrate(config, val)

        elif msg == "/calibhelp":
            reply = """{}\nTo calibrate the scale, first send the /reset command to the bot and then place an empty pot on the scale.
After this send the /calibrate message to the bot. After this the scale is calibrated.""".format(timestamp)

        elif msg == "/coffee":
            if cups <= 0:
                reply = "{}\nThere is no coffee in the pot, or the scale system needs a reset. Go check the situation!".format(timestamp)
            elif cups > 0:
                reply = "{}\nThere is approximately {} cups of coffee in the pot ({}dl).".format(timestamp, cups, dl)

        elif msg == "/aa":
            test_pot_weight = get_pot_weight(config)
            reply = "{}\nPot weight in config.ini file at the moment is: {}.".format(timestamp, test_pot_weight)

        elif msg not in commands:
            reply = "{}\nNot a valid command. Use command /help to see all available commands.".format(timestamp)

        #elif msg == "/sub":
            #TODO: Subscribe system to get a notification when there is fresh coffee brewing MAYBE LATER OR SOMETHING

    elif msg == None:
        timestamp = get_timestamp()
        reply = "{}\nYour message appeared to be empty. Please try again. (use command /help for available commands)".format(timestamp)

    return reply

#Infinite loop to run the bot while the pi is on
while True:
    try:
        print "###"
        updates = bot.get_updates(offset=update_id)
        updates = updates["result"]
        if updates:
            for item in updates:
                update_id = item["update_id"]
                try:
                    reply, from_ = parse_incoming_message(updates)
                    bot.send_message(reply, from_)
                except:
                    message = None
    except(KeyboardInterrupt, SystemExit):
        cleanAndExit()
