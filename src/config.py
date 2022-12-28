import aiogram


from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


TG_TOKEN = "5730981258:AAH7XtHAZo-HK5KRKh80NH9QPcC2P3IqUWs"
API_LINK = f"https://api.telegram.org/bot{TG_TOKEN}/"
UPDATE_PERIOD = 2



# Models
low_models = ["dtln_128_test_kd512", "dtln_simple_128_test_kd512"]
large_models = ["dtln_512_test", "dtln_simple_512_test"]




# Begin menu
inline_btn_1 = InlineKeyboardButton('Show', callback_data='button_show')
inline_btn_2 = InlineKeyboardButton('Start', callback_data='button_start')
inline_kb = InlineKeyboardMarkup().add(inline_btn_1).add(inline_btn_2)


# Models size show menu
inline_btn_large_show = InlineKeyboardButton('Large', callback_data='button_large_show')
inline_btn_low_show = InlineKeyboardButton('Low', callback_data='button_low_show')
inline_kb_models_size_show = InlineKeyboardMarkup().add(inline_btn_large_show).add(inline_btn_low_show)

# low Models show menu
inline_kb_low_models_show = InlineKeyboardMarkup()
for mod in low_models:
    inline_kb_low_models_show.add(InlineKeyboardButton(mod, callback_data=mod+"show"))

# large Models show menu
inline_kb_large_models_show = InlineKeyboardMarkup()
for mod in large_models:
    inline_kb_large_models_show.add(InlineKeyboardButton(mod, callback_data=mod+"show"))


# Models size start menu
inline_btn_large_start = InlineKeyboardButton('Large', callback_data='button_large_start')
inline_btn_low_start = InlineKeyboardButton('Low', callback_data='button_low_start')
inline_kb_models_size_start = InlineKeyboardMarkup().add(inline_btn_large_start).add(inline_btn_low_start)

# low Models start menu
inline_kb_low_models_start = InlineKeyboardMarkup()
for mod in low_models:
    inline_kb_low_models_start.add(InlineKeyboardButton(mod, callback_data=mod+"start"))

# large Models show menu
inline_kb_large_models_start = InlineKeyboardMarkup()
for mod in large_models:
    inline_kb_large_models_start.add(InlineKeyboardButton(mod, callback_data=mod+"start"))