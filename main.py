import telebot
from telebot import types
from DataBase.dbIndex import DB
from SMTP.index import sendToGmail,ganerateTextForOrder
import time
bot = telebot.TeleBot('5310520335:AAEcU7TtRwtOkS2Ai6yIPcDj1IUgLpOdMVo')
db = DB()

@bot.message_handler(commands=['start'])
def start(message):
    string = f'Привіт, <b>{message.chat.first_name if len(message.chat.first_name) != 0 else message.chat.username}</b>\n' \
             f'Ми раді вітати тебе у нашому боті! Обирай товари у католозі та оформлюй заказ у корзині'
    bot.send_message(message.chat.id, string, parse_mode='html')

    if db.get_customers_by_id(message.from_user.id) == True:
        bot.send_message(message.chat.id, f"{message.chat.first_name}, раді Вас знову вітати у нашому магазині!", reply_markup=my_reply_markup())
    else:
        bot.send_message(message.chat.id, 'Будь-ласка, введіть свою пошту, для реєстрації');
        bot.register_next_step_handler(message, setMail)

@bot.message_handler(commands=['menu'])
def menu(message):
    bot.send_message(message.chat.id,'Обиріть, будь-ласка, товари', reply_markup=my_reply_markup())


def setMail(message):
     # check regEx mail

     cust = {
        "userID": message.from_user.id,
        "userName": message.chat.first_name,
        "userSurname": message.chat.last_name,
        "userUsername": message.chat.username,
        "Mail": message.text
     }
     db.insert_customer(cust)


     bot.send_message(message.chat.id, 'Ви успішно зареєструвалися!!', reply_markup=my_reply_markup())

