import requests
import aiogram


import os
import json
import time
import subprocess
from multiprocessing import Process
import asyncio

from aiogram import Bot, Dispatcher, executor, types

from config import TG_TOKEN, API_LINK, UPDATE_PERIOD, low_models, large_models, \
    inline_kb, inline_kb_models_size_show, inline_kb_low_models_show, \
    inline_kb_large_models_show, inline_kb_models_size_start, \
    inline_kb_low_models_start, inline_kb_large_models_start, inline_kb_mode

import utils




# bot or run
loop = asyncio.get_event_loop()
bot = Bot(TG_TOKEN)
dp = Dispatcher(bot, loop=loop)



@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    utils.add_chat(message.chat.id)
    await bot.send_message(message.chat.id, 'Choose action', reply_markup=inline_kb)

# Mode
@dp.callback_query_handler(lambda c: c.data == 'button_mode')
async def process_callback_show(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Set mode', reply_markup=inline_kb_mode)

@dp.callback_query_handler(lambda c: c.data == 'button_manual')
async def process_callback_model_show_cur(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    utils.set_mode("manual")
    await bot.send_message(callback_query.from_user.id, 'Choose action', reply_markup=inline_kb)

@dp.callback_query_handler(lambda c: c.data == 'button_auto_restart')
async def process_callback_model_show_cur(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    utils.set_mode("auto")
    await bot.send_message(callback_query.from_user.id, 'Choose action', reply_markup=inline_kb)



# Show
@dp.callback_query_handler(lambda c: c.data == 'button_show')
async def process_callback_show(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Choose model size', reply_markup=inline_kb_models_size_show)


@dp.callback_query_handler(lambda c: c.data == 'button_large_show')
async def process_callback_model_large_show(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Choose large model', reply_markup=inline_kb_large_models_show)

@dp.callback_query_handler(lambda c: c.data == 'button_low_show')
async def process_callback_model_low_show(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Choose low model', reply_markup=inline_kb_low_models_show)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('dtln') and c.data.endswith('show'))
async def process_callback_model_show_cur(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text=utils.show_epoch_metrics(callback_query.data[:-4]))
    await bot.send_message(callback_query.from_user.id, 'Choose action', reply_markup=inline_kb)



# Start
@dp.callback_query_handler(lambda c: c.data == 'button_start')
async def process_callback_model_start(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Choose model size', reply_markup=inline_kb_models_size_start)

@dp.callback_query_handler(lambda c: c.data == 'button_large_start')
async def process_callback_model_large_start(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Choose large model', reply_markup=inline_kb_large_models_start)

@dp.callback_query_handler(lambda c: c.data == 'button_low_start')
async def process_callback_model_low_start(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Choose low model', reply_markup=inline_kb_low_models_start)

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('dtln') and c.data.endswith('start'))
async def process_callback_model_start_cur(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    message_handle = Process(target=utils.start_train, args=(callback_query.data[:-5],))
    message_handle.start()
    await bot.send_message(callback_query.from_user.id, text=f"Started train {callback_query.data[:-5]}")
    await bot.send_message(callback_query.from_user.id, 'Choose action', reply_markup=inline_kb)




def get_exception():
    try:
        while True:
            time.sleep(UPDATE_PERIOD)
            # writting exceptions
            with open("./bot_logs.json", "r") as f: # fix
                json_ = json.load(f)

            if json_["error"]:
                if json_["mode"] == "auto" and json_["cur_model"] != "":
                    message_handle = Process(target=utils.start_train, args=(json_["cur_model"],))
                    message_handle.start()

                chats = utils.get_chats()
                if chats:
                    for chat in chats:
                        _ = requests.get(API_LINK + f"sendMessage?chat_id={chat}&text={json_['error']}")
                        if json_["mode"] == "auto" and json_["cur_model"] != "":
                            _ = requests.get(API_LINK + f"sendMessage?chat_id={chat}&text=Train restarted")


                json_['error'] = 0
                with open("./bot_logs.json", "w") as f: # fix
                    json.dump(json_, f)

    except KeyboardInterrupt as e:
        with open("./bot_logs.json", "r") as f:  # fix
            json_ = json.load(f)
        json_["cur_model"] = ""
        with open("./bot_logs.json", "w") as f:  # fix
            json.dump(json_, f)




def main():

    message_handle = Process(target=executor.start_polling, args=(dp, ))
    exception_catcher = Process(target=get_exception)

    message_handle.start()
    exception_catcher.start()

    message_handle.join()
    exception_catcher.join()

if __name__ == '__main__':
    main()