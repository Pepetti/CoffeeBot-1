import requests
import json
import configparser


class telegram_chatbot():

    '''
    Bot initialization. Pulls the bot API token from the config.ini file
    '''
    def __init__(self, config):
        self.token = self.read_token_from_config_file(config)
        self.base = "https://api.telegram.org/bot{}/".format(self.token)

    '''
    Bot updates. Timeout is set to 100 seconds, if updates are not given to the bot inside that time,
    new timeout will be started
    '''
    def get_updates(self, offset=None, r=None):
        url = self.base + "getUpdates?timeout=100"
        if offset:
            url = url + "&offset={}".format(offset + 1)
        try:
            r = requests.get(url)
        except requests.exceptions.ConnectionError as e:
            print e
            pass
        except requests.exceptions.Timeout as e:
            print e
            pass
        except UnboundLocalError as e:
            print e
            r = requests.get(url)
        return json.loads(r.content)

    '''
    Sends a message back to the proper user / group
    '''
    def send_message(self, msg, chat_id):
        url = self.base + "sendMessage?chat_id={}&text={}".format(chat_id, msg)
        if msg is not None:
            requests.get(url)

    '''
    Reads the bot API token from the config.ini file
    '''
    def read_token_from_config_file(self, config):
        parser = configparser.SafeConfigParser()
        parser.read(config)
        return parser.get('creds', 'token')
