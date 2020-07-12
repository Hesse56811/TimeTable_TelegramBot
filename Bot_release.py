import telebot
import logging
from settings import TG_TOKEN
import sqlite3
from datetime import datetime, timedelta
import time
import schedule
from multiprocessing import *

conn = sqlite3.connect("TelBD.db", check_same_thread=False, timeout=10)
cursor = conn.cursor()
try:
    cursor.execute("""CREATE TABLE MAIN
                  (users TEXT,
                   day TEXT,
                    notes TEXT,
                     time REAL,
                      week INTEGER)
               """)
    cursor.execute("""CREATE TABLE USERS
                      (user_id TEXT,
                        first_name TEXT,
                        last_name TEXT,
                         username TEXT,
                          UTC INTEGER,
                          TIME_NOT TEXT,
                          NOTIF_Stat TEXT
                          )
                   """)
except sqlite3.Error:
    pass
bot = telebot.TeleBot(TG_TOKEN)

# logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )

# button about bot, start to work,feedback, look weather
keyborstart = telebot.types.ReplyKeyboardMarkup(True, True)
keyborstart.add(
    'Приступить к работе', 'О боте', 'Обратная связь', 'Посмотреть погоду', 'Изменить часовой пояс',
    'Настроить уведомления')
# URL-button for feedback
keyboardfeedback = telebot.types.InlineKeyboardMarkup()
keyboardfeedback.add(
    telebot.types.InlineKeyboardButton('@ivan56811', url='https://t.me/Ivan56811'),
)
# URL-button for weather bot
keyboardweather = telebot.types.InlineKeyboardMarkup()
keyboardweather.add(
    telebot.types.InlineKeyboardButton('WeatherBot', url='https://t.me/We_bvbot')
)
# buttons with days
keybordays = telebot.types.InlineKeyboardMarkup()
keybordays.add(
    telebot.types.InlineKeyboardButton('Понедельник', callback_data='get-monday'),
    telebot.types.InlineKeyboardButton('Вторник', callback_data='get-tuesday'),
    telebot.types.InlineKeyboardButton('Среда', callback_data='get-wednesday'),
    telebot.types.InlineKeyboardButton('Четверг', callback_data='get-thursday'),
    telebot.types.InlineKeyboardButton('Пятница', callback_data='get-friday'),
    telebot.types.InlineKeyboardButton('Суббота', callback_data='get-saturday'),
    telebot.types.InlineKeyboardButton('Воскресенье', callback_data='get-sunday'),
    telebot.types.InlineKeyboardButton('Назад', callback_data='back'),
    telebot.types.InlineKeyboardButton('В главное меню', callback_data='go_main_menu')

)

# buttons for user's choose
keyboardchoose = telebot.types.InlineKeyboardMarkup()
keyboardchoose.row(telebot.types.InlineKeyboardButton('Добавить', callback_data='add_to_day'))
keyboardchoose.row(telebot.types.InlineKeyboardButton('Удалить одну запись', callback_data='delete_one'))
keyboardchoose.row(telebot.types.InlineKeyboardButton('Удалить все записи', callback_data='delete_all'))
keyboardchoose.row(telebot.types.InlineKeyboardButton('Показать записи', callback_data='show_all'))
keyboardchoose.row(telebot.types.InlineKeyboardButton('В главное меню', callback_data='go_main_menu'))

# buttons for comfirm choose (yes or no)
keyboardcomf = telebot.types.InlineKeyboardMarkup()
keyboardcomf.row(telebot.types.InlineKeyboardButton('Да', callback_data='ch_yes'))
keyboardcomf.row(telebot.types.InlineKeyboardButton('Нет', callback_data='ch_no'))

# buttons for choose week
keyboardweek = telebot.types.InlineKeyboardMarkup()
keyboardweek.row(telebot.types.InlineKeyboardButton('Текущая', callback_data='this_week'))
keyboardweek.row(telebot.types.InlineKeyboardButton('Следующая', callback_data='next_week'))
keyboardweek.row(telebot.types.InlineKeyboardButton('Показать абсолютно все записи', callback_data='show_all_abs'))
keyboardweek.row(telebot.types.InlineKeyboardButton('Удалить абсолютно все записи', callback_data='delete_all_abs'))

