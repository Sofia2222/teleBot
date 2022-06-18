import telebot
from telebot import types
from DataBase.dbIndex import DB
from SMTP.index import sendToGmail,ganerateTextForOrder
from classes.productClass import Product, crudOperation
from classes.userClass import User
from classes.Orders import Orders
from api.novaya_poshta import NovaPoshta
from classes.basketClass import Basket
from classes.categoryClass import categoryProd
from classes.categoryGlobalProd import categoryGlobalProd

import time
bot = telebot.TeleBot('5310520335:AAEcU7TtRwtOkS2Ai6yIPcDj1IUgLpOdMVo')

userObj = User()
orderObj = Orders()
productObj = Product()
basketObj = Basket()
npObj = NovaPoshta()
categoryObj = categoryProd()
categoryGlobObj = categoryGlobalProd()


@bot.message_handler(commands=['start'])
def start(message):
    string = f'Привіт, <b>{message.chat.first_name if len(message.chat.first_name) != 0 else message.chat.username}</b>\n' \
             f'Ми раді вітати тебе у нашому боті! Обирай товари у католозі та оформлюй заказ у корзині'
    bot.send_message(message.chat.id, string, parse_mode='html')

    if len(userObj.SQLQuery(crudOperation.Select, "*", f'id = {message.from_user.id}', {})) != 0:
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
     userObj.SQLQuery(crudOperation.Insert, '', '', cust)
     bot.send_message(message.chat.id, 'Ви успішно зареєструвалися!!', reply_markup=my_reply_markup())

def my_reply_markup():
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton('🖥️ Каталог'), types.KeyboardButton('🔥 Акційні товари'))
    markup.add(types.KeyboardButton('💁🏻 Співпраця з нами'), types.KeyboardButton('🗒️ Замовлення'))
    markup.add(types.KeyboardButton('🛒 Кошик'))
    return markup

