# Telegram Monitor 🤖

## 👤 Разработчики

**Компания:** Пустота
**Главный разработчик:** Cascade AI
**Технический куратор:** Войд Емптинесс 

## 🌟 О проекте

Telegram Monitor - это мощный инструмент для отслеживания ключевых слов в телеграм-каналах. Разработан с целью помощи пользователям в автоматическом мониторинге важной информации.

## 🚀 Мой вклад и вклад ИИ

### Мой вклад (Войд Емптинесс):
- Определение бизнес-требований к проекту
- Тестирование и отладка функционала
- Формулировка технических требований

### Вклад ИИ (Cascade AI):
1. **Архитектура проекта**:
   - Разработка структуры телеграм-бота
   - Создание модуля мониторинга каналов
   - Проектирование системы уведомлений

2. **Код и функциональность**:
   - Написание основного кода телеграм-монитора
   - Реализация механизма поиска ключевых слов
   - Интеграция Telegram API
   - Разработка обработчиков сообщений
   - Создание веб-интерфейса

3. **Оптимизация и безопасность**:
   - Рефакторинг кода
   - Добавление обработки ошибок

4. **Документация**:
   - Написание README
   - Создание инструкций по установке и использованию
   - Подготовка лицензии
   - Настройка .gitignore

**Совместная работа позволила создать надежный и удобный инструмент для мониторинга телеграм-каналов!**

## 🔧 Как получить API ключи для Telegram

### Шаг 1: Создание приложения в Telegram
1. Перейдите на сайт [my.telegram.org](https://my.telegram.org/)
2. Войдите под своим номером телефона
3. Выберите "API development tools"
4. Заполните форму:
   - App title: Название вашего приложения
   - Short name: Короткое имя (без пробелов)
   - URL: Можно оставить пустым
   - Platform: Выберите платформу (Windows, macOS, Linux)
   - Description: Краткое описание приложения

### Шаг 2: Получение API ID и API Hash
- После создания приложения вам выдадут:
  - `API ID` - числовой идентификатор
  - `API Hash` - секретный ключ

### Шаг 3: Создание Telegram Bot
1. Откройте [@BotFather](https://t.me/BotFather) в Telegram
2. Отправьте команду `/newbot`
3. Следуйте инструкциям для создания бота
4. Получите `BOT TOKEN`

## 🛠 Установка

1. Клонируйте репозиторий
```bash
git clone https://github.com/VoidEmptiness/telegram_monitor.git
cd telegram-monitor
```

3. Заполните файл `.env` или запустите start.bat и зайдите на http://127.0.0.1:5000
```
API_ID='ваш_api_id'
API_HASH='ваш_api_hash'
CHANNEL_USERNAME='ссылка_на_канал'
KEYWORDS='ключевые,слова,через,запятую'
PERSONAL_CHAT_ID='ваш_личный_чат_id'
BOT_TOKEN='токен_вашего_бота'
```

## 🚀 Запуск

```bash
start.bat
```

## ⚠️ Важно
- Убедитесь, что вы используете актуальные сыллки
- Проверьте корректность API ключей
- Соблюдайте правила использования Telegram API

## 📄 Лицензия

MIT License

Copyright (c) 2024 Войд Емптинесс(Void Emptiness)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## 🤝 Поддержка
По вопросам и предложениям почта: [voidemptiness63@gmail.com]
