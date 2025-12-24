"""
Auto Sleep - Автоматический переход в спящий режим после периода бездействия.

Скрипт отслеживает время бездействия пользователя и автоматически переводит
систему в спящий режим, если пользователь не взаимодействовал с компьютером
в течение заданного времени.

Требования: Windows, Python 3.6+
"""

import ctypes
import time
import os
import sys

# Настройки
IDLE_THRESHOLD_SECONDS = 1800  # 30 минут простоя
CHECK_INTERVAL = 60            # Проверять каждую минуту


class LASTINPUTINFO(ctypes.Structure):
    """Структура для получения информации о последнем вводе пользователя."""
    _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]


def get_idle_time():
    """
    Получает время бездействия системы в секундах.

    Returns:
        float: Время бездействия в секундах

    Raises:
        OSError: Если не удалось получить информацию о времени бездействия
    """
    try:
        lii = LASTINPUTINFO()
        lii.cbSize = ctypes.sizeof(LASTINPUTINFO)

        if not ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii)):
            raise OSError("Не удалось получить информацию о последнем вводе")

        millis = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
        return millis / 1000.0
    except Exception as e:
        print(f"Ошибка при получении времени бездействия: {e}")
        return 0.0


def suspend_system():
    """
    Переводит систему в спящий режим.

    Примечание: Работает только на Windows.
    """
    try:
        # Команда для спящего режима (Windows)
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

        # Если нужно именно выключение, используйте:
        # os.system("shutdown /s /t 1")
    except Exception as e:
        print(f"Ошибка при переходе в спящий режим: {e}")


def main():
    """Основная функция программы."""
    # Проверка операционной системы
    if sys.platform != "win32":
        print("Ошибка: Скрипт работает только на Windows!")
        sys.exit(1)

    print(f"Скрипт запущен. Ожидание простоя: {IDLE_THRESHOLD_SECONDS} сек.")
    print(f"Интервал проверки: {CHECK_INTERVAL} сек.")
    print("Для остановки нажмите Ctrl+C\n")

    try:
        while True:
            idle_time = get_idle_time()

            # Выводим текущее время простоя (опционально, можно закомментировать)
            minutes = int(idle_time // 60)
            seconds = int(idle_time % 60)
            print(f"Время простоя: {minutes} мин. {seconds} сек.", end='\r')

            if idle_time >= IDLE_THRESHOLD_SECONDS:
                print("\nСистема простаивает. Переход в спящий режим...")
                suspend_system()
                break  # Выход из цикла после перехода в спящий режим

            time.sleep(CHECK_INTERVAL)

    except KeyboardInterrupt:
        print("\n\nСкрипт остановлен пользователем.")
        sys.exit(0)
    except Exception as e:
        print(f"\nКритическая ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()