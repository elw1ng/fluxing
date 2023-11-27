
import telebot


class Telega:

    def __init__(self, user_id, token, debug_mode=True):
        self.USER_ID = user_id
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

        self.bot.send_message(self.USER_ID, text)
        self._debug(text)


if __name__ == "__main__":

    from jsonOper import loadKeysTelega, saveKeysTelega


    data_keys = loadKeysTelega()

    token = data_keys["fluxing"]["key18"]["value"]

    bot = telebot.TeleBot(token)

    @bot.message_handler(content_types=['text'])
    def get_text_messages(message):

        bot.send_message(message.from_user.id, f"Ваш ID: {message.from_user.id}")
        print(f"Ваш user_id: {message.from_user.id}")
        data_keys["fluxing"]["key17"]["value"] = message.from_user.id
        saveKeysTelega(data_keys)
        exit(0)


    bot.polling(none_stop=True, interval=0)


