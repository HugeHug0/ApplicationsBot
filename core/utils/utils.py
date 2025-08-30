import phonenumbers


async def final_application(state):
    data = await state.get_data()

    name = data.get('name').replace('\n', ' ')
    service = data.get('service')
    details = data.get('details')
    file = data.get('file')
    contact = data.get('phone_number') or f'@{data.get('username')}'


    return f'''✅ Ваша заявка сформирована ✅

    Имя: {name if name else 'Отсутствует'}
    Услуга: {service if service else 'Отсутствует'}
    Детали: {details if details else 'Отсутствует'}
    Файл: {'Прикреплен' if file else 'Отсутствует'}
    Способ связи: {contact if contact else 'Отсутствует'}

    Мы вам обязательно перезвоним! (Нет, поскольку демо версия)

    '''

def is_phone_number(text: str) -> bool:
    try:
        number = phonenumbers.parse(text, None)  # None — не указываем страну
        return phonenumbers.is_possible_number(number) and phonenumbers.is_valid_number(number)
    except phonenumbers.NumberParseException:
        return False