# buttons for choose UTC
keyboardutc = telebot.types.InlineKeyboardMarkup()
keyboardutc.row(telebot.types.InlineKeyboardButton('UTC -12:00', callback_data='utc_-12'),
                telebot.types.InlineKeyboardButton('UTC -11:00', callback_data='utc_-11'),
                telebot.types.InlineKeyboardButton('UTC -10:00', callback_data='utc_-10'))
keyboardutc.row(telebot.types.InlineKeyboardButton('UTC -9:00', callback_data='utc_-9'),
                telebot.types.InlineKeyboardButton('UTC -8:00', callback_data='utc_-8'),
                telebot.types.InlineKeyboardButton('UTC -7:00', callback_data='utc_-7'))
keyboardutc.row(telebot.types.InlineKeyboardButton('UTC -6:00', callback_data='utc_-6'),
                telebot.types.InlineKeyboardButton('UTC -5:00', callback_data='utc_-5'),
                telebot.types.InlineKeyboardButton('UTC -4:00', callback_data='utc_-4'))
keyboardutc.row(telebot.types.InlineKeyboardButton('UTC -3:00', callback_data='utc_-3'),
                telebot.types.InlineKeyboardButton('UTC -2:00', callback_data='utc_-2'),
                telebot.types.InlineKeyboardButton('UTC -1:00', callback_data='utc_-1'))
keyboardutc.row(telebot.types.InlineKeyboardButton('UTC +1:00', callback_data='utc_1'),
                telebot.types.InlineKeyboardButton('UTC +2:00', callback_data='utc_2'),
                telebot.types.InlineKeyboardButton('UTC +3:00', callback_data='utc_3'))
keyboardutc.row(telebot.types.InlineKeyboardButton('UTC +4:00', callback_data='utc_4'),
                telebot.types.InlineKeyboardButton('UTC +5:00', callback_data='utc_5'),
                telebot.types.InlineKeyboardButton('UTC +6:00', callback_data='utc_6'))
keyboardutc.row(telebot.types.InlineKeyboardButton('UTC +7:00', callback_data='utc_7'),
                telebot.types.InlineKeyboardButton('UTC +8:00', callback_data='utc_8'),
                telebot.types.InlineKeyboardButton('UTC +9:00', callback_data='utc_9'))
keyboardutc.row(telebot.types.InlineKeyboardButton('UTC +10:00', callback_data='utc_10'),
                telebot.types.InlineKeyboardButton('UTC +11:00', callback_data='utc_11'),
                telebot.types.InlineKeyboardButton('UTC +12:00', callback_data='utc_12'))
keyboardutc.row(telebot.types.InlineKeyboardButton('UTC 00:00', callback_data='utc_0'),
                telebot.types.InlineKeyboardButton('В главное меню', callback_data='go_main_menu'))

# buttons-settings notifications
keyboardnotif = telebot.types.InlineKeyboardMarkup()
keyboardnotif.add(telebot.types.InlineKeyboardButton('Включить уведомления', callback_data='on_notif'))
keyboardnotif.add(telebot.types.InlineKeyboardButton('Выключить уведомления', callback_data='off_notif'))
keyboardnotif.add(telebot.types.InlineKeyboardButton('Установить время уведомлений', callback_data='time_notif'))
keyboardnotif.add(telebot.types.InlineKeyboardButton('В главное меню', callback_data='go_main_menu'))

days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]


