import subprocess
import threading
import sys
import time
import os

def run_app():
    try:
        subprocess.run([sys.executable, 'app.py'], check=True)
    except Exception as e:
        print(f"Ошибка запуска app.py: {e}")

def run_telegram_monitor():
    try:
        subprocess.run([sys.executable, 'telegram_monitor.py'], check=True)
    except KeyboardInterrupt:
        print("\n👋 Завершение telegram_monitor.py...")
    except Exception as e:
        print(f"Ошибка запуска telegram_monitor.py: {e}")

def main():
    # Создаем потоки для запуска приложений
    app_thread = threading.Thread(target=run_app)
    telegram_thread = threading.Thread(target=run_telegram_monitor)

    # Запускаем потоки
    app_thread.start()
    
    # Небольшая задержка, чтобы сайт успел запуститься
    time.sleep(2)
    
    telegram_thread.start()

    # Ждем завершения потоков
    app_thread.join()
    telegram_thread.join()

if __name__ == "__main__":
    main()
