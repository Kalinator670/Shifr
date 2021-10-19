import telebot
import sqlite3
import random
import string
from telebot import types
import hashlib
import requests
import json
import emoji

bot = telebot.TeleBot("2035295118:AAHKLBPjC87Yeoqo1U0eAIVx6TX7saoFwYg")

conn = sqlite3.connect('/home/normas/Документы/RunCasesUsers', check_same_thread=False,timeout=7)
cursor = conn.cursor()

def is_number(s):
	try:
		float(s)
		return True
	except ValueError:
		return False

@bot.message_handler(commands=['conclusion'])
def concl(message):
	global moni
	use = message.chat.id
	z ='SELECT Money FROM RunCasesUsers WHERE User_id ={} '.format(use)
	cursor.execute(z)
	resultat = cursor.fetchall()
	conn.commit()
	if resultat:
		moni=int(resultat[0][0])
		bot.send_message(message.chat.id, 'Сейчас ваш баланс составляет:  ' + str(resultat[0][0]))
		su=bot.send_message(message.chat.id, 'Введите сумму, которую хотите вывести ')
		bot.register_next_step_handler(su,concl1)
	else:
		bot.send_message(message.chat.id, 'У вас не пополнен счёт!')
def concl1(message):
	use = message.chat.id
	if is_number(message.text)==True:
		if int(message.text)<=moni:
			zapros="INSERT INTO Requests(user_id,money) VALUES ('{}','{}')".format(use,int(message.text))
			cursor.execute(zapros)
			resultat00 = cursor.fetchall()
			conn.commit()
			bot.send_message(message.chat.id, 'Ожидайте результата заявки!')
		else:
			bot.send_message(message.chat.id, 'Неверно введенная сумма!')
	else:
		bot.send_message(message.chat.id, 'Неверно введенное число!')

@bot.message_handler(commands=['mymoney'])
def check_money(message):
	user_id = message.chat.id
	sql ='SELECT Money FROM RunCasesUsers WHERE User_id ={} '.format(user_id)
	cursor.execute(sql)
	result = cursor.fetchall()
	conn.commit()
	if result:
		bot.send_message(message.chat.id, "Ваш баланс: " + str(result[0][0]) + " руб.")
	else:
		bot.send_message(message.chat.id, 'Ваш счёт пуст!')

@bot.message_handler(commands=['start'])
def s(message):
	global user_id
	bot.send_message(message.chat.id, "Тут вы можете испытать удачу и открыть {} с настоящими деньгами! В отличие от остальных ботов, тут вы реально можете поднять деньги!".format(emoji.emojize(":package:")))
	user_id = message.chat.id

@bot.message_handler(commands=['help'])
def h(message):
	bot.send_message(message.chat.id,"По вопросам обращаться к администратору бота (ссылка находится в описании бота :) )")

@bot.message_handler(commands=['pay'])
def p(message: types.Message):
	global keyboard
	msg=bot.send_message(message.chat.id, 'Введите сумму для пополнения')
	bot.register_next_step_handler(msg,summa)

def summa(message):
	global al
	global user_id0
	global hex_dig
	al=message.text
	if is_number(al)==False:
		bot.send_message(message.from_user.id, "Неправильно введенная сумма!")
	elif is_number(al)==True:
		rb=random.choice(string.ascii_letters)
		rb1=random.choice(string.ascii_letters)
		rc=random.randrange(99999,9999999999)
		rc1=random.randrange(99999,999999999)
		rb2=random.choice(string.ascii_letters)
		ve=str(rc)+rb+str(rc)+rb2+rb1
		ve=ve.encode()
		object = hashlib.sha256(ve)
		hex_dig = object.hexdigest()
		al=str(al)
		user_id0 = message.chat.id
		keyboard = types.InlineKeyboardMarkup()
		check = types.InlineKeyboardButton(text='Проверить платёж', callback_data='checkpay')
		keyboard.add(check)
		bot.send_message(message.from_user.id, text="Чтобы пополнить счет переведите на Qiwi кошелек " +al+ " руб." + " , на номер `79685753921` " +", в комментарии к платежу укажите последовательность:  " + "`{}`".format(hex_dig)+"            *ВНИМАНИЕ!!! ПЕРЕВОДИТЬ ДЕНЬГИ НЕОБХОДИМО ИМЕННО С УКАЗАНИЕМ КОММЕНТАРИЯ (ПОСЛЕДОВАТЕЛЬНОСТИ), ИНАЧЕ ДЕНЬГИ ПРОПАДУТ!!! НАЖИМАТЬ НА КНОПКУ  'Проверить платеж'  НАДО ТОЛЬКО ПОСЛЕ ЯВНОГО ПЕРЕВОДА СТРЕДСТВ! ПОСЛЕДОВАТЕЛЬНОСТЬ ГЕНЕРИРУЕТСЯ 1 РАЗ И ОНА УНИКАЛЬНА!!!*",reply_markup=keyboard,parse_mode= 'Markdown')
		user_id0=message.chat.id
		sqlm="INSERT INTO Pay(user_id,hash,money) VALUES ('{}','{}','{}')".format(user_id0,hex_dig,int(al))
		cursor.execute(sqlm)
		result = cursor.fetchall()
		conn.commit()

