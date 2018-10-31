import requests
import json
import configparser


class telegram_chatbot():

    def __init__(self, config):
        self.token = self.read_token_from_config_file(config)
        self.base = "https://api.telegram.org/bot{}/".format(self.token)

    def get_updates(self, offset=None):
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
        return json.loads(r.content)

    def send_message(self, msg, chat_id):
        url = self.base + "sendMessage?chat_id={}&text={}".format(chat_id, msg)
        if msg is not None:
            requests.get(url)

    def read_token_from_config_file(self, config):
        parser = configparser.SafeConfigParser()
        parser.read(config)
        return parser.get('creds', 'token')
