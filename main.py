import telebot
from telebot import types
from DataBase.dbIndex import DB


bot = telebot.TeleBot('5310520335:AAEcU7TtRwtOkS2Ai6yIPcDj1IUgLpOdMVo')
db = DB()

@bot.message_handler(commands=['start'])
def start(message):
    string = f'Привіт, <b>{message.chat.first_name if len(message.chat.first_name) != 0 else message.chat.username}</b>\n' \
             f'Ми раді вітати тебе у нашому боті! Оберай товари у католозі та оформлюй заказ у корзині'
    bot.send_message(message.chat.id, string, parse_mode='html')

    if db.get_customers_by_id(message.from_user.id) == True:
        bot.send_message(message.chat.id, f"{message.chat.first_name}, раді Вас знову вітати у нашому магазині!", reply_markup=my_reply_markup())
    else:
        bot.send_message(message.chat.id, 'Будь-ласка, введіть свій номер телефону, для реєстрації');
        bot.register_next_step_handler(message, setPhoneNumber)


def setPhoneNumber(message):
     # check regEx phone Number

     cust = {
        "userID": message.from_user.id,
        "userName": message.chat.first_name,
        "userSurname": message.chat.last_name,
        "userUsername": message.chat.username,
        "userPhone": message.text
     }
     db.insert_customer(cust)


     bot.send_message(message.chat.id, 'Ви успішно зареєструвалися!!', reply_markup=my_reply_markup())

def my_reply_markup():
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton('🖥️ Каталог'), types.KeyboardButton('🔥 Акційні товари'))
    markup.add(types.KeyboardButton('💁🏻 О нас'), types.KeyboardButton('🗒️ Замовлення'))
    markup.add(types.KeyboardButton('🛒 Корзина'))
    return markup

@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == '🖥️ Каталог':
            global_category = db.get_Global_Category()
            buttons = list()
            c=0

            for item in global_category:
                if item['id'] % 2 != 0:
                    buttons.append([types.InlineKeyboardButton(item['name'], callback_data=item['name']+'_dataGlobal')])
            for item in global_category:
                if item['id'] % 2 == 0:
                    buttons[c].append(types.InlineKeyboardButton(item['name'], callback_data=item['name']+'_dataGlobal'))
                    c = c+1
            print(buttons)

            bot.send_message(message.chat.id, 'Оберіть категорію, що вас цікавить', reply_markup=types.InlineKeyboardMarkup(buttons))
        elif message.text == '🔥 Акційні товари':
            bot.send_message(message.chat.id, 'TOVARI PO ACSII')
        elif message.text == '💁🏻 О нас':
            bot.send_message(message.chat.id, 'Шукаєш магазин, де є все та трішки більше? Тоді Ви звернулися за адресою, так як онлайн-магазин '
                                              '<b>Technique4You</b> допомогає покупцеві знайти, порівняти і визначитися з вибором товару та оформити покупку. \n'
                                          '\n<u><b>Переваги співпраці з нами:</b></u>\n\n'
                                          '1. Стабільний графік високої якості.⚖\n'
                                          '2. Краща геополітика. Ми можемо надіслати товар у будь-який куточок світу.📬\n'
                                          '3. Повна прозорість та зручність роботи.📊\n'
                                          '4. Найбільша і лояльна аудиторія.👨‍👩‍👧‍👧\n'
                                          '5. Найповніший і функціональний каталог товарів.✅\n'
                                          '6. Technique4You довіряють.🤍', parse_mode='html')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    dataCall = call.data
    if type(dataCall) == type('') and '_dataGlobal' in dataCall:
        call_str = dataCall.split('_dataGlobal')[0]
        categoryProd = db.get_CategoryProd(call_str)
        buttons = list()
        c = 0
        for item in categoryProd:
            if item['id'] % 2 != 0:
                buttons.append([types.InlineKeyboardButton(item['name'], callback_data=item['name'] + '_data')])
        for item in categoryProd:
            if item['id'] % 2 == 0:
                buttons[c].append(types.InlineKeyboardButton(item['name'], callback_data=item['name'] + '_data'))
                c = c + 1
        print(buttons)
        bot.send_message(call.from_user.id, 'Оберіть категорію товару, що вас цікавить', reply_markup=types.InlineKeyboardMarkup(buttons))




bot.polling(none_stop=True, interval=0)

