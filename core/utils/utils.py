import phonenumbers
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InputMediaPhoto, InputMediaVideo

from core.keyboards.reply_keyboards import confirm_application_keyboard


async def final_application_answer(message: Message, state: FSMContext):
    data = await state.get_data()

    name = data.get('name').replace('\n', ' ')
    service = data.get('service')
    details = data.get('details')
    files = data.get('files')
    contact = data.get('phone_number') or f'@{data.get("username")}'


    final_answer = f"""✅ Ваша заявка сформирована ✅

👤 Имя: {name if name else '—'}
📂 Услуга: {service if service else '—'}
📄 Детали: {details if details else '—'}
📎 Файлы: {'Прикреплены' if files else '—'}
📞 Способ связи: {contact if contact else '—'}

🔔 Мы обязательно с вами свяжемся! (В демо-версии обратный звонок не производится)
"""

    if not files:
        files = {}

    if files.get('photos_id'):
        media = [InputMediaPhoto(media=file_id) for file_id in files['photos_id'][:10]]
        await message.answer_media_group(media)
    if files.get('videos_id'):
        media_videos = [InputMediaVideo(media=file_id) for file_id in files['videos_id'][:5]]
        await message.answer_media_group(media=media_videos)

    await message.answer(final_answer, reply_markup=confirm_application_keyboard())

    if files.get('documents_id'):
        for document_id in files['documents_id']:
            await message.answer_document(document_id)


async def update_files_id(message: Message, state: FSMContext):
    data = await state.get_data()
    files = data.get('files', {'documents_id': [], 'photos_id': [], 'videos_id': []})

    # Добавляем файлы в соответствующие списки
    if message.document:
        files['documents_id'].append(message.document.file_id)
    elif message.photo:
        files['photos_id'].append(message.photo[-1].file_id)  # Берем последнюю фотографию
    else:
        files['videos_id'].append(message.video.file_id)

    # Обновляем данные состояния
    await state.update_data(files=files)


def is_phone_number(text: str) -> bool:
    try:
        number = phonenumbers.parse(text, None)  # None — не указываем страну
        return phonenumbers.is_possible_number(number) and phonenumbers.is_valid_number(number)
    except phonenumbers.NumberParseException:
        return False
