import psycopg2
import telebot
import datetime as dt
from psycopg2 import Error
from random import choice
from prettytable import PrettyTable

insults = ['пидор', 'лох', 'пидорас', 'чмо', 'чмошник', 'говно', 'уёбок',
           'петух', 'ушлёпок', 'гондон', 'блядь', 'ебанат', 'говнюк', 'урод',
           'дебил', 'спермобак', 'хуеблядь', 'чмошничек', 'гондонище',
           'мудозвон', 'мудак', 'гнида', 'многоблядская проёбина',
           'трисратое говно', 'пиздомудопрохуёбина', 'шваль']

names_of_dick = ['пенис', 'член', 'хуй', 'писюн', 'хер', 'бананчик', 'дилдак',
                 'удав', 'змей горыныч', 'дружок']

names_of_pussy = ['вагина', 'киска', 'подружка']

names_of_pussy_second = ['вагину', 'киску', 'подружку']

edit_sizes = [-10, -5, -6, -7, -19, -18, -15, -1, 15,
              -15, -3, -10, 5, 40, 4, -200, 7, 7, 70, 8, 9, 10,
              11, 2, -8, 4, 4, 43, 3, 6, 60, 2, -6, -10, 5, 5, -333,
              -4, 6, 4, 3, 5, 3, 3, 4, 0, 4, 5, 6, 3, 7, 8, 3, 6,
              -5, 3, 6, 8, 6, 4, -300, -4, 5, -13, 6, 10, 7, -44, 4, -16, -16,
              5, 4, 5, 3, -2, -5, 6, 4, -6, 4, 4, 4, 7, 7, 8, 6, 7, 5, 91, 6, 7,
              -9, - 7, - 7, -5, -18, -6, -100, 6, 120, -666, 6, 17]

TUESDAY_SCHEDULE = [
    (dt.timedelta(hours=8, minutes=30), dt.timedelta(hours=9, minutes=10)),
    (dt.timedelta(hours=9, minutes=25), dt.timedelta(hours=10, minutes=5)),
    (dt.timedelta(hours=10, minutes=20), dt.timedelta(hours=11)),
    (dt.timedelta(hours=11, minutes=15), dt.timedelta(hours=11, minutes=35)),
    (dt.timedelta(hours=11, minutes=40), dt.timedelta(hours=12, minutes=20)),
    (dt.timedelta(hours=12, minutes=35), dt.timedelta(hours=13, minutes=15)),
    (dt.timedelta(hours=13, minutes=30), dt.timedelta(hours=14, minutes=10)),
    (dt.timedelta(hours=14, minutes=20), dt.timedelta(hours=15))]

OTHER_DAYS_SCHEDULE = [
    (dt.timedelta(hours=8, minutes=30), dt.timedelta(hours=9, minutes=10)),
    (dt.timedelta(hours=9, minutes=30), dt.timedelta(hours=10, minutes=10)),
    (dt.timedelta(hours=10, minutes=30), dt.timedelta(hours=11, minutes=10)),
    (dt.timedelta(hours=11, minutes=30), dt.timedelta(hours=12, minutes=10)),
    (dt.timedelta(hours=12, minutes=30), dt.timedelta(hours=13, minutes=10)),
    (dt.timedelta(hours=13, minutes=25), dt.timedelta(hours=14, minutes=5)),
    (dt.timedelta(hours=14, minutes=15), dt.timedelta(hours=14, minutes=55))]


def base_comm(command):
    with psycopg2.connect(user="tsddxqfczcgkrt",
                          password="76866820258eaf3ea537e76afc4780d37c31a9"
                                   "b9b39b3baaa7fa209b700432e8",
                          host="ec2-63-34-97-163.eu-west-1.compute.amazona"
                               "ws.com",
                          port="5432", database="d8505ifjvpmnpu") as base:
        cur = base.cursor()
        try:
            cur.execute(command)
        except Error:
            pass
        try:
            result = cur.fetchall()
        except Error:
            result = [['None']]
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
    res = base_comm('SELECT * FROM users')
    x = PrettyTable()
    x.field_names = ['id', 'Nickname', 'Dick', 'Dick Time']
    for i in res:
        x.add_row(i)
    return x


