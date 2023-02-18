#importing neccesary libraries
import telebot
from datetime import datetime, timedelta
import mysql.connector

#create function store booking details in database
def save_to_database(name, location, category, dates, time_opt):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Anugrah@0811",
        database="vaccinedb",
        auth_plugin='mysql_native_password'
    )
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            location VARCHAR(255),
            category VARCHAR(255),
            date VARCHAR(255),
            time VARCHAR(255)
        )
    """)
    cursor.execute("INSERT INTO appointments (name, location, category, date, time) VALUES (%s, %s, %s, %s, %s)",
                   (name, location, category, dates, time_opt))
    conn.commit()
    cursor.close()
    conn.close()





#get token from BOTFATHER
TOKEN = '5768256572:AAEFmkn3ew3oNOKW8-NhUKXCTjzpKDlV_nU'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_booking(message):
    bot.send_message(chat_id=message.chat.id, text='Welcome to Vaccination Booking Bot\n\nSelect and Type following options\n Book ---> type /book\n Cancel  ---> type /cancel \n Quit ---> type /quit  ')
    #bot.register_next_step_handler(message, get_option)


@bot.message_handler(commands=['book'])
def get_option(message): 
    option = message.text
    bot.send_message(chat_id=message.chat.id, text='Please type in your Name')
    bot.register_next_step_handler(message, get_name, option=option)


def get_name(message, option):
    name = message.text
    bot.send_message(chat_id=message.chat.id, text='Please type in your Location')
    bot.register_next_step_handler(message, get_location, option=option , name=name)

def get_location(message,option,name):
    location = message.text
    bot.send_message(chat_id=message.chat.id, text='What service would you like to book an appointment for?\n\n'
                                                   '1. Covid-19 Vaccination\n'
                                                   '2. Flu Shot\n'
                                                   '3. Dengue Vaccine')
    bot.register_next_step_handler(message, get_category, name=name, location=location)
    
def get_category(message, name, location):
    category = message.text
    if category == '1':
        category = "Covid-19 Vaccination"
    elif category=='2':
        category = "Dengue Vaccine"
    elif category=='2':
        category = "Flu Shot"
    else:
        bot.send_message(chat_id=message.chat.id, text='please select valid service!')
        bot.register_next_step_handler(message, get_category, name=name, location=location)
    
    now = datetime.now()
    dates = []
    for i in range(3):
        next_date = now + timedelta(days=i)
        dates.append(next_date.strftime("%m/%d/%Y %A"))
    bot.send_message(chat_id=message.chat.id, text='Select Date from below option\n\n''Here are the next three dates available:\n\n' + '\n'.join(f'{i+1}. {date}' for i, date in enumerate(dates)) 
                     + '\n\nPlease select a date by typing in the corresponding number:')

    bot.register_next_step_handler(message, get_date, name=name, location=location, category=category)
    

def get_date(message, name, location, category):
    date_opt=message.text
    now = datetime.now()
    dates = []
    for i in range(3):
        next_date = now + timedelta(days=i)
        dates.append(next_date.strftime("%m/%d/%Y %A"))
    if date_opt == '1':
        date_opt = dates[0]
    elif date_opt=='2':
        date_opt = dates[1]
    else:
        date_opt = dates[2]
    
    time_slots = ['Time slot 1: [09:00 AM]', 'Time slot 2: [12:00 PM]', 'Time slot 3: [03:00 PM]']
    bot.send_message(chat_id=message.chat.id, text=f'For {date_opt} the following time slots are available:\n\n' + '\n'.join(f'{i+1}. {slot}' for i, slot in enumerate(time_slots))
                     + '\n\nPlease select a time by typing in the corresponding number:')
    
    bot.register_next_step_handler(message, get_time, name=name, location=location, category=category, dates=date_opt)


def get_time(message, name, location, category, dates):
    time_opt=message.text
    
    time_slots = ['Time slot 1: [09:00 AM]', 'Time slot 2: [12:00 PM]', 'Time slot 3: [03:00 PM]']
    if time_opt == '1':
        time_opt = time_slots[0]
    elif time_opt=='2':
        time_opt = time_slots[1]
    else:
        time_opt = time_slots[2]
    
    bot.send_message(chat_id=message.chat.id, text=f'Finally the Booking Message with Date & Time for Confirmation.\n\n'
                                                   f'Name: {name}\nLocation: {location}\nCategory: {category}\n'
                                                   f'Date: {dates}\nTime: {time_opt}\n\n Enter Stop or Quit to exit')
    
    save_to_database(name, location, category, dates, time_opt)
    
    bot.register_next_step_handler(message, get_confirmation)



def get_confirmation(message):
    if message.text.lower() in ['stop', 'quit']:
        bot.send_message(chat_id=message.chat.id, text='Thank you for Vaccination Booking!')
        return

    
@bot.message_handler(commands=['cancel'])
def handle_cancellation(message):
    bot.reply_to(message, "Welcome to the cancellation system! Please enter your appointment ID.")
    bot.register_next_step_handler(message, get_appointment_id)

def get_appointment_id(message):
    # code to handle getting user's appointment ID
    bot.reply_to(message, "Are you sure you want to cancel this appointment?")
    bot.reply_to(message, "1. Yes\n2. No")
    bot.register_next_step_handler(message, get_cancellation_confirmation)

def get_cancellation_confirmation(message):
    # code to handle getting user's cancellation confirmation
    bot.send_message(chat_id=message.chat.id, text='Your appointment has been cancelled. Thank you.')
    # code to cancel the appointment

@bot.message_handler(commands=['quit'])
def handle_cancellation(message):
    bot.send_message(chat_id=message.chat.id, text='Goodbye!')
    return   

#Driver Function
bot.polling()