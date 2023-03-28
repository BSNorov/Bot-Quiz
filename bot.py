import telebot
import random
import time

bot = telebot.TeleBot('5990456095:AAGyvm_XzPQG2HzB0VIHA63Sf5LTmb7DDAA')

questions = [
    {"question": "Türkiye'nin başkenti neresidir?", "answer": "Ankara"},
    {"question": "Türkiye'nin en uzun nehri hangisidir?", "answer": "Kızılırmak"},
    {"question": "Türkiye'nin en büyük gölü hangisidir?", "answer": "Van Gölü"},
    # добавьте свои вопросы здесь
]

questions_ru = [
{"question": "Какая столица Турции?", "answer": "Анкара"},
{"question": "Какая самая длинная река в Турции?", "answer": "Кызылырмак"},
{"question": "Какое самое большое озеро в Турции?", "answer": "Ванское озеро"},
# добавьте свои вопросы здесь
]

user_language = {}
scores = {}

# клавиатуры
start_keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1)
start_keyboard.add(telebot.types.KeyboardButton('Начать 🚀 - Başla 🚀'))

language_keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2)
language_keyboard.add(telebot.types.KeyboardButton('Türkçe 🇹🇷'), telebot.types.KeyboardButton('Русский 🇷🇺'))

main_menu_keyboard_tr = telebot.types.ReplyKeyboardMarkup(row_width=2)
main_menu_keyboard_tr.add(telebot.types.KeyboardButton('Soru Sor 🤔'), telebot.types.KeyboardButton('Pes Et 😔'),
                       telebot.types.KeyboardButton('Skor 📊'), telebot.types.KeyboardButton('Dil 🌐'))

main_menu_keyboard_ru = telebot.types.ReplyKeyboardMarkup(row_width=2)
main_menu_keyboard_ru.add(telebot.types.KeyboardButton('Вопрос 🤔'), telebot.types.KeyboardButton('Сдаться 😔'),
                       telebot.types.KeyboardButton('Счет 📊'), telebot.types.KeyboardButton('Язык 🌐'))



@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, '''Привет! Я Quiz-Bot. Нажмите "Начать", чтобы начать 🇷🇺 
Merhaba! Benim adım Quiz-Bot. Başlamak için "Başla"yı tıklayın 🇹🇷''', reply_markup=start_keyboard)

@bot.message_handler(func=lambda message: message.text == 'Начать 🚀 - Başla 🚀')
def choose_language(message):
    bot.send_message(message.chat.id, 'На каком языке вы хотите играть? / Hangi dili oynamak istiyorsun?', reply_markup=language_keyboard)

@bot.message_handler(func=lambda message: message.text in ['Türkçe 🇹🇷', 'Русский 🇷🇺'])
def set_language(message):
    if message.text == 'Türkçe 🇹🇷':
        user_language[message.chat.id] = 'Türkçe'
        bot.send_message(message.chat.id, 'Dil seçildi: Türkçe 🇹🇷', reply_markup=main_menu_keyboard_tr)
    elif message.text == 'Русский 🇷🇺':
        user_language[message.chat.id] = 'Русский'
        bot.send_message(message.chat.id, 'Выбран язык: Русский 🇷🇺', reply_markup=main_menu_keyboard_ru)


@bot.message_handler(func=lambda message: message.text == 'Dil 🌐' or message.text == 'Язык 🌐')
def change_language(message):
    bot.send_message(message.chat.id, 'Hangi dili tercih edersin?', reply_markup=language_keyboard)


@bot.message_handler(func=lambda message: message.text == 'Soru Sor 🤔' or message.text == 'Вопрос 🤔')
def ask_question(message):
    chat_id = message.chat.id
    language = user_language.get(message.chat.id, 'Türkçe')
    ready_message = bot.send_message(chat_id, 'Будьте готовы!')
    countdown = 5
    countdown_message = None
    while countdown > 0:
        if countdown_message:
            bot.edit_message_text(chat_id=chat_id, message_id=countdown_message.message_id, text=str(countdown))
        else:
            countdown_message = bot.send_message(chat_id, countdown)
        time.sleep(1)
        countdown -= 1
    bot.delete_message(chat_id, countdown_message.message_id)
    bot.delete_message(chat_id, ready_message.message_id)
    bot.send_message(chat_id, 'Ответьте на вопрос:')
    if language == 'Türkçe':
        question = random.choice(questions)
        answer = question['answer']
        bot.send_message(chat_id, question['question'])
    else:
        question = random.choice(questions_ru)
        answer = question['answer']
        bot.send_message(chat_id, question['question'])
    bot.register_next_step_handler(message, check_answer, answer, language)

def check_answer(message, answer, language):
    if message.text.lower() == answer.lower():
        user_id = message.chat.id
        score = scores.get(user_id, 0)
        scores[user_id] = score + 1
        bot.send_message(message.chat.id, 'Tebrikler! Doğru cevap 🎉' if language == 'Türkçe' else 'Поздравляю! Верный ответ 🎉', reply_markup=main_menu_keyboard_tr if language == 'Türkçe' else main_menu_keyboard_ru)
    elif message.text == 'Pes Et 😔' or message.text == 'Сдаться 😔':
        bot.send_message(message.chat.id, f"Cevap: {answer}" if language == 'Türkçe' else f"Ответ: {answer}", reply_markup=main_menu_keyboard_tr if language == 'Türkçe' else main_menu_keyboard_ru)
    elif message.text == 'Skor 📊' or message.text == 'Счет 📊':
        bot.send_message(message.chat.id, 'Şimdilik skor bulunmamaktadır' if language == 'Türkçe' else 'На данный момент нет результатов', reply_markup=main_menu_keyboard_tr if language == 'Türkçe' else main_menu_keyboard_ru)
    else:
        bot.send_message(message.chat.id, 'Yanlış cevap 😢' if language == 'Türkçe' else 'Неправильный ответ 😢', reply_markup=main_menu_keyboard_tr if language == 'Türkçe' else main_menu_keyboard_ru)



@bot.message_handler(func=lambda message: message.text == 'Skor 📊' or message.text == 'Счет 📊')
def get_score(message):
    user_id = message.chat.id
    language = user_language.get(user_id, 'Türkçe')
    score = scores.get(user_id, 0)
    bot.send_message(user_id, f"Ваш счет: {score}", reply_markup=main_menu_keyboard_tr if language == 'Türkçe' else main_menu_keyboard_ru)



bot.polling()
