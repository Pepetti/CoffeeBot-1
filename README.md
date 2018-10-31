# CoffeeBot
A telegram bot that tells you how much coffee there is in a pot.

## Basic structure and wiring
The hardware consists of a ![kitchen scale](https://www.power.fi/keittio-ja-ruoanlaitto/keittion-pienkoneet/keittiovaaat/senz-se3830h05-keittiovaaka/p-231191/), ![HX711 24-bit ADC](https://www.amazon.com/DIYmall-Weighing-Conversion-Sensors-Microcontroller/dp/B010FG9RXO) and a ![raspberry pi](https://www.amazon.com/Raspberry-Pi-MS-004-00000024-Model-Board/dp/B01LPLPBS8/ref=sr_1_6?s=pc&ie=UTF8&qid=1541001456&sr=1-6&keywords=raspberry+pi+3).

### Wiring
If you decide to use a kitchen scale for this bot, you might have to do a bit of soldering. Solder the wires coming from the scales weight sensors to a female jumper wire.
The wire coloring from the weight sensors or kitchen scales may vary but usually the colors are straightforward. The wiring from the sensor to the HX711 goes as follows:
- Red --> E+
- Black --> E-
- Green --> A-
- White --> A+ (This wire might be different in color, for example in this case it was yellow)

From the HX711 to the pi, the wiring is pretty straightforward:
- VCC to raspi pin 2 (5V)
- GND to raspi pin 6 (GND)
- DT to raspi pin 29 (GPIO 5)
- SCK to raspi pin 31 (GPIO 6)

## HX711
This bot uses the ![HX711 library](https://github.com/bogde/HX711) by Bogde.
On how to use the library in question, use the example.py file and the readme provided in the library.

## Usage
Create your own telegram bot with the instructions from ![Telegram](https://core.telegram.org/bots).
Clone or download the files from this repository to your raspi. Calibrate the HX711 with instructions from ![bodge](https://github.com/bogde/HX711). After you have your reference unit, open up the server.py file and set it to hx.set_reference_unit(your_reference_unit) (on line 23). After this create a config.ini file to your directory containing the python files. Construct it as shown in the image below:
<br><img src="https://github.com/oskarikotajarvi/CoffeeBot/blob/master/photosForReadme/configSH.png" width="600" height="500">

The "weight" in the config file is used to store calibrated weight of the coffee pot so the calibration doesn't have to be done everytime the raspi reboots.
After this run the server.py file and everything should be working! Start chatting with your bot! To see available commands for the bot and what they do use command /help.
