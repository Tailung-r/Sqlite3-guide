import telebot
from telebot import types
import sqlite3
token = "" #Your Bot token
bot = telebot.TeleBot(token)

name = '' #global var

@bot.message_handler(commands=['start']) #any command
def meow(message):
    conn = sqlite3.connect('tai.sql') #name your database
    cur = conn.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS users (id int auto_increpent primary key, name varchar(50), pass varchar(50))") #this command create a table, when user use /start
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, 'Hello, We will register you now!, Enter your name!') #this command will get one of the table data
    bot.register_next_step_handler(message, user_name) #move to next function

def user_name(message):
    global name #set 'name' to global var
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Enter your password') #getting the password for our table
    bot.register_next_step_handler(message, user_pass) #move to next function

def user_pass(message): #Adding a user to the database
    password = message.text.strip()
    conn = sqlite3.connect('tai.sql') 
    cur = conn.cursor()

    cur.execute("INSERT INTO users (name, pass) VALUES ('%s', '%s')" % (name,password)) #The adding method is taken from (https://www.youtube.com/@gosha_dudar) thx him!
    conn.commit()
    cur.close()
    conn.close()

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('User list', callback_data='list')) #our User list
    bot.send_message(message.chat.id, 'User was registered', reply_markup=markup) #our User was registered

@bot.callback_query_handler(func = lambda callback : True) #our callback def
def callback_message(callback):
    if callback.data == 'list': #Checking that we are accessing the database exactly
        conn = sqlite3.connect('tai.sql')
        cur = conn.cursor()

        cur.execute("SELECT * FROM users") #Accessing data from a database
        users = cur.fetchall()
        info = ''
        for el in users:
            info += f'Name: {el[1]}, password: {el[2]}\n'
        cur.close()
        conn.close()

        bot.send_message(callback.message.chat.id, info)
    

bot.polling(non_stop=True)
