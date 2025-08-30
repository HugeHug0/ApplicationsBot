from aiogram import Bot, Router, F
from aiogram.types import Message

from core.keyboards.reply_keyboards import name_application_keyboard, service_application_keyboard, \
    application_keyboard, contact_application_keyboard, phone_number_application_keyboard, confirm_application_keyboard, \
    start_application_keyboard
from core.services.application_service import ApplicationService
from core.utils import commands
from core.settings import settings
from aiogram.fsm.context import FSMContext

from core.utils.fsm_forms import ApplicationForm
from core.utils.text import name_application_message, start_application_btn, service_application_message, \
    details_application_message, file_application_message, contact_application_message, skip_btn, home_btn, \
    step_back_btn, phone_number_btn, username_btn, no_username_message, buttons, is_not_file_message, \
    phone_number_message, invalid_phone_number, final_application_message, confirm_application_btn
from core.utils.utils import final_application, is_phone_number

router = Router()

@router.startup()
async def start_bot_handler(bot: Bot):
        await commands.set_commands(bot)
        await bot.send_message(settings.bots.admin_id, 'Бот запущен')


@router.shutdown()
async def stop_bot_handler(bot: Bot):
    await bot.send_message(settings.bots.admin_id, 'Бот остановлен')


@router.message(F.text == start_application_btn)
async def start_application_handler(message: Message, state: FSMContext):

    answer = message.answer(name_application_message,
                         reply_markup=name_application_keyboard(f'''{message.from_user.first_name}
{message.from_user.last_name}'''))

    await ApplicationService.next(state, ApplicationForm.name, answer)

@router.message(ApplicationForm.name, F.text)
async def name_proces_handler(message: Message, state: FSMContext):
    answer = message.answer(service_application_message, reply_markup=service_application_keyboard())

    if message.text in (home_btn, step_back_btn) :
        await ApplicationService.back_home(state, message)
    else:
        await state.update_data(name=message.text)
        await ApplicationService.next(state, ApplicationForm.service, answer)

@router.message(ApplicationForm.service, F.text)
async def service_proces_handler(message: Message, state: FSMContext):
    answer = message.answer(details_application_message, reply_markup=application_keyboard())

    if message.text == home_btn:
        await ApplicationService.back_home(state, message)
    elif message.text == step_back_btn:
        await ApplicationService.back(state)
    elif message.text in buttons:
        await state.update_data(service=message.text)
        await ApplicationService.next(state, ApplicationForm.details, answer)


@router.message(ApplicationForm.details, F.text)
async def details_proces_handler(message: Message, state: FSMContext):
    answer = message.answer(file_application_message, reply_markup=application_keyboard())

    if message.text == home_btn:
        await ApplicationService.back_home(state, message)
    elif message.text == step_back_btn:
        await ApplicationService.back(state)
    elif message.text == skip_btn:
        await ApplicationService.skip(state, ApplicationForm.file, answer)
    else:
        await state.update_data(details=message.text)
        await ApplicationService.next(state, ApplicationForm.file, answer)


@router.message(ApplicationForm.file)
async def file_proces_handler(message: Message, state: FSMContext):
    answer = message.answer(contact_application_message, reply_markup=contact_application_keyboard())

    if message.text == home_btn:
        await ApplicationService.back_home(state, message)
    elif message.text == step_back_btn:
        await ApplicationService.back(state)
    elif message.text == skip_btn:
        await ApplicationService.skip(state, ApplicationForm.contact, answer)
    elif message.photo or message.document:
        file_id = message.document.file_id if message.document else message.photo[-1].file_id
        await state.update_data(file=file_id)
        await ApplicationService.next(state, ApplicationForm.contact, answer)
    else:
        await message.answer(is_not_file_message)


@router.message(ApplicationForm.contact, F.text == username_btn)
async def contact_proces_handler(message: Message, state: FSMContext):
    if not message.from_user.username:
        await message.answer(no_username_message, reply_markup=start_application_keyboard())
        await state.clear()
    else:
        await state.update_data(username=message.from_user.username)
        answer = message.answer(await final_application(state), reply_markup=confirm_application_keyboard())
        await ApplicationService.next(state, ApplicationForm.confirm, answer, ApplicationForm.username)


@router.message(ApplicationForm.contact, F.text == phone_number_btn)
async def contact_proces_handler(message: Message, state: FSMContext):
    answer = message.answer(phone_number_message, reply_markup=phone_number_application_keyboard())
    await ApplicationService.next(state, ApplicationForm.phone_number, answer, ApplicationForm.phone_number)


@router.message(ApplicationForm.contact)
async def contact_proces_handler(message: Message, state: FSMContext):
    if message.text == home_btn:
        await ApplicationService.back_home(state, message)
    elif message.text == step_back_btn:
        await ApplicationService.back(state)


@router.message(ApplicationForm.phone_number, F.contact)
async def phone_number_handler(message: Message, state: FSMContext):
    phone_number = message.contact.phone_number
    await state.update_data(phone_number=phone_number)
    answer = message.answer(await final_application(state), reply_markup=confirm_application_keyboard())
    await ApplicationService.next(state, ApplicationForm.confirm, answer)


@router.message(ApplicationForm.phone_number, F.text)
async def phone_number_handler(message: Message, state: FSMContext):
    if message.text == home_btn:
        await ApplicationService.back_home(state, message)
    elif message.text == step_back_btn:
        await ApplicationService.back(state)
    else:
        phone_number = message.text.strip()
        if is_phone_number(phone_number):
            await state.update_data(phone_number=phone_number)
            answer = message.answer(await final_application(state), reply_markup=confirm_application_keyboard())
            await ApplicationService.next(state, ApplicationForm.confirm, answer)
        else:
            await message.answer(invalid_phone_number)


@router.message(ApplicationForm.confirm, F.text)
async def phone_number_handler(message: Message, state: FSMContext):
    if message.text == home_btn:
        await ApplicationService.back_home(state, message)
    elif message.text == step_back_btn:
        await ApplicationService.back(state)
    elif message.text == confirm_application_btn:
        # await state.get_data() - и данные куда-то отправляются
        await state.clear()
        await message.answer(final_application_message, reply_markup=start_application_keyboard())
