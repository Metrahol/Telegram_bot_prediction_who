import os
import sys
import logging

import torch
import torch.nn.functional as F
import numpy as np
from transformers import AutoModelForSequenceClassification, AutoTokenizer

import config

logger = logging.getLogger(__name__)

model = None
tokenizer = None


def load_model_and_tokenizer():
    """Загружает модель и токенизатор из пути, указанного в config.py."""
    global model, tokenizer

    model_path = config.MODEL_PATH
    device = config.DEVICE

    logger.info(f"Загрузка модели и токенизатора из: {model_path}")
    logger.info(f"Используемое устройство: {device}")

    try:
        if not os.path.isdir(model_path):
            logger.warning(f"Локальный путь '{model_path}' не найден. Попытка загрузки с Hugging Face Hub...")
            pass

        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForSequenceClassification.from_pretrained(
            model_path,
            id2label=config.ID2AUTHOR,
        )
        model.to(device)
        model.eval()
        logger.info(f"Модель и токенизатор успешно загружены и готовы к работе на {device}.")

    except OSError as e:
        logger.exception(
            f"Критическая ошибка: Не удалось найти или загрузить модель/токен-р из '{model_path}'. Проверьте путь или имя на Hub. Ошибка: {e}")
        sys.exit(f"Завершение работы: Не удалось загрузить модель из {model_path}")
    except Exception as e:
        logger.exception(f"Критическая ошибка при загрузке модели из {model_path}: {e}")
        sys.exit("Не удалось загрузить модель. Бот не может стартовать.")


if model is None or tokenizer is None:
    load_model_and_tokenizer()


def get_prediction(text: str) -> tuple[int, np.ndarray]:
    """
    Получает текст, возвращает ID предсказанного автора и вектор вероятностей.
    Возвращает (-1, пустой_массив) при ошибке или пустом вводе.
    """

    global tokenizer

    if model is None or tokenizer is None:
        logger.error("Модель или токенизатор не загружены!")
        return -1, np.zeros(config.NUM_LABELS)

    if not text or not text.strip():
        logger.warning("Получен пустой текст для предсказания.")
        return -1, np.zeros(config.NUM_LABELS)

    try:

        inputs = tokenizer(
            text,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=config.MAX_LEN
        )
        inputs = {k: v.to(config.DEVICE) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits

        probabilities = F.softmax(logits, dim=-1).cpu().numpy()[0]  # [0] т.к. батч из 1

        predicted_class_id = np.argmax(probabilities)

        return predicted_class_id, probabilities

    except Exception as e:
        logger.error(f"Ошибка во время предсказания для текста '{text[:50]}...': {e}")
        return -1, np.zeros(config.NUM_LABELS)


def get_author_name(author_id: int) -> str:
    """Возвращает имя автора по ID из конфига или 'Неизвестный'."""
    return config.ID2AUTHOR.get(author_id, "Неизвестный")
