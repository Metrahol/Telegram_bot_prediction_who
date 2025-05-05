# Классификатор Стиля Автора Telegram-сообщений и Бот-Тест

Этот проект содержит дообученную модельку (rubertBert-conversation) на сообщениях моих друзей и меня в переписках в VK,Telegram и т.д. Задача модели угадать автора, по 10 ответам на вопросы ( по семантике конечно, а не смыслу). 

F1-score составляет всего 66%, потому что данные имеют большой дисбаланс ( 3 класса по 100к сообщений, 4 класса по 20-10 к, и 2 класса 2-3 тысячи). Но делал по фану для друзей, поэтому как игрушка сойдет.

## Технологии
*   Python 3.11+
*   PyTorch
*   Hugging Face Transformers (модель rubert-base-cased / rubert-conversational)
*   Aiogram 3.x
*   Pandas
*   Scikit-learn
*   NumPy
*   python-dotenv

## Установка
1.  Клонируйте репозиторий:
    ```bash
    git clone https://github.com/Etrahol/Telegram_bot_prediction_who.git
    cd Telegram_bot_prediction_who
    ```
2.  Создайте и активируйте виртуальное окружение (рекомендуется):
    ```bash
    python -m venv venv
    # Windows:
    venv\Scripts\activate
    # macOS/Linux:
    source venv/bin/activate
    ```
3.  Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```
## Настройка
1.  **Модель:** 
    *   Скачайте архив с обученной моделью https://drive.google.com/file/d/1I1_dTrv1IJi0l4oUv5IrrsFOiq3fDmJN/view?usp=drive_link.
    *   Распакуйте архив.
    *   В файле `config.py` установите переменную `MODEL_PATH` так, чтобы она указывала на путь к распакованной папке с моделью (например, `MODEL_PATH = "best_checkpoint"`).
2.  **Токен Бота:**
    *   Создайте файл `.env` в корневой папке проекта.
    *   Добавьте в него строку: `TELEGRAM_TOKEN="ВАШ_ТОКЕН_ОТ_BOTFATHER"` (замените на реальный токен).
  
## Запуск Бота
```bash
python main.py


