from lang_pack.lang import lang
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

bts: dict = {

    'en': {
        'create_conv_button' : KeyboardButton(text = lang['create_conv_en']),
        'del_conv': KeyboardButton(text = lang['delete_conv_en']),
        'cfg' : KeyboardButton(text = lang['settings_en'] ),
        'button_yes':KeyboardButton(text = lang['yes_en']),
        'button_no' : KeyboardButton(text = lang['no_en']),
        'choice_en' : KeyboardButton(text = lang['choice_lang_en']),
        'cfg_1': KeyboardButton(text = lang['choose_lang_en']),
        'button_back': KeyboardButton(text = lang['back_en'])
       
     },

    'ru': {
        'create_conv_button' : KeyboardButton(text = lang['create_conv_ru']),
        'del_conv'  : KeyboardButton(text = lang['delete_conv_ru']),
        'cfg'  : KeyboardButton(text = lang['settings_ru'] ),
        'button_yes'  : KeyboardButton(text = lang['yes_ru']),
        'button_no'  : KeyboardButton(text = lang['no_ru']),
        'choice_ru'  : KeyboardButton(text = lang['choice_lang_ru']),
        'cfg_1': KeyboardButton(text = lang['choose_lang_ru']),
        'button_back': KeyboardButton(text = lang['back_ru'])
    }
}