def parity_of_week(m):
    z = 0
    utc = 0
    cursor.execute(
        "SELECT UTC FROM USERS WHERE user_id=:ID", {"ID": m})
    while True:
        row = cursor.fetchone()
        if row == None:
            if z == 0:
                utc = 0
            break
        else:
            z = 1
            utc = row[0]
    conn.commit()
    try:
        now = datetime.now() + timedelta(hours=-3) + timedelta(hours=utc)
    except:
        now = datetime.now() + timedelta(hours=-3)
    sep = datetime(now.year if now.month >= 9 else now.year - 1, 9, 1)
    d1 = sep - timedelta(days=sep.weekday())
    d2 = now - timedelta(days=now.weekday())
    return ((d2 - d1).days // 7) % 2

    ####Функции для выполнения заданий по времени


def send_message1(t):
    day_num = datetime.now().weekday()
    next_week = parity_of_week(t)
    if days[day_num] == 'sunday':
        if next_week == 0:
            next_week = 1
        else:
            next_week = 0
        next_day = 'monday'
    else:
        next_day = days[day_num + 1]
    cursor.execute("SELECT notes, time FROM MAIN WHERE week=:Week and day=:Day and users=:U ORDER BY time",
                   {"Week": next_week, "Day": next_day, "U": t})
    while True:
        row = cursor.fetchone()
        if row == None:
            break
        elif row[1] == None:
            bot.send_message(t, text=row[0])
        else:
            conn.commit()
            if int(row[1]) >= 10:
                if len(str(row[1])) < 5:
                    y = str(row[1]) + '0'
                else:
                    y = str(row[1])
            else:
                if len(str(row[1])) < 4:
                    y = str(row[1]) + '0'
                else:
                    y = str(row[1])
            bot.send_message(chat_id=t, text=y + ' — ' + row[0])


###Настройки команд telebot#########

# message for /start
@bot.message_handler(commands=['start'])
def first_start_message(message):
    bot.send_message(message.chat.id, 'Приветствую тебя, Сталкер!', reply_markup=keyborstart)
    cursor.execute(
        "SELECT username FROM USERS WHERE user_id=:ID", {"ID": message.chat.id})
    while True:
        row = cursor.fetchone()
        if row == None:
            sql = """
                         INSERT INTO USERS (user_id, first_name, last_name, username)
                         VALUES (?, ?, ?, ?)
                        """
            cursor.execute(sql, (
                message.chat.id, message.from_user.first_name, message.from_user.last_name,
                message.from_user.username))
            conn.commit()
            break
        else:
            break


# main menu
@bot.message_handler(content_types=['text', 'document', 'audio'])
def start_messages(message):
    if message.text == 'Привет':
        bot.send_message(message.chat.id, 'Приветсвую тебя, Сталкер!', reply_markup=keyborstart)
    elif message.text == 'Пока':
        bot.send_message(message.chat.id, 'Да пребудет с тобой сила')
    elif message.text == 'Обратная связь':
        bot.send_message(message.chat.id, 'Вы можете написать сюда', reply_markup=keyboardfeedback)
    elif message.text == 'О боте':
        bot.send_message(message.chat.id,
                         'Данный бот предназначен для запоминания чередующегося расписания (четная/нечетная неделя),'
                         'кроме этого он будет каждый день напоминать о '
                         'расписании на следующий день(можно настроить из главного меню) ',
                         reply_markup=keyborstart)
    elif message.text == 'Посмотреть погоду':
        bot.send_message(message.chat.id, 'Вы можете посмотреть погоду здесь:', reply_markup=keyboardweather)
    elif message.text == 'Приступить к работе':
        bot.send_message(message.chat.id, 'Выберите неделю:', reply_markup=keyboardweek)
    elif message.text == 'Изменить часовой пояс':
        bot.send_message(message.chat.id, 'Выберите часовой пояс(по умолчанию UTC 0)', reply_markup=keyboardutc)
    elif message.text == 'Настроить уведомления':
        cursor.execute(
            "SELECT UTC FROM USERS WHERE user_id=:ID", {"ID": message.chat.id})
        while True:
            row = cursor.fetchone()
            if row[0] == None:
                bot.send_message(message.chat.id, 'Для корректной работы выберите часовой пояс',
                                 reply_markup=keyborstart)
                break
            else:
                bot.send_message(message.chat.id, 'Что вы хотите сделать?', reply_markup=keyboardnotif)
                break
        conn.commit()
    else:
        bot.send_message(message.chat.id, 'К сожалению, я тебя не понимаю', reply_markup=keyborstart)


# dict for week and day
dict_week = {}
dict_day = {}


# user choose the week
@bot.callback_query_handler(func=lambda call: call.data == 'this_week' or call.data == 'next_week')
def week_choose(call):
    week = parity_of_week(call.message.chat.id)
    if call.data == 'this_week':
        bot.answer_callback_query(call.id)
        dict_week[call.message.chat.id] = week
        bot.delete_message(message_id=call.message.message_id, chat_id=call.message.chat.id)
        bot.send_message(call.message.chat.id, 'Выберете день недели', reply_markup=keybordays)
    if call.data == 'next_week':
        bot.answer_callback_query(call.id)
        if week == 0:
            week = 1
        else:
            week = 0
        dict_week[call.message.chat.id] = week
        bot.delete_message(message_id=call.message.message_id, chat_id=call.message.chat.id)
        bot.send_message(call.message.chat.id, 'Выберете день недели', reply_markup=keybordays)


# user choose the day
@bot.callback_query_handler(func=lambda call: 'get-' in call.data)
def callback_worker(call):
    # what user want
    bot.answer_callback_query(call.id)
    y = len(call.data)
    defies = call.data.find('-')
    day = call.data[defies + 1:y]
    dict_day[call.message.chat.id] = day
    bot.delete_message(message_id=call.message.message_id, chat_id=call.message.chat.id)
    bot.send_message(call.message.chat.id, 'Что вы хотите сделать?', reply_markup=keyboardchoose)


# go back button
@bot.callback_query_handler(func=lambda call: call.data == 'back')
def go_back(call):
    bot.answer_callback_query(call.id)
    bot.delete_message(message_id=call.message.message_id, chat_id=call.message.chat.id)
    bot.send_message(call.message.chat.id, 'Назад', reply_markup=keyboardweek)
    dict_week.clear()
    dict_day.clear()


# do that want user
@bot.callback_query_handler(func=lambda call:
call.data == 'add_to_day' or
call.data == 'delete_one' or
call.data == 'delete_all' or
call.data == 'show_all' or
call.data == 'go_main_menu')
def what_user_choose(call):
    if call.data == 'add_to_day':
        bot.answer_callback_query(call.id)
        bot.delete_message(message_id=call.message.message_id, chat_id=call.message.chat.id)
        bot.register_next_step_handler(
            bot.send_message(call.message.chat.id,
                             'Введите запись, которую хотите добавить ('
                             'для корректной работы следует писать в таком формате: hour.min-notes'),
            add_message)
    if call.data == 'delete_one':
        bot.answer_callback_query(call.id)
        bot.delete_message(message_id=call.message.message_id, chat_id=call.message.chat.id)
        bot.register_next_step_handler(
            bot.send_message(call.message.chat.id, 'Введите запись, которую хотите удалить'),
            del_message)
    if call.data == 'delete_all':
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, 'Вы уверены?', reply_markup=keyboardcomf)
        bot.delete_message(message_id=call.message.message_id, chat_id=call.message.chat.id)
    if call.data == 'show_all':
        bot.answer_callback_query(call.id)
        bot.delete_message(message_id=call.message.message_id, chat_id=call.message.chat.id)
        cursor.execute("SELECT notes,time FROM MAIN WHERE users=:Id AND day=:Day AND week=:Week ORDER BY time",
                       {"Id": call.message.chat.id, "Day": dict_day[call.message.chat.id],
                        "Week": dict_week[call.message.chat.id]})
        z = 0
        while True:
            row = cursor.fetchone()
            if row == None:
                if z == 0:
                    bot.send_message(call.message.chat.id, text='Записей не найдено')
                break
            elif row[1] == None:
                bot.send_message(call.message.chat.id, text=row[0])
            else:
                if int(row[1]) >= 10:
                    if len(str(row[1])) < 5:
                        y = str(row[1]) + '0'
                    else:
                        y = str(row[1])
                else:
                    if len(str(row[1])) < 4:
                        y = str(row[1]) + '0'
                    else:
                        y = str(row[1])
                z = 1
                bot.send_message(call.message.chat.id, text=y + ' — ' + row[0], reply_markup=keyborstart)
        dict_week.clear()
        dict_day.clear()
        conn.commit()
    if call.data == 'go_main_menu':
        bot.answer_callback_query(call.id)
        bot.delete_message(message_id=call.message.message_id, chat_id=call.message.chat.id)
        dict_week.clear()
        dict_day.clear()
        bot.send_message(call.message.chat.id, 'В главное меню', reply_markup=keyborstart)