@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == '🖥️ Каталог':
            global_category = categoryGlobObj.SQLQuery(crudOperation.Select, '*', '')
            buttons = list()
            c=0

            for item in global_category:
                if item.id % 2 != 0:
                    buttons.append([types.InlineKeyboardButton(item.Name, callback_data=str(item.id)+'_dg')])
            for item in global_category:
                if item.id % 2 == 0:
                    buttons[c].append(types.InlineKeyboardButton(item.Name, callback_data=str(item.id)+'_dg'))
                    c = c+1
            print(buttons)

            bot.send_message(message.chat.id, '\n\n\nОберіть категорію, що вас цікавить', reply_markup=types.InlineKeyboardMarkup(buttons))

        elif message.text == '🛒 Кошик':
            objFromBasket = basketObj.SQLQuery(crudOperation.Select, '*', f'idCust = {message.from_user.id}',
                                               {})
            if(objFromBasket != []):
                idsProdFromBasket = objFromBasket[0].idsProd
                countsProd = objFromBasket[0].countsProd.split(',')

                idsProdFromBasket = 'id = ' + idsProdFromBasket.replace(',', ' or id=')
                str_str = f"<b>Кошик</b>\n\n"
                products = productObj.SQLQuery(crudOperation.Select, '*', idsProdFromBasket)
                c = 0
                for item in products:
                    str_str += f"<b>{item.Name}</b>\t" \
                               f"\n<i><u>{item.Price if (item.isSale == 0) else float(item.Price) * float(item.percentSale)} грн.</u></i> x {countsProd[c]}\n" \
                               f"--------------------------------------------------------------------\n"
                    c+=1
                str_str += f"\n<b>Разом: {str(objFromBasket[0].SumOrder)} грн.</b>"
                buttons = list()
                buttons.append(
                    [types.InlineKeyboardButton("Редагувати", callback_data=f"{str(message.from_user.id)}_red"),
                     types.InlineKeyboardButton("Оформити замовлення",
                                                callback_data=f"{str(message.from_user.id)}" + "_ofOrd")])

                bot.send_message(message.chat.id, str_str, parse_mode="html",
                                 reply_markup=types.InlineKeyboardMarkup(buttons))
            else:
                bot.send_message(message.chat.id, 'Ваш кошик порожній.')

        elif message.text == '🔥 Акційні товари':
            prods = productObj.SQLQuery(crudOperation.Select, '*', ' isSale = TRUE')
            if prods != None:
                for item in prods:
                    if item.countProd != 0:
                        try:
                            photoProd = open(
                                f'C:/Users/Владелец/PycharmProjects/TelegramBotElectronic/Data/PhotoProduct/{item.NamePhoto}',
                                'rb')
                        except:
                            photoProd = 'https://kebabchef.ua/images/photo_default_1_0.png'
                        strProd = f'\n\n\n<b>{item.Name}</b>\n\n' \
                                  f'<b>Характеристики:</b>\n' \
                                  f'<i>{item.Description}</i>\n\n' \
                                  f'Стара ціна: <s>{item.Price}</s>' \
                                  f'<b>\nАкційна ціна</b> <u>{float(item.Price) * float(item.percentSale)}</u> грн.'

                        buttons = list()
                        buttons.append([types.InlineKeyboardButton('➖', callback_data=f'1_{item.id}_minus'),
                                        types.InlineKeyboardButton('1', callback_data='_count'),
                                        types.InlineKeyboardButton('➕', callback_data=f'1_{item.id}_plus')])
                        buttons.append(
                            [types.InlineKeyboardButton('Додати до кошика', callback_data=f'1_{item.id}_addToBas')])
                        bot.send_photo(message.from_user.id, photoProd, strProd, parse_mode='html',
                                       reply_markup=types.InlineKeyboardMarkup(buttons))

        elif message.text == '💁🏻 Співпраця з нами':
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
            bot.send_message(message.chat.id, "<b>Оплата товарів</b>\n"
                                              "<u>Оплата товарів та послуг здійснюється на розрахунковий рахунок, який надсилається замовнику на електронну пошту у вигляді накладної з замовленням, де він вказаний</u>", parse_mode='html')
            bot.send_message(message.chat.id, "<b>Зворотній зв'язок.</b> \n\n"
                                              "<i>Відділ по роботі з інтернет-магазином:</i>\n"
                                              "Тел. (099) 646-77-99\n"
                                              "E-mail: billing@technique4you.ua\n\n"
                                              "<i>Відділ обробки товарних фідів:</i> \n"
                                              "Тел. (098) 886-16-34\n"
                                              "E-mail: pricelist@technique4you.ua\n\n"
                                              "<i>Редакція каталогів:</i>\n"
                                              "Тел. (098) 789-23-76\n\n"
                                              "<i>Відділ маркетингу:</i>\n"
                                              "Тел. (068) 716-37-89, (098) 629-73-89\n\n"
                                              "<i>Відділ реклами:</i>\n"
                                              "Тел. (073) 678-21-70\n"
                                              "E-mail: ads@technique4you.ua)\n", parse_mode='html')

        elif message.text == '🗒️ Замовлення':
            orderslist = orderObj.SQLQuery(crudOperation.Select, "*", f'idCust = {message.from_user.id}', {})
            print(orderslist)
            if len(orderslist) != 0:

                for item in orderslist:
                    strr = f'Номер замовлення № {item.id}'
                    idsProdForItem = 'id = ' + item.idsProd.replace(',', ' or id=')
                    products = productObj.SQLQuery(crudOperation.Select, '*', idsProdForItem)
                    c = 0
                    countsProd = item.countProd.split(',')
                    for itemProd in products:
                        strr += f"\n<b>{itemProd.Name}</b>\t" \
                                   f"\n<i><u>{itemProd.Price} грн.</u></i> x {countsProd[c]}\n" \
                                   f"--------------------------------------------------------------------\n"
                        c += 1
                    strr += f"\n<b>Разом: {str(item.SumOrder)} грн.</b>"
                    bot.send_message(message.from_user.id, strr, parse_mode='html')
            else:
                bot.send_message(message.from_user.id, 'У Вас немає замовлень')

        elif message.text == 'Зберегти кошик':
            bot.send_message(message.from_user.id, 'Збережено✅', reply_markup=my_reply_markup())


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    dataCall = call.data
    if type(dataCall) == type('') and '_dg' in dataCall:
        call_str = dataCall.split('_dg')[0]
        categoryProd = categoryObj.SQLQuery(crudOperation.Select, '*', f'idGlobalCategory = {int(call_str)}')
        buttons = list()
        secondFor = 0
        firstFor = 0
        for item in categoryProd:
            if item.id % 2 == 0:
                firstFor += 1
                buttons.append([types.InlineKeyboardButton(item.Name, callback_data=str(item.id) + '_dp')])

        for item in categoryProd:
            if item.id % 2 != 0:
                if secondFor < firstFor:
                    buttons[secondFor].append(types.InlineKeyboardButton(item.Name, callback_data=str(item.id) + '_dp'))
                else:
                    buttons.append([types.InlineKeyboardButton(item.Name, callback_data=str(item.id)+'_dp')])
                secondFor = secondFor + 1
        bot.send_message(call.from_user.id, 'Оберіть категорію товару, що вас цікавить', reply_markup=types.InlineKeyboardMarkup(buttons))
    elif type(dataCall) == type('') and '_dp' in dataCall:
            call_str = dataCall.split('_dp')[0]
            Products = productObj.SQLQuery(crudOperation.Select, '*', f'CategoryId = {int(call_str)}')
            if Products != None:
                for item in Products:
                    if item.countProd != 0:
                        try:
                            photoProd = open(
                                f'C:/Users/Владелец/PycharmProjects/TelegramBotElectronic/Data/PhotoProduct/{item.NamePhoto}',
                                'rb')
                        except:
                            photoProd = 'https://kebabchef.ua/images/photo_default_1_0.png'
                        strProd = f'\n\n\n<b>{item.Name}</b>\n\n' \
                                  f'<b>Характеристики:</b>\n' \
                                  f'<i>{item.Description}</i>\n' \
                                  f'<b>\nЦіна</b> <u>{item.Price}</u> грн.'

                        buttons = list()
                        buttons.append([types.InlineKeyboardButton('➖', callback_data=f'1_{item.id}_minus'),
                                        types.InlineKeyboardButton('1', callback_data='_countProducts'),
                                        types.InlineKeyboardButton('➕', callback_data=f'1_{item.id}_plus')])
                        buttons.append([types.InlineKeyboardButton('Додати до кошика', callback_data=f'1_{item.id}_addToBas')])
                        bot.send_photo(call.from_user.id, photoProd, strProd, parse_mode='html', reply_markup=types.InlineKeyboardMarkup(buttons))

            else:
                bot.send_message(call.from_user.id, 'На жаль, у цій категорії зараз немає товарів 😓', parse_mode='html')
    elif type(dataCall) == type('') and '_addToBas' in dataCall:

        call_str = dataCall.split('_addToBas')[0]
        count = call_str.split('_')[0]
        call_str = call_str.split('_')[1]
        print(call_str, 'y')
        Product = productObj.SQLQuery(crudOperation.Select, '*', f'id = {call_str}')

        setUserBasket(call.from_user.id, Product, count)
        bot.send_message(call.from_user.id, 'Товар додано до кошика✅')

    elif type(dataCall) == type('') and '_plus' in dataCall or '_Rplus' in dataCall:
        print(dataCall)
        if '_plus' in dataCall:
            operationPlus = 'Додати до кошика'
            operationPlusM = '_plus'
            operationMinus = '_minus'
            operationDataCall = '_addToBas'
        elif '_Rplus' in dataCall:
            operationPlus = 'Видалити з кошика'
            operationPlusM = '_Rplus'
            operationMinus = '_Rminus'
            operationDataCall = '_deleteFromBask'

        call_str = dataCall.split('_plus')[0]
        strpuk = call_str.split('_')[0]
        call_str = call_str.split('_')[1]
        Product = productObj.SQLQuery(crudOperation.Select, '*', f'id = {call_str}')[0]

        str_prod = f'\n\n\n<b>{Product.Name}</b>\n\n' \
        f'<b>Характеристики:</b>\n' \
        f'<i>{Product.Description}</i>\n' \
        f'<b>\nЦіна</b> <u>{Product.Price}</u> грн.'


        if Product.countProd >= int(strpuk):
            count = str(int(strpuk) + 1)
        else:
            count = strpuk
            str_prod += '\n\nТовар закінчився на складі'

        if Product.countProd - 1 == strpuk:
            str_prod += f"\n\nВ наявності {Product.countProd}"

        if '_Rplus' in dataCall:
            basket = basketObj.SQLQuery(crudOperation.Select, '*', f'idCust = {call.from_user.id}', {})[0]
            print(basket, 'rplus')
            print(dataCall, 'rplus')
            countsProd = basket.countsProd.split(',')
            idsProd = basket.idsProd.split(',')

            counterForBasket = 0

            for item in idsProd:
                if str(Product.id) == item:
                    countsProd[counterForBasket] = str(count)
                counterForBasket+=1
            symbolForList = ','
            countsProd = symbolForList.join(countsProd)
            countsIdsProd = symbolForList.join(idsProd)

            basketToUpdate = {
                "idCust": call.from_user.id,
                "idsProd": countsIdsProd,
                "countsProd": countsProd,
                "SumOrder": float(basket.SumOrder)+float(float(Product.Price))
            }
            basketObj.SQLQuery(crudOperation.Update, '', '', basketToUpdate)
        buttons = list()
        buttons.append([types.InlineKeyboardButton('➖', callback_data=f'{count}_{Product.id}{operationMinus}'),
                        types.InlineKeyboardButton(count, callback_data='_countProducts'),
                        types.InlineKeyboardButton('➕', callback_data=f'{count}_{Product.id}{operationPlusM}')])
        buttons.append([types.InlineKeyboardButton(operationPlus, callback_data=f'{count}_{Product.id}{operationDataCall}')])

        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.id, caption=str_prod, parse_mode='html')
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=types.InlineKeyboardMarkup(buttons))

    elif type(dataCall) == type('') and '_minus' in dataCall or '_Rminus' in dataCall:
        if '_minus' in dataCall:
            operationMinus = 'Додати до кошика'
            operationPlus = '_plus'
            operationMinusP = '_minus'
            operationDataCall = '_addToBas'
        elif '_Rminus' in dataCall:
            operationMinus = 'Видалити з кошика'
            operationPlus = '_Rplus'
            operationMinusP = '_Rminus'
            operationDataCall = '_deleteFromBask'

        call_str = dataCall.split('_minus')[0]
        strpuk = call_str.split('_')[0]
        call_str = call_str.split('_')[1]
        Product = productObj.SQLQuery(crudOperation.Select, '*', f'id = {call_str}')[0]
        print(Product)

        count = str(str(int(strpuk) if(int(strpuk)==1)else int(strpuk) - 1 ))
        str_prod = f'\n\n\n<b>{Product.Name}</b>\n\n' \
        f'<b>Характеристики:</b>\n' \
        f'<i>{Product.Description}</i>\n' \
        f'<b>\nЦіна</b> <u>{Product.Price}</u> грн.'

        if '_Rminus' in dataCall:
            basket = basketObj.SQLQuery(crudOperation.Select, '*', f'idCust = {call.from_user.id}', {})[0]
            print(basket)
            print(dataCall)
            countsProd = basket.countsProd.split(',')
            idsProd = basket.idsProd.split(',')

            counterForBasket = 0

            for item in idsProd:
                if str(Product.id) == item:
                    countsProd[counterForBasket] = str(count)
                counterForBasket += 1
            symbolForList = ','
            countsProd = symbolForList.join(countsProd)
            countsIdsProd = symbolForList.join(idsProd)

            basketToUpdate = {
                "idCust": call.from_user.id,
                "idsProd": countsIdsProd,
                "countsProd": countsProd,
                "SumOrder": float(basket.SumOrder) - float(float(Product.Price))
            }
            basketObj.SQLQuery(crudOperation.Update, '', '', basketToUpdate)

        buttons = list()
        buttons.append([types.InlineKeyboardButton('➖', callback_data=f'{count}_{Product.id}{operationMinusP}'),
                        types.InlineKeyboardButton(count, callback_data='_countProducts'),
                        types.InlineKeyboardButton('➕', callback_data=f'{count}_{Product.id}{operationPlus}')])
        buttons.append([types.InlineKeyboardButton(operationMinus, callback_data=f'{count}_{Product.id}{operationDataCall}')])

        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.id, caption=str_prod, parse_mode='html')
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=types.InlineKeyboardMarkup(buttons))

    elif type(dataCall) == type('') and '_ofOrd' in dataCall:

        idCust = dataCall.split('_ofOrd')[0]

        basket = basketObj.SQLQuery(crudOperation.Select, '*', f'idCust = {idCust}', {})[0]
        msg = bot.send_message(idCust, 'Вкажіть місто для доставки')
        bot.register_next_step_handler(msg, setCity,basket,idCust)

    elif type(dataCall) == type('') and '_red' in dataCall:
        idCust = dataCall.split('_red')[0]
        print(0000)
        objFromBasket = basketObj.SQLQuery(crudOperation.Select, '*', f'idCust = {idCust}', {})
        print(objFromBasket)
        if (objFromBasket != []):
            idsProdFromBasket = objFromBasket[0].idsProd
            countsProd = objFromBasket[0].countsProd.split(',')

            idsProdFromBasket = 'id = ' + idsProdFromBasket.replace(',', ' or id=')
            print(idsProdFromBasket, 'red')
            str_str = f"<b>Кошик</b>\n\n"
            products = productObj.SQLQuery(crudOperation.Select, '*', f'{idsProdFromBasket}', 'no')

            c = 0
            for item in products:
                print(item.id)
                if item.countProd != 0:
                    try:
                        photoProd = open(
                            f'C:/Users/Владелец/PycharmProjects/TelegramBotElectronic/Data/PhotoProduct/{item.NamePhoto}',
                            'rb')
                    except:
                        photoProd = 'https://kebabchef.ua/images/photo_default_1_0.png'
                    strProd = f'\n\n\n<b>{item.Name}</b>\n\n' \
                              f'<b>Характеристики:</b>\n' \
                              f'<i>{item.Description}</i>\n' \
                              f'<b>\nЦіна</b> <u>{item.Price}</u> грн.'

                    buttons = list()
                    buttons.append([types.InlineKeyboardButton('➖', callback_data=f'{countsProd[c]}_{item.id}_Rminus'),
                                    types.InlineKeyboardButton(countsProd[c], callback_data='_countProducts'),
                                    types.InlineKeyboardButton('➕', callback_data=f'{countsProd[c]}_{item.id}_Rplus')])
                    buttons.append(
                        [types.InlineKeyboardButton('Видалити з кошика', callback_data=f'{countsProd[c]}_{item.id}_deleteFromBask')])
                    c += 1
                    bot.send_photo(call.from_user.id, photoProd, strProd, parse_mode='html',
                                   reply_markup=types.InlineKeyboardMarkup(buttons))

            markup = types.ReplyKeyboardMarkup()
            markup.add(types.KeyboardButton('Зберегти кошик'))
            bot.send_message(idCust, 'При закінчинні редагування кошика, натисніть <i><b>Зберегти кошик</b></i>', parse_mode='html', reply_markup=markup)

    elif type(dataCall) == type('') and '_deleteFromBask' in dataCall:
        call_str = dataCall.split('_deleteFromBask')[0]
        count = call_str.split('_')[0]
        idProduct = call_str.split('_')[1]
        Product = productObj.SQLQuery(crudOperation.Select, '*', f'id = {idProduct}')[0]
        basket = basketObj.SQLQuery(crudOperation.Select, '*', f'idCust = {call.from_user.id}', {})[0]
        print(basket)
        print(dataCall)
        countsProd = basket.countsProd.split(',')
        idsProd = basket.idsProd.split(',')

        counterForBasket = 0

        for item in idsProd:
            if str(Product.id) == item:
                del countsProd[counterForBasket]
                del idsProd[counterForBasket]
            counterForBasket += 1
        symbolForList = ','
        countsProd = symbolForList.join(countsProd)
        countsIdsProd = symbolForList.join(idsProd)
        if countsProd == '' and countsIdsProd == '':
            basketObj.SQLQuery(crudOperation.Delete, '', f'idCust = {call.from_user.id}', {})
        else:
            basketToUpdate = {
                "idCust": call.message.chat.id,
                "idsProd": countsIdsProd,
                "countsProd": countsProd,
                "SumOrder": float(basket.SumOrder) - float(float(Product.Price)*float(count))
            }
            basketObj.SQLQuery(crudOperation.Update, '', '', basketToUpdate)
        bot.delete_message(call.message.chat.id, call.message.id)

    elif type(dataCall) == type('') and '_np' in dataCall:
        idNP = dataCall.split('_np')[0]
        print(idNP)
        itemNP = npObj.dataCity[int(idNP)]

        npObj.setAll(modelName='Address',
                                 calledMethod='getWarehouses',
                                 methodProperties = {
                                     "CityRef": itemNP['Ref']
                                 })
        npObj.response()
        print(len(npObj.dataNP))
        if len(npObj.dataNP) == 0 or len(npObj.dataNP) >= 50:
            msg3 = bot.send_message(call.from_user.id, 'Введіть номер нової пошти на яку відправляти посилку.')
            bot.register_next_step_handler(msg3, setNovaposhta, itemNP, call.from_user.id)
        else:
            buttons = list()
            secondFor = 0
            firstFor = 0
            counter = 0
            for item in npObj.dataNP:
                if counter % 2 == 0:
                    firstFor += 1
                    buttons.append([types.InlineKeyboardButton(item['Description'], callback_data=f'{idNP}_{counter}_Whousenp')])
                counter += 1
            counter = 0
            for item in npObj.dataNP:
                if counter % 2 != 0:
                    if secondFor < firstFor:
                        buttons[secondFor].append(
                            types.InlineKeyboardButton(item['Description'], callback_data=f'{idNP}_{counter}_Whousenp'))
                    else:
                        buttons.append([types.InlineKeyboardButton(item['Description'], callback_data=f'{idNP}_{counter}_Whousenp')])
                    secondFor = secondFor + 1
                counter += 1

            bot.send_message(call.from_user.id, 'Оберіть Ваше місто/село', reply_markup=types.InlineKeyboardMarkup(buttons))

    elif type(dataCall) == type('') and '_Whousenp' in dataCall:
         idWarehouse = dataCall.split('_Whousenp')[0].split('_')[0]
         idCity = dataCall.split('_Whousenp')[0].split('_')[1]
         print(idWarehouse, idCity, 'np')
         itemNPWareHouse = npObj.dataCity[int(idWarehouse)]
         itemNPCity = npObj.dataNP[int(idCity)]
         basket = basketObj.SQLQuery(crudOperation.Select, '*', f'idCust = {call.from_user.id}', {})[0]
         order = {
             'idCust': call.from_user.id,
             'idsProd': basket.idsProd,
             'countProd': basket.countsProd,
             'City': itemNPWareHouse['Description'],
             'AdressNP': itemNPCity['Description'],
             'SumOrder': basket.SumOrder,
             'Phone': ''
         }
         print(order)
         orderObj.SQLQuery(crudOperation.Insert, '', '', order)
         basketObj.SQLQuery(crudOperation.Delete, '', f'idCust = {call.from_user.id}', {})
         msg4 = bot.send_message(call.from_user.id, 'Введіть ваш номер телефону.')
         bot.register_next_step_handler(msg4, setPhone, order)

