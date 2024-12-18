from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv, set_key
import threading
import json
from datetime import datetime, timedelta

load_dotenv()

app = Flask(__name__)

ENV_PATH = os.path.join(os.path.dirname(__file__), '.env')
CONFIG_FILE = 'config.json'

def load_config():
    load_dotenv(ENV_PATH)
    return {
        'channel_username': os.getenv('CHANNEL_USERNAME', ''),
        'personal_chat_id': os.getenv('PERSONAL_CHAT_ID', ''),
        'keywords': os.getenv('KEYWORDS', '').split(',') if os.getenv('KEYWORDS') else [],
        'bot_token': os.getenv('BOT_TOKEN', '')
    }

def load_time_config():
    """Загрузка конфигурации времени"""
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {
            'custom_utc_time': None,
            'time_offset_hours': 12
        }

def save_time_config(config):
    """Сохранение конфигурации времени"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

@app.route('/')
def index():
    config = load_config()
    time_config = load_time_config()
    return render_template('index.html', 
                           **config, 
                           custom_utc_time=time_config.get('custom_utc_time'),
                           time_offset=time_config.get('time_offset_hours', 12))

@app.route('/help')
def help_page():
    return render_template('help.html')

@app.route('/save_config', methods=['POST'])
def save_config():
    try:
        data = request.json
        
        # Обновляем переменные окружения
        set_key(ENV_PATH, 'CHANNEL_USERNAME', data.get('channel_username', ''))
        set_key(ENV_PATH, 'PERSONAL_CHAT_ID', data.get('personal_chat_id', ''))
        set_key(ENV_PATH, 'BOT_TOKEN', data.get('bot_token', ''))
        
        # Обновляем ключевые слова
        keywords = data.get('keywords', [])
        set_key(ENV_PATH, 'KEYWORDS', ','.join(keywords))
        
        return jsonify({
            'status': 'success',
            'message': 'Конфигурация успешно сохранена'
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Ошибка сохранения: {str(e)}'
        }), 500

@app.route('/set_time', methods=['POST'])
def set_time():
    config = load_time_config()
    
    # Получаем данные из формы
    custom_utc_time_str = request.form.get('custom_utc_time')
    time_offset = int(request.form.get('time_offset', 12))
    
    # Обработка пользовательского UTC времени
    if custom_utc_time_str:
        try:
            # Парсим время в формате ISO
            custom_utc_time = datetime.fromisoformat(custom_utc_time_str.replace('Z', '+00:00'))
            config['custom_utc_time'] = custom_utc_time.isoformat()
        except ValueError:
            return jsonify({'status': 'error', 'message': 'Неверный формат UTC времени'})
    else:
        config['custom_utc_time'] = None
    
    # Сохраняем настройки времени
    config['time_offset_hours'] = time_offset
    save_time_config(config)
    
    return jsonify({
        'status': 'success', 
        'message': 'Время UTC успешно обновлено',
        'custom_utc_time': config.get('custom_utc_time'),
        'time_offset': time_offset
    })

@app.route('/get_time_settings')
def get_time_settings():
    config = load_time_config()
    return jsonify({
        'custom_utc_time': config.get('custom_utc_time'),
        'time_offset': config.get('time_offset_hours', 12)
    })

def run_flask_app():
    app.run(host='127.0.0.1', port=5000, debug=False)

if __name__ == '__main__':
    print(" Сайт управления запущен. Перейдите по адресу: http://localhost:5000")
    run_flask_app()
