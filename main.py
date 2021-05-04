import sqlite3
import telebot
import datetime as dt
from sqlite3 import Error
from random import choice

insults = ['пидор', 'лох', 'пидорас', 'чмо', 'чмошник', 'говно', 'уёбок',
           'петух', 'ушлёпок', 'гондон', 'блядь', 'ебанат', 'говнюк', 'урод',
           'дебил', 'спермобак', 'хуеблядь', 'чмошничек', 'гондонище',
           'мудозвон', 'мудак', 'гнида']

names_of_dick = ['пенис', 'член', 'хуй', 'писюн', 'хер', 'елдак', 'дилдак',
                 'удав']


def school_schedule():
    TUESDAY = [
        (dt.timedelta(hours=8, minutes=30), dt.timedelta(hours=9, minutes=10)),
        (dt.timedelta(hours=9, minutes=25), dt.timedelta(hours=10, minutes=5)),
        (dt.timedelta(hours=10, minutes=20), dt.timedelta(hours=11)),
        (
            dt.timedelta(hours=11, minutes=15),
            dt.timedelta(hours=11, minutes=35)),
        (
            dt.timedelta(hours=11, minutes=40),
            dt.timedelta(hours=12, minutes=20)),
        (
            dt.timedelta(hours=12, minutes=35),
            dt.timedelta(hours=13, minutes=15)),
        (
            dt.timedelta(hours=13, minutes=30),
            dt.timedelta(hours=14, minutes=10)),
        (dt.timedelta(hours=14, minutes=20), dt.timedelta(hours=15))]

    OTHER = [
        (dt.timedelta(hours=8, minutes=30), dt.timedelta(hours=9, minutes=10)),
        (dt.timedelta(hours=9, minutes=25), dt.timedelta(hours=10, minutes=5)),
        (dt.timedelta(hours=10, minutes=20), dt.timedelta(hours=11)),
        (dt.timedelta(hours=11, minutes=20), dt.timedelta(hours=12)),
        (dt.timedelta(hours=12, minutes=20), dt.timedelta(hours=13)),
        (
            dt.timedelta(hours=13, minutes=15),
            dt.timedelta(hours=13, minutes=55)),
        (dt.timedelta(hours=14, minutes=5), dt.timedelta(hours=14, minutes=45))]

    date_week = dt.datetime.now().weekday()
    time = dt.timedelta(hours=int(dt.datetime.now().hour),
                        minutes=dt.datetime.now().minute)

    flag = 0

    if date_week == 1:
        for i in TUESDAY:
            if i[0] <= time <= i[1]:
                return i[1] - time
    else:
        for i in OTHER:
            if i[0] <= time <= i[1]:
                return i[1] - time
    if not flag:
        return 'Ты ёбнутый?, Иди спи'


def post_sql_query(sql_query):
    with sqlite3.connect('base.db') as connection:
        cursor = connection.cursor()
        try:
            cursor.execute(sql_query)
        except Error:
            pass
        result = cursor.fetchall()
        return result


def create_tables():
    users_query = '''CREATE TABLE IF NOT EXISTS USERS 
                        (user_id INTEGER PRIMARY KEY NOT NULL,
                        username TEXT,
                        first_name TEXT,
                        last_name TEXT,
                        size_of_dick INTEGER,
                        last_dick_request TEXT);'''
    post_sql_query(users_query)


def reply_size_of_dick(message):
    bot.reply_to(message, 'Твой ' + choice(names_of_dick) + ' ' + str(
        post_sql_query(
            'SELECT size_of_dick FROM users WHERE user_id =' +
            str(message.from_user.id))[0][0]) + '-сантиметровый')


