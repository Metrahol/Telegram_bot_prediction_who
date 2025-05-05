import logging
import os
from collections import Counter
from contextlib import suppress

from aiogram import F, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.exceptions import TelegramBadRequest

import config
from states import TestStates
from model_utils import (
    get_prediction,
    get_author_name
)
from utils import sanitize_filename

logger = logging.getLogger(__name__)


async def command_start_handler(message: Message, state: FSMContext) -> None:
    """Обрабатывает команду /start, сбрасывает состояние и предлагает начать тест."""
    await state.clear()
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Начать тест!", callback_data="start_test")]
    ])
    await message.answer(
        "Привет! 👋\nЯ бот, который попробует угадать, на кого из моих друзей "
        "ты похож по стилю письма.\n\n"
        "Я задам 10 вопросов. Пожалуйста, отвечай на них текстом, "
        "стараясь писать так, как ты обычно общаешься.\n\n"
        "Готов(а) начать?",
        reply_markup=keyboard
    )


async def start_test_callback(query: CallbackQuery, state: FSMContext) -> None:
    """Обрабатывает нажатие кнопки, запускает тест."""
    await query.answer()

    with suppress(TelegramBadRequest):
        await query.message.edit_text(
            text=f"{query.message.text}\n\nОтлично! Поехали.",
            reply_markup=None
        )

    await state.update_data(question_index=0, answers=[], predictions=[])

    await state.set_state(TestStates.answering)

    await query.message.answer(config.QUESTIONS[0])


async def handle_answer(message: Message, state: FSMContext) -> None:
    """
    Обрабатывает текстовый ответ пользователя, сохраняет его,
    получает предсказание, задает следующий вопрос или подводит итоги.
    """
    user_answer = message.text
    user_info = message.from_user

    if user_info and user_answer and user_answer.strip():
        base_filename = f"{user_info.id}_{user_info.username or user_info.first_name or 'user'}"
        safe_filename = sanitize_filename(base_filename) + ".txt"
        file_path = os.path.join(config.ANSWERS_DIR, safe_filename)
        try:
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(user_answer.strip() + "\n\n")
        except IOError as e:
            logger.error(f"Не удалось записать ответ в файл {file_path}: {e}")
        except Exception as e:
            logger.error(f"Неожиданная ошибка при сохранении ответа в файл: {e}")

    data = await state.get_data()
    current_index = data.get("question_index", 0)
    answers = data.get("answers", [])
    predictions = data.get("predictions", [])

    answers.append(user_answer)

    predicted_id, _ = get_prediction(user_answer)
    if predicted_id != -1:
        predictions.append(predicted_id)
    else:
        logger.warning(f"Предсказание для ответа пользователя {user_info.id} не получено.")

    next_index = current_index + 1

    if next_index < 10:
        # Если есть еще вопросы
        await state.update_data(question_index=next_index, answers=answers, predictions=predictions)
        await message.answer(config.QUESTIONS[next_index])
        await state.set_state(TestStates.answering)
    else:

        await message.answer("Спасибо! Ты ответил(а) на все вопросы. Сейчас я подумаю...")

        if not predictions:
            await message.answer(
                "К сожалению, не удалось проанализировать твои ответы (не получено ни одного предсказания стиля). Попробуй еще раз /start")
            await state.clear()
            return

        vote_counts = Counter(predictions)
        most_common_list = vote_counts.most_common(1)

        winner_id = most_common_list[0][0]
        winner_author = get_author_name(winner_id)

        result_text = f"Готово! ✨\n\nПроанализировав твои ответы, я думаю, что твой стиль письма больше всего похож на стиль общения **{winner_author}** в наших чатах."

        details = "\n\n(Детали голосования:\n"
        for author_id, count in vote_counts.most_common():  # Показываем все голоса
            author_name = get_author_name(author_id)
            details += f"- {author_name}: {count} раз(а)\n"
        details += ")"
        result_text += details

        await message.answer(result_text, parse_mode=ParseMode.MARKDOWN)

        await state.clear()


async def handle_wrong_answer_type(message: Message, state: FSMContext):
    """Ругает пользователя за нетекстовый ответ и повторяет вопрос."""
    await message.reply("Пожалуйста, отвечай на вопросы текстом.")

    data = await state.get_data()
    current_index = data.get("question_index", 0)

    if 0 <= current_index < 10:
        await message.answer(config.QUESTIONS[current_index])


def register_handlers(dp: Dispatcher):
    """Регистрирует все хендлеры в переданном диспетчере."""
    dp.message.register(command_start_handler, CommandStart())
    dp.callback_query.register(start_test_callback, F.data == "start_test")
    dp.message.register(handle_answer, TestStates.answering, F.text)
    dp.message.register(handle_wrong_answer_type, TestStates.answering)
    logger.info("Хендлеры успешно зарегистрированы.")
