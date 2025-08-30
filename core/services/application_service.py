from idlelib.window import add_windows_to_menu
from typing import Coroutine

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.methods import SendMessage
from aiogram.types import Message

from core.handlers.command_handlers import start_command_handler


class ApplicationService:
    states_history_key = 'states_history'
    answers_history_key = 'answers_history'

    @staticmethod
    async def next(state: FSMContext, next_state: State, answer: SendMessage, field_state: State = None):  # Метод для назначения следующего узла
        data = await state.get_data()

        states_history = data.get(ApplicationService.states_history_key, [])  # Получаем историю состояний или создаем пустую, если нет
        answers_history = data.get(ApplicationService.answers_history_key, [])  # Получаем историю ответов или создаем пустую, если нет

        current_state = await state.get_state()  # Берет текущее состояние
        current_state_field = None

        if current_state:
            current_state_field = current_state.split(':')[-1]  # Берет название состояния

        if field_state:  # Если указан этот параметр
            current_state_field = field_state.state.split(':')[-1]  # То использует его в качестве поля

        states_history.append({'state': current_state,
                               'field_state': current_state_field})  # Добавляет текущее состояние в список и состояние которое обновляется
        answers_history.append(answer)  # Добавляем answer в список answers

        await state.update_data({ApplicationService.states_history_key: states_history})  # Сохраняем
        await state.update_data({ApplicationService.answers_history_key: answers_history})

        await state.set_state(next_state)
        await answer

    @staticmethod
    async def back(state: FSMContext):  # Метод для шага назад
        data = await state.get_data()

        states_history = data.get(ApplicationService.states_history_key)  # Получаем историю состояний
        answers_history = data.get(ApplicationService.answers_history_key)  # Получаем историю answers

        last_state = states_history.pop()  # Забираем последнее состояние
        await state.update_data({last_state['field_state']: None})  # Стирает данные последнего поля

        if len(answers_history) < 2:
            ValueError('Некуда возвращаться')

        del answers_history[-1]  # Удаляет последний ответ из истории
        await answers_history[-1]  # Ожидает предыдущий ответ

        await state.set_state(last_state['state'])  # Предыдущее состояние

    @staticmethod
    async def skip(state: FSMContext, next_state: State, answer: SendMessage, field_state: State = None):  # Метод для пропуска
        await ApplicationService.next(state, next_state, answer, field_state)

    @staticmethod
    async def back_home(state: FSMContext, message: Message):  # Метод для возврата к началу
        await state.clear()
        await start_command_handler(message)  # Вернуться к начальному обработчику
