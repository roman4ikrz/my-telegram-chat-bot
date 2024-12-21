import telebot
from datetime import datetime
import threading
import time

TOKEN = '12345'
bot = telebot.TeleBot(TOKEN)

# Хранение напоминаний
reminders = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет пользователь! Напиши,  мне текст напоминания.")

@bot.message_handler(func=lambda message: True)
def set_reminder_text(message):
    user_id = message.chat.id
    reminder_text = message.text.strip()

    # Сохраняем текст напоминания
    reminders[user_id] = {'text': reminder_text, 'time': None}
    bot.send_message(user_id, "Теперь напиши дату и время в формате 'день.месяц.год-00:00, пример-16.10.2024-22:27.")

    # Устанавливаем следующую функцию обработки
    bot.register_next_step_handler(message, set_reminder_time, reminder_text)

def set_reminder_time(message, reminder_text):
    user_id = message.chat.id
    try:
        reminder_time = datetime.strptime(message.text.strip(), '%d.%m.%Y-%H:%M')
        reminders[user_id]['time'] = reminder_time
        bot.send_message(user_id, f"Напоминание установлено на {reminder_time} с сообщением: '{reminder_text}'.")
        threading.Thread(target=wait_and_remind, args=(user_id, reminder_time, reminder_text)).start()
    except ValueError:
        bot.send_message(user_id, "Неверный формат. Используй 'день.месяц.год-00:00'. Пожалуйста, введи дату и время снова.")
        bot.register_next_step_handler(message, set_reminder_time, reminder_text)

def wait_and_remind(user_id, reminder_time, reminder_text):
    while True:
        if datetime.now() >= reminder_time:
            bot.send_message(user_id, reminder_text)
            break
        time.sleep(10)

if __name__ == '__main__':
    bot.polling(none_stop=True)
