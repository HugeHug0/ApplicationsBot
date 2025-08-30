from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from core.utils import text
from core.utils.text import buttons


def application_keyboard():
    return ReplyKeyboardMarkup(keyboard =
                               [
                                   [KeyboardButton(text=text.skip_btn)],
                                   [KeyboardButton(text=text.step_back_btn)],
                                   [KeyboardButton(text=text.home_btn)]
                                ],
                               resize_keyboard=True)

def start_application_keyboard():
    return ReplyKeyboardMarkup(keyboard =
                               [
                                   [KeyboardButton(text=text.start_application_btn)]
                               ],
                               resize_keyboard=True)

def name_application_keyboard(share_name_btn):
    return ReplyKeyboardMarkup(keyboard =
                               [
                                   [KeyboardButton(text=share_name_btn)],
                                   [KeyboardButton(text=text.step_back_btn)],
                                   [KeyboardButton(text=text.home_btn)]
                                ],
                               resize_keyboard=True)

def service_application_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(*[KeyboardButton(text=button) for button in buttons])
    builder.adjust(3)

    builder.row(KeyboardButton(text=text.step_back_btn),
                KeyboardButton(text=text.home_btn))

    kb = builder.as_markup(resize_keyboard=True)
    return kb

def contact_application_keyboard():
    return ReplyKeyboardMarkup(keyboard =
                               [
                                   [KeyboardButton(text=text.username_btn)],
                                   [KeyboardButton(text=text.phone_number_btn)],
                                   [KeyboardButton(text=text.step_back_btn)],
                                   [KeyboardButton(text=text.home_btn)]
                                ],
                               resize_keyboard=True)

def phone_number_application_keyboard():
    return ReplyKeyboardMarkup(keyboard =
                               [
                                   [KeyboardButton(text=text.share_phone_number_btn, request_contact=True)],
                                   [KeyboardButton(text=text.step_back_btn)],
                                   [KeyboardButton(text=text.home_btn)]
                                ],
                               resize_keyboard=True)

def confirm_application_keyboard():
    return ReplyKeyboardMarkup(keyboard =
                               [
                                   [KeyboardButton(text=text.confirm_application_btn)],
                                   [KeyboardButton(text=text.step_back_btn)],
                                   [KeyboardButton(text=text.home_btn)]
                                ],
                               resize_keyboard=True)