def my_reply_markup():
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton('🖥️ Каталог'), types.KeyboardButton('🔥 Акційні товари'))
    markup.add(types.KeyboardButton('💁🏻 О нас'), types.KeyboardButton('🗒️ Замовлення'))
    markup.add(types.KeyboardButton('🛒 Кошик'))
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
                    buttons.append([types.InlineKeyboardButton(item['name'], callback_data=str(item['id'])+'_dg')])
            for item in global_category:
                if item['id'] % 2 == 0:
                    buttons[c].append(types.InlineKeyboardButton(item['name'], callback_data=str(item['id'])+'_dg'))
                    c = c+1
            print(buttons)

            bot.send_message(message.chat.id, '\n\n\nОберіть категорію, що вас цікавить', reply_markup=types.InlineKeyboardMarkup(buttons))

        elif message.text == '🛒 Кошик':
            objFromBasket = db.get_basket(message.from_user.id)
            if(objFromBasket != []):
                idsProdFromBasket = objFromBasket[0]['idsProd']
                countsProd = objFromBasket[0]['countsProd'].split(',')

                idsProdFromBasket = 'id = ' + idsProdFromBasket.replace(',', ' or id=')
                str_str = f"<b>Кошик</b>\n\n"
                products = db.get_Product_by_all_id(idsProdFromBasket)
                c = 0
                for item in products:
                    str_str += f"<b>{item['Name']}</b>\t" \
                               f"\n<i><u>{item['Price']} грн.</u></i> x {countsProd[c]}\n" \
                               f"--------------------------------------------------------------------\n"
                    c+=1
                str_str += f"\n<b>Разом: {str(objFromBasket[0]['SumOrder'])} грн.</b>"
                buttons = list()
                buttons.append(
                    [types.InlineKeyboardButton("Редагувати", callback_data=f"{str(objFromBasket[0]['id'])}" + "_red"),
                     types.InlineKeyboardButton("Оформити заказ",
                                                callback_data=f"{str(message.from_user.id)}" + "_ofOrd")])

                bot.send_message(message.chat.id, str_str, parse_mode="html",
                                 reply_markup=types.InlineKeyboardMarkup(buttons))
            else:
                bot.send_message(message.chat.id, 'Ваш кошик порожній.')

        elif message.text == '🔥 Акційні товари':
            Products = db.get_Sale_Product()
            if Products != None:
                for item in Products:
                    if item["countProd"] != 0:
                        try:
                            photoProd = open(
                                f'C:/Users/Владелец/PycharmProjects/TelegramBotElectronic/Data/PhotoProduct/{item["NamePhoto"]}',
                                'rb')
                        except:
                            photoProd = 'https://kebabchef.ua/images/photo_default_1_0.png'
                        strProd = f'\n\n\n<b>{item["Name"]}</b>\n\n' \
                                  f'<b>Характеристики:</b>\n' \
                                  f'<i>{item["Description"]}</i>\n\n' \
                                  f'Стара ціна: <s>{item["Price"]}</s>' \
                                  f'<b>\nАкційна ціна</b> <u>{float(item["Price"]) * float(item["percentSale"])}</u> грн.'

                        buttons = list()
                        buttons.append([types.InlineKeyboardButton('➖', callback_data='_minus'),
                                        types.InlineKeyboardButton('1', callback_data='_count'),
                                        types.InlineKeyboardButton('➕', callback_data='_plus')])
                        buttons.append(
                            [types.InlineKeyboardButton('Додати до кошика', callback_data=f'{item["id"]}_addToBas')])
                        bot.send_photo(message.from_user.id, photoProd, strProd, parse_mode='html',
                                       reply_markup=types.InlineKeyboardMarkup(buttons))

        elif message.text == '💁🏻 О нас':
            bot.send_message(message.chat.id,
                             'Шукаєш магазин, де є все та трішки більше? Тоді Ви звернулися за адресою, так як онлайн-магазин '
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
    if type(dataCall) == type('') and '_dg' in dataCall:
        call_str = dataCall.split('_dg')[0]
        categoryProd = db.get_CategoryProd(call_str)
        buttons = list()
        secondFor = 0
        firstFor = 0
        for item in categoryProd:
            if item['id'] % 2 == 0:
                firstFor += 1
                buttons.append([types.InlineKeyboardButton(item['name'], callback_data=str(item['id']) + '_dp')])

        for item in categoryProd:
            if item['id'] % 2 != 0:
                if secondFor < firstFor:
                    buttons[secondFor].append(types.InlineKeyboardButton(item['name'], callback_data=str(item['id']) + '_dp'))
                else:
                    buttons.append([types.InlineKeyboardButton(item['name'], callback_data=str(item['id'])+'_dp')])
                secondFor = secondFor + 1
        bot.send_message(call.from_user.id, 'Оберіть категорію товару, що вас цікавить', reply_markup=types.InlineKeyboardMarkup(buttons))
    elif type(dataCall) == type('') and '_dp' in dataCall:
            call_str = dataCall.split('_dp')[0]
            Products = db.get_Product(call_str)
            if Products != None:
                for item in Products:
                    if item["countProd"] != 0:
                        try:
                            photoProd = open(
                                f'C:/Users/Владелец/PycharmProjects/TelegramBotElectronic/Data/PhotoProduct/{item["NamePhoto"]}',
                                'rb')
                        except:
                            photoProd = 'https://kebabchef.ua/images/photo_default_1_0.png'
                        strProd = f'\n\n\n<b>{item["Name"]}</b>\n\n' \
                                  f'<b>Характеристики:</b>\n' \
                                  f'<i>{item["Description"]}</i>\n' \
                                  f'<b>\nЦіна</b> <u>{item["Price"]}</u> грн.'

                        buttons = list()
                        buttons.append([types.InlineKeyboardButton('➖', callback_data=f'1_{item["id"]}_minus'),
                                        types.InlineKeyboardButton('1', callback_data='_countProducts'),
                                        types.InlineKeyboardButton('➕', callback_data=f'1_{item["id"]}_plus')])
                        buttons.append([types.InlineKeyboardButton('Додати до кошика', callback_data=f'1_{item["id"]}_addToBas')])
                        bot.send_photo(call.from_user.id, photoProd, strProd, parse_mode='html', reply_markup=types.InlineKeyboardMarkup(buttons))

            else:
                bot.send_message(call.from_user.id, 'На жаль, у цій категорії зараз немає товарів 😓', parse_mode='html')
    elif type(dataCall) == type('') and '_addToBas' in dataCall:

        call_str = dataCall.split('_addToBas')[0]
        count = call_str.split('_')[0]
        call_str = call_str.split('_')[1]

        Product = db.get_Product_by_id(call_str)

        setUserBasket(call.from_user.id, Product, count)
        bot.send_message(call.from_user.id, 'Товар додано до кошика✅')

    elif type(dataCall) == type('') and '_plus' in dataCall:
        call_str = dataCall.split('_plus')[0]
        strpuk = call_str.split('_')[0]
        call_str = call_str.split('_')[1]
        Product = db.get_Product_by_id(call_str)[0]


        str_prod = f'\n\n\n<b>{Product["Name"]}</b>\n\n' \
        f'<b>Характеристики:</b>\n' \
        f'<i>{Product["Description"]}</i>\n' \
        f'<b>\nЦіна</b> <u>{Product["Price"]}</u> грн.'



        if Product['countProd'] >= int(strpuk):
            count = str(int(strpuk) + 1)
        else:
            count = strpuk
            str_prod += '\n\nТовар закінчився на складі'


        if Product['countProd'] - 1 == strpuk:
            str_prod += f"\n\nВ наявності {Product['countProd']}"

        buttons = list()
        buttons.append([types.InlineKeyboardButton('➖', callback_data=f'{count}_{Product["id"]}_minus'),
                        types.InlineKeyboardButton(count, callback_data='_countProducts'),
                        types.InlineKeyboardButton('➕', callback_data=f'{count}_{Product["id"]}_plus')])
        buttons.append([types.InlineKeyboardButton('Додати до кошика', callback_data=f'{count}_{Product["id"]}_addToBas')])

        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.id, caption=str_prod, parse_mode='html')
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=types.InlineKeyboardMarkup(buttons))

    elif type(dataCall) == type('') and '_minus' in dataCall:
        call_str = dataCall.split('_minus')[0]
        strpuk = call_str.split('_')[0]
        call_str = call_str.split('_')[1]
        Product = db.get_Product_by_id(call_str)[0]

        count = str(str(int(strpuk) if(int(strpuk)==1)else int(strpuk) - 1 ))
        str_prod = f'\n\n\n<b>{Product["Name"]}</b>\n\n' \
        f'<b>Характеристики:</b>\n' \
        f'<i>{Product["Description"]}</i>\n' \
        f'<b>\nЦіна</b> <u>{Product["Price"]}</u> грн.'

        buttons = list()
        buttons.append([types.InlineKeyboardButton('➖', callback_data=f'{count}_{Product["id"]}_minus'),
                        types.InlineKeyboardButton(count, callback_data='_countProducts'),
                        types.InlineKeyboardButton('➕', callback_data=f'{count}_{Product["id"]}_plus')])
        buttons.append([types.InlineKeyboardButton('Додати до кошика', callback_data=f'{count}_{Product["id"]}_addToBas')])

        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.id, caption=str_prod, parse_mode='html')
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=types.InlineKeyboardMarkup(buttons))

    elif type(dataCall) == type('') and '_ofOrd' in dataCall:

        idCust = dataCall.split('_ofOrd')[0]

        basket = db.get_basket(idCust)[0]
        msg = bot.send_message(idCust, 'Вкажіть місто в яке буде доставка')
        bot.register_next_step_handler(msg, setCity,basket,idCust)