def setUserBasket(idCust, itemProduct, count):
    print(itemProduct)
    prodFromBasket = basketObj.SQLQuery(crudOperation.Select, '*', f'idCust = {idCust}', {})
    print(itemProduct, 'kj')
    if len(prodFromBasket) != 0:
        basket = {
            "idCust": idCust,
            "idsProd": str(prodFromBasket[0].idsProd)+str(",") + str(itemProduct[0].id),
            "countsProd": str(prodFromBasket[0].countsProd) + str(",") + str(count),
            "SumOrder": float(prodFromBasket[0].SumOrder)+float(float(itemProduct[0].Price)*float(count)) if (itemProduct[0].isSale == 0) else float(prodFromBasket[0].SumOrder)+float((float(itemProduct[0].Price) * float(itemProduct[0].percentSale))*float(count))
        }
        basketObj.SQLQuery(crudOperation.Update, '', '', basket)
    else:

        basket = {
            "idCust": idCust,
            "idsProd": itemProduct[0].id,
            "SumOrder": float(float(itemProduct[0].Price)*float(count)),
            "countsProd": str(count),
        }
        print(basket)
        basketObj.SQLQuery(crudOperation.Insert, '', '', basket)

def setCity(message,basket,idCust):
    city = message.text
    print(city)
    npObj.setAll(modelName='Address',
                 calledMethod='getCities',
                 methodProperties={
                    "FindByString": city
                 })
    npObj.response()
    cityNP = list()

    for item in npObj.dataCity:
        cityNP.append(item['SettlementTypeDescription'] + ' ' + item['Description'])
    print(cityNP)
    buttons = list()

    secondFor = 0
    firstFor = 0
    counter = 0
    for item in cityNP:
        if counter % 2 == 0:
            firstFor += 1
            buttons.append([types.InlineKeyboardButton(item, callback_data= f'{counter}_np')])
        counter += 1
    counter = 0
    for item in cityNP:
        if counter % 2 != 0:
            if secondFor < firstFor:
                buttons[secondFor].append(
                    types.InlineKeyboardButton(item, callback_data=f'{counter}_np'))
            else:
                buttons.append([types.InlineKeyboardButton(item, callback_data=f'{counter}_np')])
            secondFor = secondFor + 1
        counter+=1

    bot.send_message(idCust, 'Оберіть Ваше місто/село🏙️', reply_markup=types.InlineKeyboardMarkup(buttons))
    #bot.register_next_step_handler(msg2, setPhone, city,basket,idCust)

