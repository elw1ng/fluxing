
import telebot


class Telega:

    def __init__(self, user1_id="", user2_id="", token="", debug_mode=True):
        self.USER1_ID = user1_id
        self.USER2_ID = user2_id
        self.TOKEN = token
        self.bot = telebot.TeleBot(self.TOKEN)
        self.debug_mode = debug_mode

    def _debug(self, value: str, debug_show=True):
        if self.debug_mode:
            if debug_show:
                print(f"TELEGA DEBUG: {value}")
            else:
                print(value)

    def send_message(self, text):
        if self.USER1_ID != "":
            self.bot.send_message(self.USER1_ID, f"RTX3080: {text}")
        if self.USER2_ID != "":
            self.bot.send_message(self.USER2_ID, f"RTX3080: {text}")
        self._debug(text)


if __name__ == "__main__":

    from jsonOper import loadKeysTelega, saveKeysTelega


    data_keys = loadKeysTelega()

    token = data_keys["fluxing"]["key19"]["value"]

    bot = telebot.TeleBot(token)

    @bot.message_handler(content_types=['text'])
    def get_text_messages(message):

        bot.send_message(message.from_user.id, f"Ваш ID: {message.from_user.id}")
        print(f"Ваш user_id: {message.from_user.id}")

        if data_keys["fluxing"]["key17"]["value"] == "":
            data_keys["fluxing"]["key17"]["value"] = message.from_user.id
        elif data_keys["fluxing"]["key18"]["value"] == "":
            data_keys["fluxing"]["key18"]["value"] = message.from_user.id

        saveKeysTelega(data_keys)
        exit(0)


    bot.polling(none_stop=True, interval=0)