# add message to DataBase
def add_message(message):
    x = message.text
    y = len(x)
    defies = x.find('-')
    if defies == -1:
        sql = """
         INSERT INTO MAIN (users, day, notes,week)
         VALUES (?, ?, ?, ?)
        """
        cursor.execute(sql, (message.chat.id, dict_day[message.chat.id], x, dict_week[message.chat.id]))
        conn.commit()
        bot.send_message(message.chat.id, 'Запись успешно добавлена!', reply_markup=keyborstart)
        dict_week.clear()
        dict_day.clear()
    else:
        note_time = float(x[0:defies])
        notes = x[defies + 1:y]
        sql = """
                          INSERT INTO MAIN (users, day, notes, time, week)
                           VALUES (?, ?, ?, ?, ?)
                           """
        cursor.execute(sql,
                       (message.chat.id, dict_day[message.chat.id], notes, note_time,
                        dict_week[message.chat.id]))
        conn.commit()
        bot.send_message(message.chat.id, 'Запись успешно добавлена!', reply_markup=keyborstart)
        dict_week.clear()
        dict_day.clear()


# delete message from DataBase
def del_message(message):
    x = message.text
    cursor.execute("DELETE FROM MAIN WHERE users=:Id AND notes=:IK AND week=:Week AND day=:Day",
                   {"Id": message.chat.id, "IK": x, "Day": dict_day[message.chat.id],
                    "Week": dict_week[message.chat.id]})
    conn.commit()
    bot.send_message(message.chat.id, 'Данная запись успешно удалена!', reply_markup=keyborstart)
    dict_week.clear()
    dict_day.clear()