@bot.callback_query_handler(func=lambda call: call.data.startswith("summa"))
def callback_worker(call1):
	if call1.data:
		user_id0 = call1.from_user.id
		bot.edit_message_reply_markup(call1.message.chat.id, call1.message.message_id)
		TOKEN = '7746077c6f5a1e919bf2f215bd06bebd'
		ACCOUNT = '79685753921'
		s = requests.Session()
		s.headers['authorization'] = 'Bearer ' + TOKEN
		parameters = {'rows': '50'}
		h = s.get('https://edge.qiwi.com/payment-history/v1/persons/'+ ACCOUNT +'/payments',params=parameters)
		req = json.loads(h.text)
		phone = req[1] 
		sqln ="SELECT money FROM Pay WHERE user_id ={} AND hash='{}'".format(user_id0,hex_dig)
		cursor.execute(sqln)
		result01 = cursor.fetchall()
		conn.commit()
		if result01:
			den=result01[0][0]
			for i in range(len(req['data'])):
				if req['data'][i]['comment'] == hex_dig:
					if req['data'][i]['sum']['amount'] == den:
						bot.send_message(call1.from_user.id,'Оплата прошла успешно!')
						sqlz ='SELECT Money FROM RunCasesUsers WHERE User_id ={} '.format(user_id0)
						cursor.execute(sqlz)
						resultz = cursor.fetchall()
						conn.commit()
						sqld='UPDATE RunCasesUsers SET Money={} WHERE User_id= {}'.format(resultz[0][0]+den,user_id0)
						cursor.execute(sqld)
						resultd = cursor.fetchall()
						conn.commit()
						new='UPDATE RunCasesUsers SET Number={} WHERE User_id= {}'.format(phone,user_id0)
						cursor.execute(new)
						restat = cursor.fetchall()
						conn.commit()
					else:
						bot.send_message(call1.from_user.id,"Неверные данные")
				else:
					bot.send_message(call1.from_user.id, "Неверные данные")

		else:
			bot.send_message(message.chat.id, 'Ваш счёт пуст!')
@bot.message_handler(commands=['play'])
def igra(message):
	global result
	global user_id1
	user_id1 = message.chat.id
	sql1 ='SELECT Money FROM RunCasesUsers WHERE User_id ={} '.format(user_id1)
	cursor.execute(sql1)
	result = cursor.fetchall()
	conn.commit()
	if result:
		mm = types.ReplyKeyboardMarkup(row_width=2,one_time_keyboard=True,resize_keyboard=True)
		button1 = types.KeyboardButton("Открыть кейс за 50 рублей")
		mm.add(button1)
		bot.send_message(message.chat.id,'Выберите кейс, который хотите открыть',reply_markup=mm)
	else:
		bot.send_message(message.chat.id, 'Ваш счёт пуст!')

@bot.message_handler(content_types=['text'])
def bplay(message):
	otvet = types.InlineKeyboardMarkup(row_width=2)
	a = telebot.types.ReplyKeyboardRemove()
	button1 = types.InlineKeyboardButton("Да", callback_data='yeah')
	button2 = types.InlineKeyboardButton("Нет", callback_data='noit')
	otvet.add(button1,button2)
	if message.text=='Открыть кейс за 50 рублей':
		bot.send_message(message.chat.id,'ok',reply_markup=a)
		bot.send_message(message.chat.id, 'Вы уверены, что хотите открыть кейс за 50 рублей?  Открыв этот кейс вы можете выиграть от 5 до 250 рублей!', reply_markup=otvet)
def tzz():
	chisla1=[]
	for j in range(20):
		a=random.randrange(5,201)
		chisla1.append(a)
	return min(chisla1)

@bot.callback_query_handler(func=lambda call: call.data == "yeah")
def callback_inline(call):
	if call.data == 'yeah':
		bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Вы уверены, что хотите открыть кейс за 50 рублей?  Открыв этот кейс вы можете выиграть от 5 до 250 рублей!")
		mon=int(result[0][0])
		if (mon-50)>=0:
			mon1=mon-50
			dp0=tzz()
			bot.send_message(call.from_user.id, "Поздравляю, выш выигрыш составил: " + str(dp0))
			sql1='UPDATE RunCasesUsers SET Money={} WHERE User_id= {}'.format(mon1+int(dp0),user_id1)
			cursor.execute(sql1)
			result1 = cursor.fetchall()
			conn.commit()
		else:
			bot.send_message(call.from_user.id, "Недостаточно денег. Пополните счёт!")

bot.polling()
