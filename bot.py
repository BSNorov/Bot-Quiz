import random
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

logging.basicConfig(level=logging.INFO)

TOKEN = "5990456095:AAGyvm_XzPQG2HzB0VIHA63Sf5LTmb7DDAA"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

questions = {
    "Türkiye'nin başkenti neresidir?": "Ankara",
    "Türkiye'nin en yüksek dağı nedir?": "Ağrı Dağı",
    "Türkiye'nin en büyük gölü nedir?": "Van Gölü",
    "Türkiye'nin en uzun nehri nedir?": "Kızılırmak",
    "Türkiye'nin en kalabalık şehri nedir?": "İstanbul"
}


async def start(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for question in questions:
        keyboard.add(KeyboardButton(question))
    await message.reply("Merhaba! Benim adım QuizBot. Hazır mısın bir viktorine oynamaya? "
                        "O zaman, başlayalım! İlk soru seçiniz:", reply_markup=keyboard)

    async with dp.current_state(chat=message.chat.id, user=message.from_user.id) as state:
        await state.set_state("quiz")
        await state.set_data({"questions": list(questions.keys())})


async def answer(message: types.Message):
    user_answer = message.text
    async with dp.current_state(chat=message.chat.id, user=message.from_user.id) as state:
        data = await state.get_data()
        questions_list = data.get("questions")
        current_question = data.get("current_question")
        correct_answer = questions[questions_list[current_question]]
        if user_answer == correct_answer:
            await message.reply("Tebrikler, doğru cevap!")
        else:
            await message.reply("Maalesef, yanlış cevap. Doğru cevap {}.".format(correct_answer))
        next_question = current_question + 1
        if next_question == len(questions_list):
            await message.reply("Tebrikler, oyunu tamamladınız!")
            await state.finish()
        else:
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(KeyboardButton(questions_list[next_question]))
            await message.reply(questions_list[next_question], reply_markup=keyboard)
            await state.set_data({"current_question": next_question})


async def unknown(message: types.Message):
    await message.reply("Üzgünüm, bu komutu anlayamadım.")


dp.register_message_handler(start, commands=["start"])
dp.register_message_handler(answer, state="quiz")
dp.register_message_handler(unknown)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
