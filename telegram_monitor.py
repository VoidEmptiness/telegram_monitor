from telethon import TelegramClient, events
import os
import logging
from dotenv import load_dotenv
from telethon.tl.types import InputPeerChannel
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.errors import ChannelInvalidError, ChannelPrivateError
from telethon.sessions import StringSession
import requests
import signal
import sys
from datetime import datetime, timedelta
import pytz
import asyncio
import json

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='telegram_monitor.log',
    filemode='w'
)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения
load_dotenv()

# Параметры подключения
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNEL_USERNAME = os.getenv('CHANNEL_USERNAME')
KEYWORDS = os.getenv('KEYWORDS', '').split(',') if os.getenv('KEYWORDS') else []
PERSONAL_CHAT_ID = int(os.getenv('PERSONAL_CHAT_ID'))

# Путь к файлу сессии
SESSION_FILE = 'telegram_session.session'

# Счетчик нажатий Ctrl+C
exit_count = 0

def signal_handler(sig, frame):
    global exit_count
    exit_count += 1
    
    if exit_count == 1:
        print("\n🛑 Нажмите Ctrl+C еще раз для завершения...")
    elif exit_count >= 2:
        print("\n👋 Завершение программы...")
        os._exit(0)  # Принудительное закрытие всех потоков

# Регистрация обработчика сигнала
signal.signal(signal.SIGINT, signal_handler)

def extract_username_from_link(channel_link):
    """Извлекает username из полной ссылки на канал"""
    logger.debug(f"Входная ссылка: {channel_link}")
    
    # Обработка приватных каналов с '+' в ссылке
    if channel_link.startswith('https://t.me/+'):
        return [channel_link.replace('https://t.me/', '')]
    
    # Варианты обработки ссылки
    variants = [
        channel_link.replace('https://t.me/', '').replace('t.me/', ''),  # Без префиксов
        channel_link.replace('https://t.me/', '@').replace('t.me/', '@'),  # С @
    ]
    
    # Фильтруем варианты, убираем лишние символы
    clean_variants = [
        variant.split('+')[0].strip()  # Убираем '+' и пробелы
        for variant in variants
    ]
    
    logger.debug(f"Варианты для проверки: {clean_variants}")
    
    # Возвращаем первый непустой вариант
    for variant in clean_variants:
        if variant and not variant.startswith('+'):
            return [variant]
    
    # Если не нашли подходящий username
    logger.warning(f"Не удалось извлечь username из ссылки: {channel_link}")
    return [channel_link]

async def send_notification(client, message):
    """
    Отправляет уведомление через Bot API.
    """
    try:
        # Формируем системное уведомление
        system_message = (
            "🚨 <b>СИСТЕМА МОНИТОРИНГА</b> 🚨\n\n"
            "Обнаружено совпадение по ключевому слову!\n\n"
            "Детали сообщения:\n"
        )
        
        # Полное сообщение с системным уведомлением
        full_message = system_message + message
        
        # Отправка через Bot API
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            params = {
                "chat_id": PERSONAL_CHAT_ID,
                "text": full_message,
                "parse_mode": "HTML"
            }
            
            response = requests.post(url, params=params)
            
            if response.status_code == 200:
                print("✅ Уведомление отправлено")
                return True
            else:
                print(f"❌ Не удалось отправить сообщение")
                return False
        
        except Exception as e:
            print(f"❌ Ошибка отправки сообщения")
            return False
    
    except Exception as favorite_error:
        print(f"❌ Глобальная ошибка")
        return False

def get_local_time(hours_back=12):
    """
    Получает локальное время с учетом часового пояса
    
    :param hours_back: Количество часов назад
    :return: Локальное время в UTC
    """
    # Загружаем конфигурацию времени
    try:
        with open('config.json', 'r') as f:
            time_config = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        time_config = {
            'custom_utc_time': None,
            'time_offset_hours': 12
        }
    
    # Определяем базовое время
    if time_config.get('custom_utc_time'):
        # Используем пользовательское UTC время
        base_time = datetime.fromisoformat(time_config['custom_utc_time']).replace(tzinfo=pytz.UTC)
    else:
        # Используем текущее локальное время
        base_time = datetime.now().astimezone(pytz.UTC)
    
    # Вычитаем указанное количество часов
    time_threshold = base_time - timedelta(hours=time_config.get('time_offset_hours', hours_back))
    
    # Отладочный вывод
    print(f"🕰️ Текущее время (UTC): {base_time}")
    
    return time_threshold

async def check_recent_messages(client, channel_entity, keywords, hours=12):
    """
    Проверяет сообщения за последние N часов на наличие ключевых слов
    
    :param client: Клиент Telegram
    :param channel_entity: Объект канала
    :param keywords: Список ключевых слов
    :param hours: Количество часов для проверки
    :return: Список найденных сообщений
    """
    try:
        # Получаем локальное время с учетом часового пояса
        time_threshold = get_local_time(hours)
        print(f"🕰️ Порог времени (UTC): {time_threshold}")
        
        # Получаем сообщения за последние N часов
        messages = await client.get_messages(
            channel_entity, 
            limit=None,  # Убираем ограничение
            offset_date=datetime.now(pytz.utc)  # Начинаем с текущего момента
        )
        
        # Список найденных сообщений
        matched_messages = []
        
        # Проверяем каждое сообщение
        for message in messages:
            # Делаем datetime сообщения timezone-aware
            message_date = message.date.replace(tzinfo=pytz.utc) if message.date else None
            
            # Пропускаем None и сообщения старше порога
            if not message or not message_date or message_date < time_threshold:
                continue
            
            message_text = message.message or ''
            
            # Проверка наличия ключевых слов
            for keyword in keywords:
                if keyword.strip().lower() in message_text.lower():
                    matched_messages.append({
                        'text': message_text,
                        'date': message_date,
                        'keyword': keyword
                    })
                    break  # Прекращаем проверку после первого совпадения
        
        return matched_messages
    
    except Exception as e:
        print(f"❌ Ошибка при проверке старых сообщений: {e}")
        return []

