import os
import torch
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

MODEL_PATH = "checkpoint-26608"

ANSWERS_DIR = "user_test_answers"

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

MAX_LEN = 128

ID2AUTHOR = {
    0: "Артём",
    1: "Влад",
    2: "Георгий",
    3: "Даня",
    4: "Дима",
    5: "Лёша",
    6: "Маша",
    7: "Моя Бабушка Таня",
    8: "Саша"
}

NUM_LABELS = len(ID2AUTHOR)

QUESTIONS = [
    "Вопрос 1/10: Как  дела?",
    "Вопрос 2/10: Что делаешь?",
    "Вопрос 3/10: Что кушал сегодня?",
    "Вопрос 4/10: Что будешь завтра делать?",
    "Вопрос 5/10: Как ты относишься к неграм?",
    "Вопрос 6/10: Какое качество в людях ты ценишь больше всего?",
    "Вопрос 7/10:  Сколько ты зарабатываешь?",
    "Вопрос 8/10: Как тебя зовут?",
    "Вопрос 9/10: Ты сделал лабу на субботу?",
    "Вопрос 10/10:  В чем смысл жизни?"
]

LOGGING_LEVEL = "INFO"