def setNovaposhta(message, itemNP, idCust):
    np = message.text
    basket = basketObj.SQLQuery(crudOperation.Select, '*', f'idCust = {idCust}', {})[0]
    order = {
        'idCust': idCust,
        'idsProd': basket.idsProd,
        'countProd': basket.countsProd,
        'City': itemNP['Description'],
        'AdressNP': np,
        'SumOrder': basket.SumOrder,
        'Phone': ''
    }
    print(order)
    orderObj.SQLQuery(crudOperation.Insert, '', '', order)
    basketObj.SQLQuery(crudOperation.Delete, '', f'idCust = {idCust}', {})

    msg4 = bot.send_message(idCust, 'Введіть ваш номер телефону.')
    bot.register_next_step_handler(msg4, setPhone, order)

def setPhone(message, order):
    print(message)
    orderObj.SQLQuery(crudOperation.Update, '' ,'' ,{'Phone': message.text, 'idCust': message.from_user.id})
    cust = userObj.SQLQuery(crudOperation.Select, '*', f'id = {message.from_user.id}', {})[0]
    sendToGmail(cust.Mail, ganerateTextForOrder(order).as_string())
    bot.send_message(message.from_user.id, 'Ви успішно оформили свій заказ!✅')


#
# def setNp(message, itemNP, idCust,basket):
#     np = message.text
#     order = {
#         'idCust': idCust,
#         'idsProd': basket['idsProd'],
#         'countProd': basket['countsProd'],
#         'City': city,
#         'AdressNP': np,
#         'SumOrder': basket['SumOrder'],
#         'Phone': phone
#     }
#     productObj.SQLQuery(crudOperation.Insert, '', '', order)
#     basketObj.SQLQuery(crudOperation.Delete, '', f'idCust = {idCust}')
#     cust = productObj.SQLQuery(crudOperation.Select, 'Mail', f'idCust = {idCust}', {})[0]
#
#     print(cust)
#     sendToGmail(cust['mail'], ganerateTextForOrder(order).as_string())
#     bot.send_message(idCust, 'Ви успішно оформили свій заказ!.')
#
#
bot.polling(none_stop=True, interval=0)