# comfirm all notes of day delete
@bot.callback_query_handler(func=lambda call: call.data == 'ch_yes' or call.data == 'ch_no')
def com_all_del(call):
    if call.data == 'ch_yes':
        bot.answer_callback_query(call.id)
        if bool(dict_day):
            cursor.execute("DELETE FROM MAIN WHERE users=:Id AND day=:Day AND week=:Week",
                           {"Id": call.message.chat.id, "Day": dict_day[call.message.chat.id],
                            "Week": dict_week[call.message.chat.id]})
            conn.commit()
            bot.send_message(call.message.chat.id, 'Все записи на данный день успешно удалены.',
                             reply_markup=keyborstart)
            dict_week.clear()
            dict_day.clear()
        else:
            cursor.execute("DELETE FROM MAIN WHERE users=:Id", {"Id": call.message.chat.id})
            conn.commit()
            bot.send_message(call.message.chat.id, 'Все записи на данный день успешно удалены.',
                             reply_markup=keyborstart)
    if call.data == 'ch_no':
        bot.send_message(call.message.chat.id, 'Ничего, бывает', reply_markup=keyborstart)
    bot.delete_message(message_id=call.message.message_id, chat_id=call.message.chat.id)


# absolutly delete all notes
@bot.callback_query_handler(func=lambda call: call.data == 'delete_all_abs')
def del_all_abc(call):
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, 'Вы уверены?', reply_markup=keyboardcomf)
    bot.delete_message(message_id=call.message.message_id, chat_id=call.message.chat.id)


def days_to_rus(d):
    if d == 'monday':
        return 'Понедельник:'
    if d == 'tuesday':
        return 'Вторник:'
    if d == 'wednesday':
        return 'Среда:'
    if d == 'thursday':
        return 'Четверг:'
    if d == 'friday':
        return 'Пятница:'
    if d == 'saturday':
        return 'Суббота:'
    if d == 'sunday':
        return 'Воскресенье:'


# absolutly show all notes
@bot.callback_query_handler(func=lambda call: call.data == 'show_all_abs')
def del_all_abc(call):
    bot.answer_callback_query(call.id)
    bot.delete_message(message_id=call.message.message_id, chat_id=call.message.chat.id)
    p = parity_of_week(call.message.chat.id)
    z = 0
    bot.send_message(call.message.chat.id, text='Текущая неделя:')
    for i in days:
        cursor.execute("SELECT notes,time FROM MAIN WHERE users=:Id AND day=:Day AND week=:Week ORDER BY time",
                       {"Id": call.message.chat.id, "Day": i, "Week": p})
        while True:
            row = cursor.fetchone()
            if row == None:
                z = 0
                break
            elif row[1] == None:
                bot.send_message(call.message.chat.id, text=row[0])
            else:
                if int(row[1]) >= 10:
                    if len(str(row[1])) < 5:
                        y = str(row[1]) + '0'
                    else:
                        y = str(row[1])
                else:
                    if len(str(row[1])) < 4:
                        y = str(row[1]) + '0'
                    else:
                        y = str(row[1])
                if z == 0:
                    bot.send_message(call.message.chat.id, text=days_to_rus(i))
                else:
                    z = 1
                bot.send_message(call.message.chat.id, text=y + ' — ' + row[0], reply_markup=keyborstart)
                conn.commit()
    if p == 1:
        p = 0
    else:
        p = 1
    z = 0
    bot.send_message(call.message.chat.id, text='Следущая неделя:')
    for i in days:
        cursor.execute("SELECT notes,time FROM MAIN WHERE users=:Id AND day=:Day AND week=:Week ORDER BY time",
                       {"Id": call.message.chat.id, "Day": i, "Week": p})
        while True:
            row = cursor.fetchone()
            if row == None:
                z = 0
                break
            elif row[1] == None:
                bot.send_message(call.message.chat.id, text=row[0])
            else:
                if int(row[1]) >= 10:
                    if len(str(row[1])) < 5:
                        y = str(row[1]) + '0'
                    else:
                        y = str(row[1])
                else:
                    if len(str(row[1])) < 4:
                        y = str(row[1]) + '0'
                    else:
                        y = str(row[1])
                if z == 0:
                    bot.send_message(call.message.chat.id, text=days_to_rus(i))
                else:
                    z = 1
                bot.send_message(call.message.chat.id, text=y + ' — ' + row[0], reply_markup=keyborstart)
    conn.commit()


