import time
import datetime
log = input("|Производить логирование в консоли? 'Y/N': ")
if log != "Y" and log != "y" and log != "n" and log != "N":
	print("Закрытие скрипта, вы дебил.")
	time.sleep(2)
	exit()
import requests
import const
import telebot
import random
from telebot import *
import json
from funcs import *


#Обязательно к заполнению
try:
	admin       = "1403297076"
	token       = "1435515327:AAHYbrq2GNxlJin40dW8N0zCzvUhcMtYMrI"
	qiwi_num    = "+79672668511"
	qiwi_tok    = "7548a18867d142e0663159b829f80186"

	buy = types.InlineKeyboardButton(text="💰Купить",callback_data="buy")
	profile = types.InlineKeyboardButton(text="👔Профиль",callback_data="profile")
	info = types.InlineKeyboardButton(text="❗️Информация",callback_data="inform")
	online_manage = types.InlineKeyboardButton(text="💬Менеджеры онлайн",callback_data="manage_on")


	MARKDOWN = """
	    *bold text*
	    _italic text_
	    [text](URL)
	    """

	bot = TeleBot(token)
	if log == "Y" or log == "y":
		print("| Бот успешно запущен!")

	@bot.message_handler(content_types=['text'])
	def messages(message):
		try:
			time_now = datetime.datetime.today().strftime("%d.%m.%y")
			menu = types.InlineKeyboardMarkup(row_width=1)
			menu.row(buy,profile)
			menu.row(info)

			userid = str(message.from_user.id)
			if log == "Y" or log == "y":
				print(message.text+"|"+userid+"")

			if "рассылка" in message.text:
				if userid == admin:
					splitter = message.text.split("+-")
					text = splitter[1]
					opener = open("base.txt","r").read().split("\n")
					for uid in opener:
						try:
							bot.send_message(uid,text)
						except:
							if log == "Y" or log == "y":
								print("|"+uid + " добавил бота в черный список")
				elif userid != admin:
					pass

			if message.text == "Статистика":
				if userid == admin:
					opener = open("base.txt","r").read().split("\n")
					userss = len(opener)
					payments = open("money.txt","r").readline()
					bot.send_message(userid,"Всего юзеров в боте: "+str(userss)+"\n\nОбщая сумма выплат: "+payments+" руб.")
				elif userid != admin:
					pass
			if "/start" in message.text:
				in_base = checkBase(userid)

				if in_base == True:
					bot.send_message(userid,"*Меню*",parse_mode="MARKDOWN",reply_markup = menu)

				if in_base == False:
					terms = "*Правила использования ботом.\nПокупки в боте идут от 1шт. *"
					hello_text = "*Добро пожаловать в  лучший не оффициальный магазин по продаже SNUS, HQD и JUUL в СНГ!*"
					bot.send_message(userid,"_Пользуясь нашим ботом, вы автоматически соглашаетесь с указанными ниже правилами._\n\n"+terms,parse_mode="MARKDOWN")
					bot.send_message(userid,hello_text,reply_markup=menu,parse_mode="MARKDOWN")
					splitter = message.text.split(" ")
					try:
						bot.send_message(admin,"Реферальный код = "+splitter[1]+"|"+str(userid))
					except Exception as E:
						print(E)
						
					newUser(userid,time_now,log,admin)


				if userid == admin and message.text == "/start":
					bot.send_message(admin,"Вы были распознаны как админ.\n\nАдмин-команды:\n*рассылка+-(текст)*\nПример:\nрассылка+-Сегодня скидки 90%!",parse_mode="MARKDOWN")
		except Exception as E:
			bot.send_message(admin,"Произошла ошибка у бота:\n"+str(E))
	@bot.callback_query_handler(func=lambda call: True)
	def callback_inline(call):

		buy = types.InlineKeyboardButton(text="💰Купить",callback_data="buy")
		profile = types.InlineKeyboardButton(text="👔Профиль",callback_data="profile")
		info = types.InlineKeyboardButton(text="❗️Информация",callback_data="inform")
		online_manage = types.InlineKeyboardButton(text="💬Менеджеры онлайн",callback_data="manage_on")

		menu = types.InlineKeyboardMarkup(row_width=1)
		menu.row(buy,profile)
		menu.row(info,online_manage)
		button_menu = types.InlineKeyboardButton(text="В меню",callback_data="menu")

		userid = str(call.from_user.id)
		if call.data == "menu":
			bot.send_message(userid,"*Меню*",parse_mode="MARKDOWN",reply_markup = menu)
		if call.data == "inform":
			info = """
			⚠️SNUSWORLD - лучшие в своём роде.⚠️

Контакты:
@Aleksandrs4k - главный, владелец магазина. (По всем вопросам к нему).


О нас:
Мы стремимся радовать Вас качеством и нашими вкусными ценами.

Почему именно мы:
1. Вкусные цены.
2. Самый большой ассортимент.
3. Оперативная доставка.
4. Молниеносная поддержка.
5. ОРИГИНАЛЬНАЯ продукция.
6. Гарантируем анонимность.

Отправим в любую точку планеты, Почтой России или курьерской службой.
Стоимость отправки Почтой России около 100 рублей, время доставки 1-8 дней (зависит от удаленности региона от нас).
При покупке от пяти шайб будет СЛАДКАЯ скидка (уточнять у Администратора).
От десяти шайб ДОСТАВКА - БЕСПЛАТНАЯ!!!
			"""
			bot.send_message(userid,info)
		if call.data == "profile":
			opener = open("profiles/"+userid+".txt","r").readline()
			if call.from_user.username != None or call.from_user.username != "None":
				bot.send_message(userid,"👔Профиль\n\nУникальный айди: "+userid+"\nВаш никнейм: @"+str(call.from_user.username)+"\nДата регистрации: "+ opener+"\nЛичный менеджер: Отсутствует\nСкидка: 0%\nПокупок на сумму: 0 руб.")
		if call.data == "manage_on":
			bot.send_message(userid,"_Чтобы вернуться в меню, нажмите /start_\n\n*Доступные менеджеры:*\nМенеджер №1 - ❌\nМенеджер №2 - ❌\nМенеджер №3 - ✅\nМенеджер №4 - ❌\nМенеджер №5 - ✅\nМенеджер №6 - ❌\nМенеджер №7 - ❌\nМенеджер №8 - ✅\nМенеджер №9 - ✅",parse_mode="MARKDOWN")
		if "s_" in call.data:
			check_n_link = types.InlineKeyboardMarkup(row_width=1)
			splitter = call.data.split("_")
			snus_type = splitter[1]
			taste = splitter[2]
			price = splitter[3]
			code = round(random.uniform(1000,50000))
			payment = "https://qiwi.com/payment/form/99?extra%5B%27account%27%5D="+qiwi_num+"&amountInteger=" + price + "&amountFraction=0&extra%5B%27comment%27%5D="+userid+str(code)+"&currency=643&blocked[0]=sum&blocked[1]=comment&blocked[2]=account"
			link = types.InlineKeyboardButton(text="📦Перейти к оплате",url=payment)
			check = types.InlineKeyboardButton(text="📥Проверить оплату",callback_data="check")

			check_n_link.row(link)
			check_n_link.row(check)
			check_n_link.row(button_menu)
			
			bot.send_message(userid,"_Чтобы вернуться в меню, нажмите /start_\nПокупая через смартфон, кнопка ниже отправит вас просто в приложение Qiwi, поэтому, вы можете использовать карту для прямого приема (карту узнавать у Aдминистратора -  @Aleksandrs4k) , и указать в комментариях: "+userid+str(code)+".\nЛибо используйте ссылку отправленную в отдельном сообщении.\n\n*Производитель:* _"+snus_type+"_\n*Тип:* _"+taste+"_\n*Цена за 1 шт.:* _"+price+"руб_",parse_mode="MARKDOWN",reply_markup=check_n_link)
			bot.send_message(userid,"[Ссылка для телефонов]("+payment+")",parse_mode="MARKDOWN")
			opener = open("profiles/"+userid+"_pay.txt","w")
			opener.write(price)
		if log == "Y" or log == "y":
			print(call.data + "|" + str(call.from_user.id))
		if call.data == "menu2":
			menu_buy = types.InlineKeyboardMarkup(row_width=1)
			button_vapes = types.InlineKeyboardButton(text="Вейпы/Многоразовые поды",callback_data="vapes")
			button_liquid = types.InlineKeyboardButton(text="Жидкость Boshki Salt",callback_data="l1")
			button_liquid2 = types.InlineKeyboardButton(text="Жидкость Морс Мороз Salt",callback_data="l2")
			button_liquid3 = types.InlineKeyboardButton(text="Жидкость Fantasi(Фейк и оригинал)",callback_data="l3")
			button_liquid3 = types.InlineKeyboardButton(text="Жидкость Funta",callback_data="l4")
			menu2 = types.InlineKeyboardButton(text="<---",callback_data="buy")
			menu_buy.row(button_vapes)
			menu_buy.row(button_liquid)
			menu_buy.row(button_liquid2)
			menu_buy.row(button_liquid3)
			menu_buy.row(menu2)
			bot.send_message(userid,"*Вы выбрали Каталог #2*\n\n_Чтобы вернуться, нажмите /start_",reply_markup=menu_buy,parse_mode="MARKDOWN")
		if call.data == "l1":
			#BOSHKI_LIQUID
			katalog = const.BOSHKI_LIQUID
			katalog_menu = types.InlineKeyboardMarkup(row_width=1)
			for element in katalog:
				splitter = element.split("|")
				vape_type = splitter[0]
				taste = splitter[1]
				price = splitter[2]
				button = types.InlineKeyboardButton(text=taste,callback_data="s_"+vape_type+"_"+taste+"_"+price)
				katalog_menu.row(button)
			bot.send_message(userid,"*Выбранный вами каталог:"+vape_type+"*\n\n_Чтобы вернуться, нажмите /start_",parse_mode="MARKDOWN",reply_markup=katalog_menu)
		if call.data == "l2":
			#BOSHKI_LIQUID
			katalog = const.MORS_MOROZ
			katalog_menu = types.InlineKeyboardMarkup(row_width=1)
			for element in katalog:
				splitter = element.split("|")
				vape_type = splitter[0]
				taste = splitter[1]
				price = splitter[2]
				button = types.InlineKeyboardButton(text=taste,callback_data="s_"+vape_type+"_"+taste+"_"+price)
				katalog_menu.row(button)
			bot.send_message(userid,"*Выбранный вами каталог:"+vape_type+"*\n\n_Чтобы вернуться, нажмите /start_",parse_mode="MARKDOWN",reply_markup=katalog_menu)
		if call.data == "l3":
			#BOSHKI_LIQUID
			katalog = const.FANTASI_FAKE
			katalog_menu = types.InlineKeyboardMarkup(row_width=1)
			for element in katalog:
				splitter = element.split("|")
				vape_type = splitter[0]
				taste = splitter[1]
				price = splitter[2]
				button = types.InlineKeyboardButton(text=taste,callback_data="s_"+vape_type+"_"+taste+"_"+price)
				katalog_menu.row(button)
			bot.send_message(userid,"*Выбранный вами каталог:"+vape_type+"*\n\n_Чтобы вернуться, нажмите /start_",parse_mode="MARKDOWN",reply_markup=katalog_menu)
		if call.data == "l4":
			#BOSHKI_LIQUID
			katalog = const.FUNTA
			katalog_menu = types.InlineKeyboardMarkup(row_width=1)
			for element in katalog:
				splitter = element.split("|")
				vape_type = splitter[0]
				taste = splitter[1]
				price = splitter[2]
				button = types.InlineKeyboardButton(text=taste,callback_data="s_"+vape_type+"_"+taste+"_"+price)
				katalog_menu.row(button)
			bot.send_message(userid,"*Выбранный вами каталог:"+vape_type+"*\n\n_Чтобы вернуться, нажмите /start_",parse_mode="MARKDOWN",reply_markup=katalog_menu)
		if call.data == "vapes":
			#BOSHKI_LIQUID
			katalog = const.VAPES_PODS
			katalog_menu = types.InlineKeyboardMarkup(row_width=1)
			for element in katalog:
				splitter = element.split("|")
				vape_type = splitter[0]
				taste = splitter[1]
				price = splitter[2]
				button = types.InlineKeyboardButton(text=taste,callback_data="s_"+vape_type+"_"+taste+"_"+price)
				katalog_menu.row(button)
			bot.send_message(userid,"*Выбранный вами каталог:"+vape_type+"*\n\n_Чтобы вернуться, нажмите /start_",parse_mode="MARKDOWN",reply_markup=katalog_menu)

		if call.data == "buy":
			element_list = ["Alfa","Arqa","Blax","Boshki","Nictech","Kurwa","Taboo"]
			menu_buy = types.InlineKeyboardMarkup(row_width=1)
			button_hqd = types.InlineKeyboardButton(text="HQD - Одноразки",callback_data="hqd")
			button_snus = types.InlineKeyboardButton(text="Снюс",callback_data="snus")
			button_juul = types.InlineKeyboardButton(text="Juul",callback_data="juul")
			button_pods = types.InlineKeyboardButton(text="Картриджы Juul",callback_data="pods")
			menu2 = types.InlineKeyboardButton(text="--->",callback_data="menu2")
			menu_buy.row(button_hqd)
			menu_buy.row(button_snus)
			menu_buy.row(button_juul)
			menu_buy.row(button_pods)
			menu_buy.row(button_menu)
			menu_buy.row(menu2)
			bot.send_message(userid,"*Вы выбрали Каталог*\n\n_Чтобы вернуться, нажмите /start_",reply_markup=menu_buy,parse_mode="MARKDOWN")
		if call.data == "juul":
			katalog = const.JUUL
			katalog_menu = types.InlineKeyboardMarkup(row_width=1)
			for element in katalog:
				splitter = element.split("|")
				vape_type = splitter[0]
				taste = splitter[1]
				price = splitter[2]
				button = types.InlineKeyboardButton(text=taste,callback_data="s_"+vape_type+"_"+taste+"_"+price)
				katalog_menu.row(button)
			bot.send_message(userid,"*Выбранный вами каталог:"+vape_type+"*\n\n_Чтобы вернуться, нажмите /start_",parse_mode="MARKDOWN",reply_markup=katalog_menu)

		if call.data == "pods":
			katalog = const.JUUL_PODS
			katalog_menu = types.InlineKeyboardMarkup(row_width=1)
			for element in katalog:
				splitter = element.split("|")
				vape_type = splitter[0]
				taste = splitter[1]
				price = splitter[2]
				button = types.InlineKeyboardButton(text=taste,callback_data="s_"+vape_type+"_"+taste+"_"+price)
				katalog_menu.row(button)
			bot.send_message(userid,"*Выбранный вами каталог:"+vape_type+"*\n\n_Чтобы вернуться, нажмите /start_",parse_mode="MARKDOWN",reply_markup=katalog_menu)



		if call.data == "snus":
			menu_buy = types.InlineKeyboardMarkup(row_width=1)
			button_1 = types.InlineKeyboardButton(text="Alfa",callback_data="Alfa")
			button_2 = types.InlineKeyboardButton(text="Arqa",callback_data="Arqa")
			button_3 = types.InlineKeyboardButton(text="Blax",callback_data="Blax")
			button_4 = types.InlineKeyboardButton(text="Boshki",callback_data="Boshki")
			button_5 = types.InlineKeyboardButton(text="Nictech",callback_data="Nictech")
			button_6 = types.InlineKeyboardButton(text="Kurwa",callback_data="Kurwa")
			button_7 = types.InlineKeyboardButton(text="Taboo",callback_data="Taboo")
			button_8 = types.InlineKeyboardButton(text="Chainsaw",callback_data="Chainsaw")
			button_9 = types.InlineKeyboardButton(text="Siberia",callback_data="Siberia")
			button_10 = types.InlineKeyboardButton(text="Lyft",callback_data="Lyft")
			button_11 = types.InlineKeyboardButton(text="Corvus",callback_data="Corvus")
			menu_buy.row(button_11,button_1)
			menu_buy.row(button_8,button_9,button_10)
			menu_buy.row(button_2,button_3,button_4)
			menu_buy.row(button_5,button_6,button_7)
			menu_buy.row(button_menu)
			bot.send_message(userid,"*Вы выбрали Каталог*\n\n_Чтобы вернуться, нажмите /start_",reply_markup=menu_buy,parse_mode="MARKDOWN")
		if call.data == "hqd":
			menu_buy = types.InlineKeyboardMarkup(row_width=1)
			button_1 = types.InlineKeyboardButton(text="HQD Cuvie",callback_data="cuvie")
			button_2 = types.InlineKeyboardButton(text="HQD Maxim",callback_data="maxim")
			button_3 = types.InlineKeyboardButton(text="HQD Stark",callback_data="stark")
			button_4 = types.InlineKeyboardButton(text="HQD Ultra",callback_data="ultra")
			button_5 = types.InlineKeyboardButton(text="HQD Rosy",callback_data="rosy")
			
			menu_buy.row(button_1)
			menu_buy.row(button_2,button_3,button_4)
			menu_buy.row(button_5)
			menu_buy.row(button_menu)
			bot.send_message(userid,"*Вы выбрали Каталог*\n\n_Чтобы вернуться, нажмите /start_",reply_markup=menu_buy,parse_mode="MARKDOWN")

		if call.data == "cuvie":
			katalog = const.HQDCUVIE
			katalog_menu = types.InlineKeyboardMarkup(row_width=1)
			for element in katalog:
				splitter = element.split("|")
				vape_type = splitter[0]
				taste = splitter[1]
				price = splitter[2]
				button = types.InlineKeyboardButton(text=taste,callback_data="s_"+vape_type+"_"+taste+"_"+price)
				katalog_menu.row(button)
			bot.send_message(userid,"*Выбранный вами каталог:"+vape_type+"*\n\n_Чтобы вернуться, нажмите /start_",parse_mode="MARKDOWN",reply_markup=katalog_menu)

		if call.data == "maxim":
			katalog = const.HQDMAXIM
			katalog_menu = types.InlineKeyboardMarkup(row_width=1)
			for element in katalog:
				splitter = element.split("|")
				vape_type = splitter[0]
				taste = splitter[1]
				price = splitter[2]
				button = types.InlineKeyboardButton(text=taste,callback_data="s_"+vape_type+"_"+taste+"_"+price)
				katalog_menu.row(button)
			bot.send_message(userid,"*Выбранный вами каталог:"+vape_type+"*\n\n_Чтобы вернуться, нажмите /start_",parse_mode="MARKDOWN",reply_markup=katalog_menu)

		if call.data == "stark":
			katalog = const.HQDSTARK
			katalog_menu = types.InlineKeyboardMarkup(row_width=1)
			for element in katalog:
				splitter = element.split("|")
				vape_type = splitter[0]
				taste = splitter[1]
				price = splitter[2]
				button = types.InlineKeyboardButton(text=taste,callback_data="s_"+vape_type+"_"+taste+"_"+price)
				katalog_menu.row(button)
			bot.send_message(userid,"*Выбранный вами каталог:"+vape_type+"*\n\n_Чтобы вернуться, нажмите /start_",parse_mode="MARKDOWN",reply_markup=katalog_menu)

		if call.data == "ultra":
			katalog = const.HQDULTRA
			katalog_menu = types.InlineKeyboardMarkup(row_width=1)
			for element in katalog:
				splitter = element.split("|")
				vape_type = splitter[0]
				taste = splitter[1]
				price = splitter[2]
				button = types.InlineKeyboardButton(text=taste,callback_data="s_"+vape_type+"_"+taste+"_"+price)
				katalog_menu.row(button)
			bot.send_message(userid,"*Выбранный вами каталог:"+vape_type+"*\n\n_Чтобы вернуться, нажмите /start_",parse_mode="MARKDOWN",reply_markup=katalog_menu)

		if call.data == "rosy":
			katalog = const.HQDROSY
			katalog_menu = types.InlineKeyboardMarkup(row_width=1)
			for element in katalog:
				splitter = element.split("|")
				vape_type = splitter[0]
				taste = splitter[1]
				price = splitter[2]
				button = types.InlineKeyboardButton(text=taste,callback_data="s_"+vape_type+"_"+taste+"_"+price)
				katalog_menu.row(button)

			bot.send_message(userid,"*Выбранный вами каталог:"+vape_type+"*\n\n_Чтобы вернуться, нажмите /start_",parse_mode="MARKDOWN",reply_markup=katalog_menu)


		if call.data == "Alfa":
			katalog = const.ALFA
			katalog_menu = types.InlineKeyboardMarkup(row_width=1)
			for element in katalog:
				splitter = element.split("|")
				snus_type = splitter[0]
				taste = splitter[1]
				price = splitter[2]
				button = types.InlineKeyboardButton(text=taste,callback_data="s_"+snus_type+"_"+taste+"_"+price)
				katalog_menu.row(button)

			bot.send_message(userid,"*Выбранный вами каталог:"+snus_type+"*\n\n_Чтобы вернуться, нажмите /start_",parse_mode="MARKDOWN",reply_markup=katalog_menu)

		if call.data == "Arqa":
			katalog = const.ARQA
			katalog_menu = types.InlineKeyboardMarkup(row_width=1)
			for element in katalog:
				splitter = element.split("|")
				snus_type = splitter[0]
				taste = splitter[1]
				price = splitter[2]
				button = types.InlineKeyboardButton(text=taste,callback_data="s_"+snus_type+"_"+taste+"_"+price)
				katalog_menu.row(button)
				katalog_menu.row(button_menu)
			katalog_menu.row(button_menu)
			bot.send_message(userid,"*Выбранный вами каталог:"+snus_type+"*\n\n_Чтобы вернуться, нажмите /start_",parse_mode="MARKDOWN",reply_markup=katalog_menu)

		if call.data == "Blax":
			katalog = const.BLAX
			katalog_menu = types.InlineKeyboardMarkup(row_width=1)
			for element in katalog:
				splitter = element.split("|")
				snus_type = splitter[0]
				taste = splitter[1]
				price = splitter[2]
				button = types.InlineKeyboardButton(text=taste,callback_data="s_"+snus_type+"_"+taste+"_"+price)
				katalog_menu.row(button)

			katalog_menu.row(button_menu)
			bot.send_message(userid,"*Выбранный вами каталог:"+snus_type+"*\n\n_Чтобы вернуться, нажмите /start_",parse_mode="MARKDOWN",reply_markup=katalog_menu)


		if call.data == "Boshki":
			katalog = const.BOSHKI
			katalog_menu = types.InlineKeyboardMarkup(row_width=1)
			for element in katalog:
				splitter = element.split("|")
				snus_type = splitter[0]
				taste = splitter[1]
				price = splitter[2]
				button = types.InlineKeyboardButton(text=taste,callback_data="s_"+snus_type+"_"+taste+"_"+price)
				katalog_menu.row(button)
			katalog_menu.row(button_menu)
			bot.send_message(userid,"*Выбранный вами каталог:"+snus_type+"*\n\n_Чтобы вернуться, нажмите /start_",parse_mode="MARKDOWN",reply_markup=katalog_menu)

		if call.data == "Nictech":
			katalog = const.NICTECH
			katalog_menu = types.InlineKeyboardMarkup(row_width=1)
			for element in katalog:
				splitter = element.split("|")
				snus_type = splitter[0]
				taste = splitter[1]
				price = splitter[2]
				button = types.InlineKeyboardButton(text=taste,callback_data="s_"+snus_type+"_"+taste+"_"+price)
				katalog_menu.row(button)
			katalog_menu.row(button_menu)
			bot.send_message(userid,"*Выбранный вами каталог:"+snus_type+"*\n\n_Чтобы вернуться, нажмите /start_",parse_mode="MARKDOWN",reply_markup=katalog_menu)

		if call.data == "Kurwa":
			katalog = const.KURWA
			katalog_menu = types.InlineKeyboardMarkup(row_width=1)
			for element in katalog:
				splitter = element.split("|")
				snus_type = splitter[0]
				taste = splitter[1]
				price = splitter[2]
				button = types.InlineKeyboardButton(text=taste,callback_data="s_"+snus_type+"_"+taste+"_"+price)
				katalog_menu.row(button)
			katalog_menu.row(button_menu)
			bot.send_message(userid,"*Выбранный вами каталог:"+snus_type+"*\n\n_Чтобы вернуться, нажмите /start_",parse_mode="MARKDOWN",reply_markup=katalog_menu)

		if call.data == "Taboo":
			katalog = const.TABOO
			katalog_menu = types.InlineKeyboardMarkup(row_width=1)
			for element in katalog:
				splitter = element.split("|")
				snus_type = splitter[0]
				taste = splitter[1]
				price = splitter[2]
				button = types.InlineKeyboardButton(text=taste,callback_data="s_"+snus_type+"_"+taste+"_"+price)
				katalog_menu.row(button)
			katalog_menu.row(button_menu)
			bot.send_message(userid,"*Выбранный вами каталог:"+snus_type+"*\n\n_Чтобы вернуться, нажмите /start_",parse_mode="MARKDOWN",reply_markup=katalog_menu)


		if call.data == "Siberia":
			katalog = const.SIBERIA
			katalog_menu = types.InlineKeyboardMarkup(row_width=1)
			for element in katalog:
				splitter = element.split("|")
				snus_type = splitter[0]
				taste = splitter[1]
				price = splitter[2]
				button = types.InlineKeyboardButton(text=taste,callback_data="s_"+snus_type+"_"+taste+"_"+price)
				katalog_menu.row(button)
			katalog_menu.row(button_menu)
			bot.send_message(userid,"*Выбранный вами каталог:"+snus_type+"*\n\n_Чтобы вернуться, нажмите /start_",parse_mode="MARKDOWN",reply_markup=katalog_menu)

		if call.data == "Lyft":
			katalog = const.LYFT
			katalog_menu = types.InlineKeyboardMarkup(row_width=1)
			for element in katalog:
				splitter = element.split("|")
				snus_type = splitter[0]
				taste = splitter[1]
				price = splitter[2]
				button = types.InlineKeyboardButton(text=taste,callback_data="s_"+snus_type+"_"+taste+"_"+price)
				katalog_menu.row(button)
			katalog_menu.row(button_menu)
			bot.send_message(userid,"*Выбранный вами каталог:"+snus_type+"*\n\n_Чтобы вернуться, нажмите /start_",parse_mode="MARKDOWN",reply_markup=katalog_menu)


		if call.data == "Chainsaw":
			katalog = const.CHAINSAW
			katalog_menu = types.InlineKeyboardMarkup(row_width=1)
			for element in katalog:
				splitter = element.split("|")
				snus_type = splitter[0]
				taste = splitter[1]
				price = splitter[2]
				button = types.InlineKeyboardButton(text=taste,callback_data="s_"+snus_type+"_"+taste+"_"+price)
				katalog_menu.row(button)
			katalog_menu.row(button_menu)
			bot.send_message(userid,"*Выбранный вами каталог:"+snus_type+"*\n\n_Чтобы вернуться, нажмите /start_",parse_mode="MARKDOWN",reply_markup=katalog_menu)

		if call.data == "Corvus":
			katalog = const.CORVUS
			katalog_menu = types.InlineKeyboardMarkup(row_width=1)
			for element in katalog:
				splitter = element.split("|")
				snus_type = splitter[0]
				taste = splitter[1]
				price = splitter[2]
				button = types.InlineKeyboardButton(text=taste,callback_data="s_"+snus_type+"_"+taste+"_"+price)
				katalog_menu.row(button)
			katalog_menu.row(button_menu)
			bot.send_message(userid,"*Выбранный вами каталог:"+snus_type+"*\n\n_Чтобы вернуться, нажмите /start_",parse_mode="MARKDOWN",reply_markup=katalog_menu)

		if call.data == "check":
			if userid:
				bot.send_message(userid,"*К сожалению, ваша оплата пока не дошла до нас.*\n\n_Как только вы убедитесь в том что оплата успешно проведена, нажмите_ *Проверить оплату*",parse_mode="markdown")
except Exception as E:
	print(E)

try:

	bot.polling(none_stop=True)
except:

	print("FATAL ERROR")