def setUserBasket(idCust, itemProduct, count):
    print(itemProduct)
    prodFromBasket = db.get_basket(idCust)

    if len(prodFromBasket) != 0:
        basket = {
            "idsProd": str(prodFromBasket[0]['idsProd'])+str(",") + str(itemProduct[0]['id']),
            "countsProd": str(prodFromBasket[0]['countsProd']) + str(",") + str(count),
            "SumOrder": float(prodFromBasket[0]['SumOrder'])+float(float(itemProduct[0]['Price'])*float(count))
        }
        db.update_basket(idCust, basket)
    else:

        basket = {
            "idCust": idCust,
            "idsProd": itemProduct[0]['id'],
            "SumOrder": float(float(itemProduct[0]['Price'])*float(count)),
            "countsProd": str(count),
        }
        print(basket)
        db.insert_Basket(basket)

def setCity(message,basket,idCust):
    city = message.text
    print(city)
    msg2 = bot.send_message(idCust, 'Введіть свій номер телефону.')
    bot.register_next_step_handler(msg2, setPhone, city,basket,idCust)

def setPhone(message,city,basket,idCust):
    phone = message.text
    print(phone)
    msg3 = bot.send_message(idCust, 'Введіть номер нової пошти на яку відправляти посилку.')
    bot.register_next_step_handler(msg3, setNp, city, phone,basket,idCust)

def setNp(message,city, phone,basket, idCust):
    np = message.text
    print(np)
    print(city)
    print(phone)
    print(basket)

    order = {
        'idCust': idCust,
        'idsProd': basket['idsProd'],
        'countProd': basket['countsProd'],
        'City': city,
        'AdressNP': np,
        'SumOrder': basket['SumOrder'],
        'Phone': phone
    }
    db.insert_orders(order)
    db.delete_Basket_by_idCust(idCust)
    cust = db.get_customers_mail(idCust)[0]
    print(cust)
    sendToGmail(cust['mail'], ganerateTextForOrder(order).as_string())
    bot.send_message(idCust, 'Ви успішно оформили свій заказ!.')



























bot.polling(none_stop=True, interval=0)

