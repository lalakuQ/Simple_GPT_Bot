from keyboard.buttons import bts
from aiogram.types import ReplyKeyboardMarkup

kbs: dict = {

    'general': {
        'choice_lang_kb': ReplyKeyboardMarkup(keyboard = [[bts['ru']['choice_ru'], bts['en']['choice_en']]], resize_keyboard = True),
        
    },

    'en': {
        'choice_lang_kb': ReplyKeyboardMarkup(keyboard = [[bts['ru']['choice_ru'], bts['en']['choice_en']], [bts['en']['button_back']]], resize_keyboard = True),
        'main_menu_kb': ReplyKeyboardMarkup(keyboard = [[bts['en']['create_conv_button'], bts['en']['del_conv']], [bts['en']['cfg']]], resize_keyboard = True),
        'choice_kb': ReplyKeyboardMarkup(keyboard = [[bts['en']['button_yes'], bts['en']['button_no']], [bts['en']['button_back']]], resize_keyboard = True),
        'cfg_kb': ReplyKeyboardMarkup(keyboard = [[bts['en']['cfg_1']], [bts['en']['button_back']]], resize_keyboard = True)

    },

    'ru': {
        'choice_lang_kb': ReplyKeyboardMarkup(keyboard = [[bts['ru']['choice_ru'], bts['en']['choice_en']], [bts['en']['button_back']]], resize_keyboard = True),
        'main_menu_kb': ReplyKeyboardMarkup(keyboard = [[bts['ru']['create_conv_button'], bts['ru']['del_conv']], [bts['ru']['cfg']]], resize_keyboard = True),
        'choice_kb': ReplyKeyboardMarkup(keyboard = [[bts['ru']['button_yes'], bts['ru']['button_no']], [bts['ru']['button_back']]], resize_keyboard = True),
        'cfg_kb': ReplyKeyboardMarkup(keyboard = [[bts['ru']['cfg_1']],[bts['ru']['button_back']]], resize_keyboard = True)
    }

}