def edit_size_of_dick(message, new_size):
    base = sqlite3.connect('base.db')
    cur = base.cursor()
    prev_size = post_sql_query(
        'SELECT size_of_dick FROM users WHERE user_id =' +
        str(message.from_user.id))[0][0]
    if (new_size != 0) and (prev_size + new_size >= 0):
        cur.execute(
            'UPDATE users SET size_of_dick = ' + str(prev_size + new_size)
            + ' WHERE user_id = ' + str(message.from_user.id))
        base.commit()
        if new_size > 0:
            bot.reply_to(message,
                         'Твой ' + choice(names_of_dick) + ' вырос на '
                         + str(new_size)
                         + ' см. Теперь он ' + str(new_size + prev_size)
                         + '-сантиметровый')
        else:
            bot.reply_to(message, 'Твой ' + choice(names_of_dick)
                         + ' уменьшился на ' + str(abs(new_size))
                         + ' см. Теперь он ' + str(new_size + prev_size)
                         + '-сантиметровый')
    else:
        cur.execute(
            'UPDATE users SET size_of_dick = ' + str(0)
            + ' WHERE user_id = ' + str(message.from_user.id))
        base.commit()
        bot.reply_to(message, 'Твой ' + choice(names_of_dick) + ' отвалился...')


def register_user(user_id, username, first_name, last_name):
    user_check_query = f'SELECT * FROM USERS WHERE user_id = {user_id};'
    user_check_data = post_sql_query(user_check_query)
    reg_time = str(dt.datetime.now().year) + ' ' + str(
        dt.datetime.now().month) + ' ' + str(
        dt.datetime.now().day) + ' ' + str(dt.datetime.now(
    ).hour) + ' ' + str(dt.datetime.now().minute)
    if not user_check_data:
        insert_to_db_query = f'INSERT INTO USERS (user_id, username, ' \
                             f'first_name,  last_name, size_of_dick, ' \
                             f'last_dick_request) VALUES ({user_id}, ' \
                             f'"{username}", "{first_name}", "{last_name}",' \
                             f'{10},"{reg_time}");'
        post_sql_query(insert_to_db_query)


def top(message):
    S = telebot.types


def pisun(message):
    last_req_list = list(map(int, post_sql_query(
        'SELECT last_dick_request FROM users WHERE user_id =' +
        str(message.from_user.id))[0][0].split()))
    last_req = dt.datetime(last_req_list[0], last_req_list[1], last_req_list[2],
                           last_req_list[3], last_req_list[4])
    edit_sizes = [-10, -5, -6, -7, -4, -3, -2, -1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2,
                  2, 3, 3, 3, 3, -2, -3, -10, -1, 5, 4, 4, 4, 7, 7, 7, 8, 9, 10,
                  11, 2, 2, 4, 4, -3, 3, 6, 6, 2, 2, -1, -10, 5, 5, 3, 2, 2, 6,
                  4, 3, 5, 3, 3, 4, 0, 2, 4, 7, 5, 6, 3, 7, 8, 3, 6, 1, 1, 3, 6,
                  8, 6, 4, -3, -4, 5, 2, 6, 2, 7, 1, 4, 4, -2, -2]
    if dt.datetime.now() > last_req + dt.timedelta(hours=24):
        edit_size_of_dick(message, choice(edit_sizes))
        base = sqlite3.connect('base.db')
        cur = base.cursor()
        new_time = str(dt.datetime.now().year) + ' ' + str(
            dt.datetime.now().month) + ' ' + str(
            dt.datetime.now().day) + ' ' + str(dt.datetime.now(
        ).hour) + ' ' + str(dt.datetime.now().minute)
        cur.execute(
            'UPDATE users SET last_dick_request = ' + '"' + new_time + '"'
            + ' WHERE user_id = ' + str(message.from_user.id))
        base.commit()
    else:
        bot.reply_to(message, 'Жди, ' + choice(insults))


create_tables()
bot = telebot.TeleBot('1791565125:AAH0BxQSJROn2zQLHkpKwtFlNB2sUuoTqfg')
message = bot.message_handlers


@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.reply_to(message, 'Привет, ' + choice(insults))
    register_user(message.from_user.id, message.from_user.username,
                  message.from_user.first_name, message.from_user.last_name)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == 'длина хуя':
        reply_size_of_dick(message)
    elif message.text.lower() == 'расписание':
        bot.reply_to(message, school_schedule())
    elif message.text.lower() == '/писюн':
        pisun(message)


bot.polling()
