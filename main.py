import telebot
from telebot import types

bot = telebot.TeleBot('7643201067:AAHdQobwX5yNGFAQ-f9zULGFD9rq3Pr9jfQ')

admin_username = 'sellandprey'  # Укажите юзернейм администратора

user_interests = {}
events = {
    'Активный спорт': [
        {'photo': 'sport1.jpg', 'text': 'Покорение вершин \n\nПрисоединяйтесь к нашей команде на захватывающую экспедицию по заснеженным вершинам. Это уникальная возможность испытать себя и насладиться великолепными видами, не доступными обычным туристам. Встречи у костра и истории о великих покорителях гор создадут атмосферу приключения и дружбы!', 'url': 'https://google.com'},
        {'photo': 'sport2.jpg', 'text': 'Велопробег по живописным местам \n\nИспытай свои физические способности на велопрогулке, которая охватывает горные тропы и живописные долины. Насладись свежим воздухом и единением с природой. Сопровождение опытных инструкторов гарантирует безопасность и незабываемые эмоции!', 'url': 'https://google.com'}
    ],
    'Искусство': [
        {'photo': 'art1.jpg', 'text': 'Искусство вдохновения \n\nПогрузитесь в мир живописи на нашем мастер-классе! Под руководством известного художника вы узнаете секреты техники акварели и масла. Это не просто обучение, а возможность выразить свои чувства и открыть в себе новых взглядов на искусство!', 'url': 'https://google.com'},
        {'photo': 'art2.jpg', 'text': 'Оживление материи \n\nПриглашаем вас на выставку современных скульптур, где вас ждет встреча с креативными и революционными подходами к искусству. Познакомьтесь с произведениями признанных отечественных и зарубежных мастеров, вдохновляющими своей оригинальностью и значимостью.', 'url': 'https://google.com'}
    ],
    'Ночные тусовки': [
        {'photo': 'party1.jpg', 'text': 'В ритме ночи \n\nПогрузитесь в атмосферу энергичного клубного вечера! Зажигательная музыка от приглашенных DJ, световая шоу-программа и множество сюрпризов ждут вас. Наслаждайтесь танцем до утра в компании единомышленников и новых друзей!', 'url': 'https://google.com'},
        {'photo': 'party2.jpg', 'text': 'Под звездным небом \n\nПроведите ночь у моря, наслаждаясь живой музыкой и барбекю на открытом воздухе. Уютная атмосфера позволяет расслабиться, спеть песни у костра и забыть о городской суете. Идеальное место для романтических встреч и душевных разговоров!', 'url': 'https://google.com'}
    ],
    'Бизнес-образование': [
        {'photo': 'ed1.jpg', 'text': 'Захватите онлайн-пространство \n\nУзнайте, как эффективно продвигать ваш бизнес в интернете! Ведущие эксперты расскажут о трендах и новых стратегиях в области цифрового маркетинга. Познакомьтесь с успешными кейсами и получите практические рекомендации, которые помогут вам подняться на новый уровень!', 'url': 'https://google.com'},
        {'photo': 'ed2.jpg', 'text': 'Инвестируйте в себя \n\nПрисоединяйтесь к программе бизнес-коучинга, которая помогает развить лидерские качества и улучшить личную эффективность. Вас ждут интерактивные тренинги, групповые обсуждения и индивидуальные консультации с профессионалами. Получите новые инструменты для управления своим жизненным курсом!', 'url': 'https://google.com'}
    ]
}


@bot.message_handler(commands=['start'])
def start(message):
    interests = ['Активный спорт', 'Искусство', 'Ночные тусовки', 'Бизнес-образование']
    markup = types.InlineKeyboardMarkup(row_width=2)
    buttons = [types.InlineKeyboardButton(text=interest, callback_data=interest) for interest in interests]
    markup.add(*buttons)
    markup.add(types.InlineKeyboardButton(text="Готово", callback_data="Готово"))
    bot.send_photo(message.chat.id, open('welcome.jpg', 'rb'))
    bot.send_message(message.chat.id, f'Привет!'
                                      f'\n\nВыбери все свои интересы из списка, чтобы я мог подобрать для тебя мероприятия'
                                      f'\n\nКогда закончишь выбор, нажми на кнопку "Готово"', reply_markup=markup)
    user_interests[message.chat.id] = []
@bot.callback_query_handler(func=lambda call: call.data in events.keys() or call.data == "Готово")
def handle_interests(call):
    chat_id = call.message.chat.id
    if call.data == 'Готово':
        selected_interests = user_interests.get(chat_id, [])

        if not selected_interests:
            bot.send_message(chat_id, "Вы не выбрали ни одного интереса.")
            return

        for interest in selected_interests:
            interest_events = events.get(interest, [])
            for event in interest_events:
                markup = types.InlineKeyboardMarkup(row_width=2)
                back_button = types.InlineKeyboardButton(text="Назад", callback_data="Назад")
                url_button = types.InlineKeyboardButton(text="Перейти", url=event['url'])
                markup.add(back_button, url_button)

                bot.send_photo(chat_id, open(event['photo'], 'rb'), caption=event['text'], reply_markup=markup)
    else:
        user_interests[chat_id].append(call.data)
        bot.answer_callback_query(call.id, f"Добавлен интерес: {call.data}")


@bot.callback_query_handler(func=lambda call: call.data == "Назад")
def go_back(call):
    start(call.message)


@bot.message_handler(commands=['add_event'])
def add_event(message):
    if message.from_user.username == admin_username:
        params = message.text.split(';')
        if len(params) != 4:
            bot.send_message(message.chat.id,
                             "Пожалуйста, используйте правильный формат: /add_event;Категория;Фото;Описание")
            return

        _, category, photo, description = params
        if category not in events:
            bot.send_message(message.chat.id,
                             "Указанная категория не существует. Доступные категории: " + ', '.join(events.keys()))
            return

        events[category].append({'photo': photo.strip(), 'text': description.strip()})
        bot.send_message(message.chat.id,
                         f"Мероприятие '{description.strip()}' добавлено в категорию '{category.strip()}'.")
    else:
        bot.send_message(message.chat.id, "У вас нет прав для добавления мероприятий.")


bot.polling(non_stop=True)