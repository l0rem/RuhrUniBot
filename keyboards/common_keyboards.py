from telegram import ReplyKeyboardMarkup

main_menu_buttons = ['\U0001F371 Mensa', '\U0001F4D1 Schedule', '\U0001F4E2 Notifications', '\U0001F5FA Map',
                     '\U00002139 Help']

main_menu_keyboard = ReplyKeyboardMarkup(keyboard=[[main_menu_buttons[0], main_menu_buttons[1]],
                                                   [main_menu_buttons[2], main_menu_buttons[3]],
                                                   [main_menu_buttons[4]]],
                                         resize_keyboard=True,
                                         one_time_keyboard=True)

back_button = '\U000021A9 Back'

back_keyboard = ReplyKeyboardMarkup(keyboard=[[back_button]],
                                    resize_keyboard=True,
                                    one_time_keyboard=True)
