import telebot
from telebot import types
from schedule import schedule

bot = telebot.TeleBot('Your bot API Token')

# старт движняка
@bot.message_handler(content_types=['text'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я бот, который скинет тебе твое расписание! Если в боте есть какая либо ошибка, то пиши сюда: @stepashkaept")
    class_keyboard = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    class_buttons = [types.KeyboardButton(str(number)) for number in range(5, 9)]
    class_buttons1 = [types.KeyboardButton(str(number)) for number in range(10, 11)]
    class_keyboard.add(*class_buttons, *class_buttons1)
    bot.send_message(message.chat.id, "Выбери цифру своего класса:", reply_markup=class_keyboard)
    bot.register_next_step_handler(message, letter)


# твой буква, брат
def letter(message):
    class_number = message.text
    letter_keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    letter_buttons = [types.KeyboardButton(letter) for letter in ['а', 'б', 'в', 'г', 'д']]
    backrooms = types.KeyboardButton ('назад')
    letter_keyboard.add(*letter_buttons, backrooms)
    bot.send_message(message.chat.id, "Выбери букву своего класса:", reply_markup=letter_keyboard)
    bot.register_next_step_handler(message, back1, class_number)


# первый из костылей ввиде клопки 'назад'
def back1(message, class_number):
    if message.text == 'назад':
        class_keyboard = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
        class_buttons = [types.KeyboardButton(str(number)) for number in range(5, 9)]
        class_buttons1 = [types.KeyboardButton(str(number)) for number in range(10, 11)]
        class_keyboard.add(*class_buttons, *class_buttons1)
        bot.send_message(message.chat.id, "Выбери цифру своего класса:", reply_markup=class_keyboard)
        bot.register_next_step_handler(message, letter)
    else:
        day(message, class_number)


# день недели, брат
def day(message, class_number):
    class_letter = message.text
    day_keyboard = types.ReplyKeyboardMarkup(row_width=2)
    backrooms = types.KeyboardButton ('назад')
    day_buttons = [types.KeyboardButton(day) for day in ['понедельник', 'вторник', 'среда', 'четверг', 'пятница']]
    day_keyboard.add(*day_buttons, backrooms)
    bot.send_message(message.chat.id, "Выбери день недели:", reply_markup=day_keyboard)
    bot.register_next_step_handler(message, back2, class_number, class_letter)

# второй из костылей ввиде клопки 'назад'
def back2(message, class_number, class_letter):
    if message.text == 'назад':
        class_keyboard = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
        class_buttons = [types.KeyboardButton(str(number)) for number in range(5, 9)]
        class_buttons1 = [types.KeyboardButton(str(number)) for number in range(10, 11)]
        class_keyboard.add(*class_buttons, *class_buttons1)
        bot.send_message(message.chat.id, "Выбери цифру своего класса:", reply_markup=class_keyboard)
        bot.register_next_step_handler(message, letter)
    else:
        schedule_res(message, class_number, class_letter)

# победа
def schedule_res(message, class_number, class_letter):
    day = message.text
    if (class_number in schedule and class_letter in schedule[class_number] and day in
            schedule[class_number][class_letter]):
        hz = f"Расписание на {day} для {class_number}{class_letter}:\n"
        for lesson in schedule[class_number][class_letter][day]:
            hz += f"{lesson}\n"
        bot.send_message(message.chat.id, hz)
        start2(message)
    else:
        bot.send_message(message.chat.id, "Расписание не найдено.")
        start2(message)

# старт с самого начала
def start2(message):
    class_keyboard = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    class_buttons = [types.KeyboardButton(str(number)) for number in range(5, 9)]
    class_buttons1 = [types.KeyboardButton(str(number)) for number in range(10, 11)]
    class_keyboard.add(*class_buttons, *class_buttons1)
    bot.send_message(message.chat.id, "Выбери цифру своего класса:", reply_markup=class_keyboard)
    bot.register_next_step_handler(message, letter)

# запуск бота
bot.polling(none_stop=True)