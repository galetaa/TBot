import psycopg2
import telebot
import datetime as dt
from psycopg2 import Error
from random import choice
from prettytable import PrettyTable

insults = ['пидор', 'лох', 'пидорас', 'чмо', 'чмошник', 'говно', 'уёбок',
           'петух', 'ушлёпок', 'гондон', 'блядь', 'ебанат', 'говнюк', 'урод',
           'дебил', 'спермобак', 'хуеблядь', 'чмошничек', 'гондонище',
           'мудозвон', 'мудак', 'гнида']
names_of_dick = ['пенис', 'член', 'хуй', 'писюн', 'хер', 'елдак', 'дилдак',
                 'удав']


def base_comm(command):
    with psycopg2.connect(user="phicxvcitlmbuj",
                          password="0e80d79a63bec606138c087b2312e51d97a4eca87fc84c03e2232f2c3db27275",
                          host="ec2-54-220-35-19.eu-west-1.compute.amazonaws.com",
                          port="5432", database="d9q40o7dpeuhj3") as base:
        cur = base.cursor()
        try:
            cur.execute(command)
        except Error:
            pass
        try:
            result = cur.fetchall()
        except Error:
            result = None
        base.commit()
        cur.close()
        return result


def create_tables():
    users_query = '''CREATE TABLE IF NOT EXISTS USERS 
                        (user_id INTEGER PRIMARY KEY NOT NULL,
                        username TEXT,
                        size_of_dick INTEGER,
                        last_dick_request TEXT);'''
    base_comm(users_query)


def print_base():
    with psycopg2.connect(user="phicxvcitlmbuj",
                          password="0e80d79a63bec606138c087b2312e51d97a4eca87fc84c03e2232f2c3db27275",
                          host="ec2-54-220-35-19.eu-west-1.compute.amazonaws.com",
                          port="5432", database="d9q40o7dpeuhj3") as base:
        cur = base.cursor()
        cur.execute('SELECT * FROM users')
        res = cur.fetchall()
        x = PrettyTable()
        x.field_names = ['id', 'Nickname', 'Dick', 'Dick Time']
        for i in res:
            x.add_row(i)
        return x


def reply_size_of_dick(message):
    bot.reply_to(message, 'Твой ' + choice(names_of_dick) + ' ' + str(
        base_comm(
            'SELECT size_of_dick FROM users WHERE user_id =' +
            str(message.from_user.id))[0][0]) + '-сантиметровый')


def register_user(user_id, username):
    user_check_query = f'SELECT * FROM USERS WHERE user_id = {user_id};'
    user_check_data = base_comm(user_check_query)
    reg_time = str(dt.datetime.now().year) + ' ' + str(
        dt.datetime.now().month) + ' ' + str(
        dt.datetime.now().day - 1)
    if not user_check_data:
        insert_to_db_query = f'''INSERT INTO USERS (user_id, username, 
                             size_of_dick, last_dick_request) VALUES ({user_id}, 
                             '{username}',{10},'{reg_time}');'''
        base_comm(insert_to_db_query)


def edit_size_of_dick(message, new_size):
    prev_size = base_comm(
        'SELECT size_of_dick FROM users WHERE user_id =' +
        str(message.from_user.id))[0][0]
    if (new_size != 0) and (prev_size + new_size >= 0):
        base_comm(
            'UPDATE users SET size_of_dick = ' + str(prev_size + new_size)
            + ' WHERE user_id = ' + str(message.from_user.id))
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
        base_comm(
            'UPDATE users SET size_of_dick = ' + str(0)
            + ' WHERE user_id = ' + str(message.from_user.id))
        bot.reply_to(message, 'Твой ' + choice(names_of_dick) + ' отвалился...')


def current_time():
    new_time = str(dt.datetime.now().year) + ' ' + str(
        dt.datetime.now().month) + ' ' + str(
        dt.datetime.now().day) + ' ' + str(dt.datetime.now(
    ).hour) + ' ' + str(dt.datetime.now().minute)
    return new_time


def pisun(message):
    last_req_list = list(map(int, base_comm(
        'SELECT last_dick_request FROM users WHERE user_id =' +
        str(message.from_user.id))[0][0].split()))
    last_req = dt.datetime(last_req_list[0], last_req_list[1], last_req_list[2])
    edit_sizes = [-10, -5, -6, -7, -4, -3, -2, -1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2,
                  2, 3, 3, 3, 3, -2, -3, -10, -1, 5, 4, 4, 4, 7, 7, 7, 8, 9, 10,
                  11, 2, 2, 4, 4, -3, 3, 6, 6, 2, 2, -1, -10, 5, 5, 3, 2, 2, 6,
                  4, 3, 5, 3, 3, 4, 0, 2, 4, 7, 5, 6, 3, 7, 8, 3, 6, 1, 1, 3, 6,
                  8, 6, 4, -3, -4, 5, 2, 6, 2, 7, 1, 4, 4, -2, -2]
    if dt.datetime(dt.datetime.now().year, dt.datetime.now().month,
                   dt.datetime.now().day) > last_req:
        edit_size_of_dick(message, choice(edit_sizes))
        new_time = str(dt.datetime.now().year) + ' ' + str(
            dt.datetime.now().month) + ' ' + str(
            dt.datetime.now().day)
        base_comm(
            'UPDATE users SET last_dick_request = ' + "'" + new_time + "'"
            + ' WHERE user_id = ' + str(message.from_user.id))
    else:
        bot.reply_to(message, 'Жди, ' + choice(insults) + '. Сегодня на твой '
                     + choice(names_of_dick) + ' смотреть не буду')


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


def top():
    S = sorted(list(map(list, base_comm('SELECT * FROM users'))), key=lambda
        x: x[2], reverse=True)
    return S


def console(message):
    bot.reply_to(message, eval(message.text))


bot = telebot.TeleBot('1791565125:AAH0BxQSJROn2zQLHkpKwtFlNB2sUuoTqfg')
message = bot.message_handlers


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(
        message, 'Привет, ' + choice(
            insults) +
                 '. Посмотрим на твой писюн.... так так так... Напиши «/писюн»')
    register_user(message.from_user.id, message.from_user.username)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text.lower() == 'длина хуя':
        reply_size_of_dick(message)
    elif message.text.lower() == 'расписание':
        bot.reply_to(message, school_schedule())
    elif message.text.lower() == '/писюн':
        pisun(message)
    elif message.text.lower() == 'время':
        bot.reply_to(message, current_time())
    elif message.text.lower() == 'консоль':
        if message.from_user.id == 410718594:
            bot.register_next_step_handler(message, console)
        else:
            bot.reply_to(message, 'Иди нахуй отсюда')
    elif message.text.lower() == '/топ':
        L = top()
        for i in range(len(L)):
            bot.send_message(message.chat.id,
                             str(i + 1) + '. ' + str(L[i][1]) + ' - ' + str(
                                 L[i][2]))


bot.polling(none_stop=True)