@bot.callback_query_handler(func=lambda call: 'utc' in call.data)
def choose_utc(call):
    bot.answer_callback_query(call.id)
    y = len(call.data)
    defies = call.data.find('_')
    utc = call.data[defies + 1:y]
    cursor.execute("UPDATE USERS SET UTC=:U WHERE user_id=:ID", {"ID": call.message.chat.id, "U": utc})
    conn.commit()
    bot.delete_message(message_id=call.message.message_id, chat_id=call.message.chat.id)
    bot.send_message(call.message.chat.id, 'Часовой пояс успешно выбран!', reply_markup=keyborstart)


@bot.callback_query_handler(
    func=lambda call: call.data == 'on_notif' or call.data == 'off_notif' or call.data == 'time_notif')
def set_not(call):
    bot.answer_callback_query(call.id)
    if call.data == 'on_notif':
        bot.delete_message(message_id=call.message.message_id, chat_id=call.message.chat.id)
        cursor.execute("UPDATE USERS SET NOTIF_Stat=:N WHERE user_id=:ID", {"ID": call.message.chat.id, "N": 1})
        bot.send_message(call.message.chat.id, 'Уведомления успешно включены!', reply_markup=keyborstart)
    if call.data == 'off_notif':
        bot.delete_message(message_id=call.message.message_id, chat_id=call.message.chat.id)
        cursor.execute("UPDATE USERS SET NOTIF_Stat=:N WHERE user_id=:ID", {"ID": call.message.chat.id, "N": 0})
        bot.send_message(call.message.chat.id, 'Уведомления успешно выключены!', reply_markup=keyborstart)
    if call.data == 'time_notif':
        bot.delete_message(message_id=call.message.message_id, chat_id=call.message.chat.id)
        bot.register_next_step_handler(bot.send_message(call.message.chat.id,
                                                        'Введите время, в которое хотите получать уведомления'
                                                        '(используйте формат: hour:min)'), add_time_notif)
    conn.commit()


# add time-notification to DataBase
def add_time_notif(message):
    x = message.text
    y = len(x)
    defies = x.find(':')
    b = x.find('.')
    a = x.find(',')
    u_hour = x[0:defies]
    u_min = x[defies + 1:y]
    if a != -1 or b != -1:
        defies = -1
    elif len(u_hour) > 2 or len(u_min) > 2:
        defies = -1
    elif int(u_hour) > 24 or int(u_hour) < 0 or int(u_min) > 60 or int(u_min) < 0:
        defies = -1
    if defies == -1:
        bot.send_message(message.chat.id, 'Что-то пошло не так, попробуйте еще раз')
        bot.register_next_step_handler(bot.send_message(message.chat.id,
                                                        'Введите время, в которое хотите получать уведомления'
                                                        '(Например: 21:30)'),
                                       add_time_notif)
    else:
        cursor.execute("UPDATE USERS SET TIME_NOT=:T WHERE user_id=:ID", {"ID": message.chat.id, "T": x})
        conn.commit()
        bot.send_message(message.chat.id, 'Время уведомлений успешно изменено!', reply_markup=keyborstart)


if __name__ == '__main__':
    try:
        bot.polling(none_stop=True)
    except:
        pass