def reply_size_of_dick(messag):
    if base_comm('SELECT size_of_dick FROM users WHERE user_id =' + str(
            messag.from_user.id))[0][0] >= 0:
        bot.reply_to(messag, 'Твой ' + choice(names_of_dick) + ' ' + str(
            base_comm(
                'SELECT size_of_dick FROM users WHERE user_id =' +
                str(messag.from_user.id))[0][0]) + '-сантиметровый')
    else:
        bot.reply_to(messag, 'Твоя ' + choice(names_of_pussy) + ' ' + str(abs(
            base_comm(
                'SELECT size_of_dick FROM users WHERE user_id =' +
                str(messag.from_user.id))[0][0])) + '-сантиметровая')


def register_user(user_id, username):
    user_check_data = base_comm(
        f'SELECT * FROM USERS WHERE user_id = {user_id};')
    date_now = dt.datetime.now() + dt.timedelta(hours=3) - dt.timedelta(days=1)
    reg_time = str(date_now.year) + ' ' + str(date_now.month) + ' ' + str(
        date_now.day)
    if not user_check_data:
        insert_to_db_query = f'''INSERT INTO USERS (user_id, username, 
                             size_of_dick, last_dick_request) VALUES ({user_id}, 
                             '{username}',{10},'{reg_time}');'''
        base_comm(insert_to_db_query)


def edit_size_of_dick(messag, new_size):
    prev_size = base_comm('SELECT size_of_dick FROM users WHERE user_id =' +
                          str(messag.from_user.id))[0][0]
    if (new_size != 0) and (prev_size + new_size >= 0):
        base_comm('UPDATE users SET size_of_dick = ' + str(prev_size + new_size)
                  + ' WHERE user_id = ' + str(messag.from_user.id))
        if new_size > 0:
            bot.reply_to(messag,
                         'Твой ' + choice(names_of_dick) + ' вырос на '
                         + str(new_size)
                         + ' см. Теперь он ' + str(new_size + prev_size)
                         + '-сантиметровый')
        else:
            bot.reply_to(messag, 'Твой ' + choice(names_of_dick)
                         + ' уменьшился на ' + str(abs(new_size))
                         + ' см. Теперь он ' + str(new_size + prev_size)
                         + '-сантиметровый')
    elif new_size == 0:
        base_comm('UPDATE users SET size_of_dick = ' + str(0)
                  + ' WHERE user_id = ' + str(messag.from_user.id))
        bot.reply_to(messag, 'Твой ' + choice(names_of_dick) + ' отвалился...')
    else:
        base_comm('UPDATE users SET size_of_dick = ' + str(prev_size + new_size)
                  + ' WHERE user_id = ' + str(messag.from_user.id))
        if new_size > 0:
            bot.reply_to(messag,
                         'Твоя ' + choice(names_of_pussy) + ' уменьшилась на '
                         + str(abs(new_size))
                         + ' см. Теперь она ' + str(abs(new_size + prev_size))
                         + '-сантиметровая')
        else:
            bot.reply_to(messag,
                         'Твоя ' + choice(names_of_pussy) + ' увеличилась на '
                         + str(abs(new_size))
                         + ' см. Теперь она ' + str(abs(new_size + prev_size))
                         + '-сантиметровая')


def pisun(messag):
    last_req_list = list(map(int, base_comm(
        'SELECT last_dick_request FROM users WHERE user_id =' +
        str(messag.from_user.id))[0][0].split()))
    last_req = dt.datetime(last_req_list[0], last_req_list[1],
                           last_req_list[2])
    date_now = dt.datetime.now() + dt.timedelta(hours=3)
    if dt.datetime(date_now.year, date_now.month, date_now.day) > last_req:
        edit_size_of_dick(messag, choice(edit_sizes))
        new_time = str(date_now.year) + ' ' + str(
            date_now.month) + ' ' + str(
            date_now.day)
        base_comm(
            'UPDATE users SET last_dick_request = ' + "'" + new_time + "'"
            + ' WHERE user_id = ' + str(messag.from_user.id))
    else:
        if base_comm('SELECT size_of_dick FROM users WHERE user_id =' + str(
                messag.from_user.id))[0][0] >= 0:
            bot.reply_to(messag,
                         'Жди, ' + choice(insults) + '. Сегодня на твой '
                         + choice(names_of_dick) + ' смотреть не буду')
        else:
            bot.reply_to(messag,
                         'Жди, ' + choice(insults) + '. Сегодня на твою '
                         + choice(names_of_pussy_second) + ' смотреть не буду')