async def main():
    try:
        print("🤖 Запуск Telegram Монитора...")
        print("=" * 50)
        print("Проверка конфигурации...")
        print("Для завершения нажмите Ctrl+C")
        
        # Проверка наличия необходимых переменных
        if not all([API_ID, API_HASH, CHANNEL_USERNAME, KEYWORDS, PERSONAL_CHAT_ID]):
            print("❌ Ошибка: Не все необходимые параметры настроены в .env файле!")
            return

        print(f"✅ Канал для мониторинга: {CHANNEL_USERNAME}")
        print(f"🔍 Отслеживаемые ключевые слова: {', '.join(KEYWORDS)}")
        print(f"📨 Личный чат для уведомлений: {PERSONAL_CHAT_ID}")
        
        # Инициализация клиента Telegram
        print("\n🔐 Инициализация клиента Telegram...")
        
        # Создаем клиент с использованием Bot Token
        client = TelegramClient('bot_session', API_ID, API_HASH)
        
        # Регистрация обработчика сигнала для корректного закрытия
        signal.signal(signal.SIGINT, signal_handler)
        
        # Подключение к Telegram с использованием Bot Token
        await client.start(bot_token=BOT_TOKEN)
        
        print("\n🌐 Подключение к Telegram...")
        
        # Получаем информацию о текущем боте
        try:
            me = await client.get_me()
            print(f"🤖 Авторизован как бот: {me.first_name} {me.last_name or ''}")
        except Exception as bot_error:
            print(f"❌ Ошибка получения информации о боте: {bot_error}")
            return
        
        # Получаем информацию о канале
        try:
            print("\n🔎 Поиск канала...")
            username_variants = extract_username_from_link(CHANNEL_USERNAME)
            channel_entity = None
            
            for variant in username_variants:
                try:
                    print(f"🕵️ Пробую получить канал: {variant}")
                    
                    try:
                        channel_entity = await client.get_entity(variant)
                        print(f"✅ Канал найден: {channel_entity.title}")
                        break
                    except ValueError as ve:
                        print(f"❌ Ошибка получения канала: {ve}")
                        print("Возможные причины:")
                        print("1. Бот не является участником приватного канала")
                        print("2. Неправильная ссылка")
                        print("3. Проблемы с правами бота")
                    
                except Exception as entity_error:
                    print(f"❌ Не удалось получить канал с вариантом {variant}: {entity_error}")
            
            if not channel_entity:
                print("❌ Не удалось найти канал. Проверьте правильность ссылки.")
                return
            
            # Проверяем членство в канале
            try:
                full_channel = await client(GetFullChannelRequest(channel_entity))
                participants_count = full_channel.full_chat.participants_count
                print(f"👥 Количество участников канала: {participants_count}")
            except Exception as membership_error:
                print(f"❌ Не удалось проверить членство в канале: {membership_error}")
                print("Возможно, бот не имеет доступа к каналу")
                return
            
            # Небольшая задержка перед началом работы
            print("\n⏳ Ожидание 15 секунд перед началом мониторинга...")
            await asyncio.sleep(15)
            
            # Проверка старых сообщений при первом запуске
            print("\n🕰️ Проверка сообщений за последние 12 часов...")
            recent_matched_messages = await check_recent_messages(client, channel_entity, KEYWORDS)
            
            if recent_matched_messages:
                print(f"🚨 Найдено {len(recent_matched_messages)} сообщений с ключевыми словами!")
                
                # Отправляем уведомления о найденных сообщениях
                for msg in recent_matched_messages:
                    notification_message = (
                        f"📢 Найдено старое сообщение в канале {CHANNEL_USERNAME}\n"
                        f"🕒 Дата сообщения: {msg['date'].strftime('%Y-%m-%d %H:%M:%S')}\n"
                        f"🔍 Найденное ключевое слово: {msg['keyword']}\n\n"
                        f"📝 Текст сообщения:\n{msg['text']}"
                    )
                    await send_notification(client, notification_message)
            else:
                print("✅ Сообщений с ключевыми словами за 12 часов не найдено")
            
            # Обработчик новых сообщений
            @client.on(events.NewMessage(chats=channel_entity))
            async def new_message_handler(event):
                try:
                    message_text = event.message.message
                    
                    # Проверка наличия ключевых слов
                    matched_keywords = []
                    for keyword in KEYWORDS:
                        if keyword.strip().lower() in message_text.lower():
                            matched_keywords.append(keyword)
                    
                    # Отправляем уведомление ТОЛЬКО если есть ключевые слова
                    if matched_keywords:
                        notification_message = (
                            f"📢 Канал: {CHANNEL_USERNAME}\n"
                            f"🔍 Найденные ключевые слова: {', '.join(matched_keywords)}\n\n"
                            f"📝 Текст сообщения:\n{message_text}"
                        )
                        
                        # Отправка уведомления
                        await send_notification(client, notification_message)
                
                except Exception as e:
                    print(f"❌ Ошибка при обработке сообщения")
            
            # Запуск прослушивания канала
            await client.run_until_disconnected()
        
        except Exception as e:
            print(f"❌ Критическая ошибка при получении канала: {e}")
            return
    
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        return

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
