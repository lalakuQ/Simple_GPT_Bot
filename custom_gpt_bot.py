import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart, StateFilter, Text
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
import requests
import uuid
import os
import json
from lang_pack.lang import lang
from dotenv import load_dotenv
from keyboard.keyboards import kbs
import sys



logging.basicConfig(level = logging.INFO)


bot = Bot(token=os.getenv('BOT_TOKEN'))
custom_gpt_key = os.getenv('CUSTOM_GPT_KEY')

users = {}
message_default = None
temp_dict = {}
dp = Dispatcher(bot=bot)


class FSM(StatesGroup):
    settings_menu = State()
    main_menu = State()
    wait_for_prompt = State()
    dialogue_created = State()
    lang_pick = State()
    dialogue_mode = State()
    ask_create_dialogue = State()


command_list = ['/start', '/settings']
yes_list = [lang['yes_ru'], lang['yes_en']]
settings_list = [lang['settings_en'], lang['settings_ru']]
back_list = [lang['back_ru'], lang['back_en']]

create_conv_list = [lang['create_conv_en'], lang['create_conv_ru'], lang['create_conv_en'], lang['create_conv_ru']]
delete_conv_list = [lang['delete_conv_ru'], lang['delete_conv_en']]

no_list = [lang['no_ru'], lang['no_en']]
choice_lang_list = [lang['choice_lang_ru'], lang['choice_lang_en']]
choose_lang_list = [lang['choose_lang_en'], lang['choose_lang_ru']]


@dp.message(Text(text=back_list))
async def temp(message: Message):
    await message.answer('Недоступно')


def lang_choice(chat_id):
    with open(f'{chat_id}.json', 'r') as file:
        temp_dict = json.load(file)
    if temp_dict['lang'] == 'ru':
        return 'ru'
    else:
        return 'en'


async def set_main_menu(bot: Bot):
    main_menu_commands = [
        BotCommand(command='/start',
                   description='Restart bot'),
        BotCommand(command='/settings',
                   description='Settings')]

    await bot.set_my_commands(main_menu_commands)


async def start_polling(bot: Bot):
    @dp.message(Command(commands='start'))
    async def start_command(message: Message):
        await message.answer(lang['choose_lang_en'], reply_markup=kbs['general']['choice_lang_kb'])
        if not os.path.exists(f'{message.from_user.id}.json'):
            with open(f'{message.from_user.id}.json', 'w') as file:
                users = {'conversations': [], 'curr_conver_id': None, 'lang': None, 'current_state': None}
                json.dump(users, file)

    @dp.message(Text(text=settings_list))
    async def settings(message: Message):
        chosen_lang = lang_choice(message.from_user.id)
        await message.answer(lang[f'settings_{chosen_lang}'], reply_markup=kbs[chosen_lang]['cfg_kb'])

    @dp.message(Text(text=delete_conv_list))
    async def test(message: Message):
        await message.answer('Недоступно')

    @dp.message(Text(text=choose_lang_list))
    async def choose_lang(message: Message):
        chosen_lang = lang_choice(message.from_user.id)
        await message.answer(lang[f'choose_lang_{chosen_lang}'], reply_markup=kbs[chosen_lang]['choice_lang_kb'])

    @dp.message(Text(text=choice_lang_list))
    async def chosen_lang(message: Message):
        with open(f'{message.from_user.id}.json', 'w') as file:
            if message.text == '🇷🇺Русский':
                await message.answer(lang['welcome_ru'], reply_markup=kbs['ru']['main_menu_kb'])
                users = {'conversations': [], 'curr_conver_id': None, 'dialogue_mode': False, 'lang': 'ru'}
                json.dump(users, file)

            else:
                await message.answer(lang['welcome_en'], reply_markup=kbs['en']['main_menu_kb'])
                users = {'conversations': [], 'curr_conver_id': None, 'dialogue_mode': False, 'lang': 'en'}
                json.dump(users, file)

    @dp.message(Text(text=create_conv_list))
    async def create_conversation(message: Message):
        chosen_lang = lang_choice(message.from_user.id)
        await message.answer(lang[f'create_{chosen_lang}'], reply_markup=kbs[chosen_lang]['main_menu_kb'])
        global temp_dict
        random_number = uuid.uuid4()
        conver_name = f'{message.from_user.id}-{random_number}'
        url = "https://app.customgpt.ai/api/v1/projects/4800/conversations"
        payload = {"name": f'{conver_name}'}
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": custom_gpt_key}

        response = requests.post(url, json=payload, headers=headers)
        response_data = response.json()
        session_id = response_data['data']['session_id']
        with open(f'{message.from_user.id}.json', 'r') as file:
            temp_dict = json.load(file)

        temp_dict['conversations'].append(session_id)
        temp_dict['curr_conver_id'] = session_id
        temp_dict['dialogue_mode'] = True

        with open(f'{message.from_user.id}.json', 'w') as file:
            json.dump(temp_dict, file)

    @dp.message(Text(text=no_list))
    async def button_no(message: Message):
        chosen_lang = lang_choice(message.from_user.id)
        await message.reply(lang[f'ok_{chosen_lang}'], reply_markup=kbs[chosen_lang]['main_menu_kb'])

    @dp.message()
    async def process_res(message: Message):
        chosen_lang = lang_choice(message.from_user.id)
        with open(f'{message.from_user.id}.json', 'r') as file:
            users = json.load(file)
        if users['dialogue_mode'] == False:
            await message.answer(lang[f'question_{chosen_lang}'], reply_markup=kbs[chosen_lang]['choice_kb'])
        else:
            message_default = await message.answer(lang[f'request_default_{chosen_lang}'])
            curr_conver_id = users['curr_conver_id']
            user_text = message.text
            url = f'https://app.customgpt.ai/api/v1/projects/4800/conversations/{curr_conver_id}/messages?stream=false&lang=ru'
            payload = {"prompt": user_text}
            headers = {
                "accept": "application/json",
                "content-type": "application/json",
                "authorization": custom_gpt_key}
            response = requests.post(url, json=payload, headers=headers)
            response_text = response.json()
            await message_default.delete()

            if 'openai_response' in response_text['data']:
                await message.reply(response_text['data']['openai_response'])
            else:
                response_error = response_text['data']['message']
                await message.reply(lang[f'error_{chosen_lang}'] + response_error)

    await set_main_menu(bot)
    await bot.start_polling()

if __name__ == '__main__':
    dp.startup.register(set_main_menu)
    dp.run_polling(bot)