def school_schedule(messag):
    date_week = dt.datetime.now().weekday()
    time = dt.timedelta(hours=int(dt.datetime.now().hour) + 3,
                        minutes=dt.datetime.now().minute)
    flag = 0
    if date_week == 1:
        for i in TUESDAY_SCHEDULE:
            if i[0] <= time <= i[1]:
                bot.send_message(messag.chat.id,
                                 str((i[1] - time).seconds // 60) + ' minutes.')
                flag = 1
    else:
        for i in OTHER_DAYS_SCHEDULE:
            if i[0] <= time <= i[1]:
                bot.send_message(messag.chat.id,
                                 str((i[1] - time).seconds // 60) + ' minutes.')
                flag = 1
    if not flag:
        bot.send_message(messag.chat.id, 'Иди спи')


def top(messag):
    try:
        top_str = ''
        top_list = sorted(list(map(list, base_comm('SELECT * FROM users'))),
                          key=lambda x: x[2], reverse=True)
        for i in range(len(top_list)):
            top_str += str(i + 1) + '. ' + str(
                top_list[i][1]) + ' - ' + str(
                top_list[i][2]) + '\n'
        bot.send_message(messag.chat.id, top_str)
    except Error:
        bot.send_message(messag.chat.id, 'FAIL')


def which_size(messag):
    def which_size_second_part(messag2):
        if messag2.text.isdigit():
            a = float(messag2.text)
            if a == 0:
                text_to_send = 'Иди отсюда'
            elif 0 < a <= 14:
                text_to_send = 'У тебя короткая пипка, соболезную'
            elif 14 < a < 20:
                text_to_send = 'У тебя средняя пипка'

            elif 20 <= a < 35:
                text_to_send = 'Хм, неплохо. У тебя большая пипка'
            else:
                text_to_send = 'Так все и поверили... Ебанутый?'
        else:
            text_to_send = 'ЧИСЛАМИ ПИШИ, БЛЯТЬ!'
        bot.reply_to(messag2, text_to_send)

    bot.send_message(messag.chat.id, 'Привет! Напиши число, '
                                     'какая у тебя пиписька в реальной жизни))')
    bot.register_next_step_handler(messag, which_size_second_part)


def send_to(chat, messag, number_of_message=1):
    try:
        for i in range(number_of_message):
            bot.send_message(chat, messag)
        return 'Success'
    except Error:
        return 'Error'


def console(messag):
    try:
        result = eval(messag.text)
    except Error:
        result = 'FAIL'
    bot.reply_to(messag, result)


def edit_base(cell, new_value, user_id):
    try:
        base_comm(f"UPDATE users SET {cell} = {new_value} WHERE user_id = "
                  f"{user_id}")
        return 'SUCCESS'
    except Error:
        return 'FAIL'


bot = telebot.TeleBot('1802055834:AAGLF4vOyLardyZBdA8Nk0yz0XXfBF_UuYA')
message = bot.message_handlers


@bot.message_handler(commands=['start'])
def start(messag):
    keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
    keyboard.row('/писюн', '/топ')
    keyboard.row('/длина', '/размер')
    bot.send_message(
        messag.chat.id,
        'Привет, ' + choice(insults) + '. Посмотрим на твой писюн....'
                                       ' так так так... Напиши «/писюн»')
    register_user(messag.from_user.id, messag.from_user.username)


@bot.message_handler(commands=['help'])
def help(messag):
    bot.reply_to(messag, 'Вот основные команды:'
                         '\n/писюн - проверить свой писюн\n/топ - '
                         'список рекордсменов\n/длина - посмотреть длину '
                         'писюна\n/размер - профессиональная оценка твоего '
                         'писюна')


@bot.message_handler(commands=['pisun'])
def command_pisun(messag):
    pisun(messag)


@bot.message_handler(commands=['my_length'])
def command_reply_size_of_dick(messag):
    reply_size_of_dick(messag)


@bot.message_handler(commands=['top'])
def command_top(messag):
    top(messag)


@bot.message_handler(content_types=['text'])
def get_text_messages(messag):
    if messag.text.lower() == '/длина':
        reply_size_of_dick(messag)
    elif messag.text.lower() == '/топ':
        top(messag)
    elif messag.text.lower() == '/писюн':
        pisun(messag)
    elif messag.text.lower() == '/размер':
        which_size(messag)
    elif messag.text.lower() == '/school':
        school_schedule(messag)
    elif messag.text.lower() == 'cmd':
        if messag.from_user.id == 410718594:
            bot.register_next_step_handler(messag, console)
        else:
            pass


bot.polling(none_stop=True)
