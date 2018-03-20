import time
import _thread as thread
import RPi.GPIO as GPIO
import telepot
import telepot.namedtuple
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
#import temp
#################### Code to constantly poll the motion and door sensor to detect intruder######################
def alarm():
    while True:
        if GPIO.input(pir_pin):
                print('Motion detected')
                GPIO.output(buzzer, True)
                break
        if GPIO.input(pin_door):
                print('Intruder detected !!!')
                GPIO.output(buzzer, True)
                break
        time.sleep(0.5)
##################################################################################################################
        
################################### Setup various GPIO PINS#######################################################
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
pin_door = 22
liv_light = 8
bed_light = 7
liv_fan = 18
bed_fan = 27
temp = 4
door_motor1 = 25
door_motor2 = 23
pir_pin = 17
buzzer = 24
GPIO.setup(pir_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(liv_light, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(door_motor1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(door_motor2, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(pin_door, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(liv_fan, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(buzzer, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(bed_fan, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(bed_light, GPIO.OUT, initial=GPIO.LOW)

#######################################################################################################################
# work on this code
door_status = 'locked'
bed_light_status = 'OFF'
bed_fan_status = 'OFF'
liv_fan_status = 'OFF'
liv_light_status = 'OFF'

#########################################################################################################################

######################################## This is the program entry point###########################################
'''This is where the program starts execution'''
bot = telepot.Bot('445691236:AAGpXCd1XE4k8QqlEpbnroAFzGXzNq493BM')
bot.message_loop({'chat': on_chat_message,
                  'callback_query': on_callback_query})
print('Listening ...')
while 1:
    time.sleep(10)

######################################################################################################################
# Definition of the on_chat_message function 
def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    global chaat
    chaat = chat_id
    if content_type == 'text':
        if msg['text'] == 'Main Menu':
            keyboard = [
                ['living-Room', 'Temperature'],
                ['Bedroom', 'Door'],
                ['Security', 'Home Status']
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard=keyboard)
            bot.sendMessage(chat_id, 'click on the menu', reply_markup=reply_markup)

        elif msg['text'] == '/start':
            keyboard = [
                ['living-Room', 'Temperature'],
                ['Bedroom', 'Door'],
                ['Security', 'Home Status']
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard=keyboard)
            bot.sendMessage(chat_id, 'Emmanuel with reg_No. MOUAU/12/23293, Welcome to your home. Give me any command '
                                     'by clicking on the menu below', reply_markup=reply_markup)

        elif msg['text'] == 'living-Room':
            keyboard = [['Living-Room Fan', 'Living-Room Light'], ['Main Menu']]
            reply_markup = ReplyKeyboardMarkup(keyboard=keyboard)
            bot.sendMessage(chat_id, 'Welcome to your Living-Room.', reply_markup=reply_markup)

        elif msg['text'] == 'Temperature':
            temp_c, temp_f = [122, 78.9] #temp.read_temp()
            temp_c = str(temp_c)
            temp_f = str(temp_f)
            print(temp_c)
            print(temp_f)
            keyboard = [['Main Menu']]
            reply_markup = ReplyKeyboardMarkup(keyboard=keyboard, one_time_keyboard=True)
            bot.sendMessage(chat_id, 'Temperature in degree is ' + temp_c + ' celsius')
            bot.sendMessage(chat_id, 'Temperature in Fahrenheit is ' + temp_f + ' fahrenheit', reply_markup=reply_markup)

        elif msg['text'] == 'Bedroom':
            keyboard = [['Bedroom Fan', 'Bedroom Light'], ['Main Menu']]
            reply_markup = ReplyKeyboardMarkup(keyboard=keyboard, one_time_keyboard=True)
            bot.sendMessage(chat_id, 'Welcome to your Bedroom', reply_markup=reply_markup)

        elif msg['text'] == 'Door':
            if door_status == 'locked':
                keyboard = telepot.namedtuple.InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Unlock Door', callback_data='unlock_door')]
                ])
                bot.sendMessage(chat_id, 'Should i unlock the door?', reply_markup=keyboard)
            elif door_status == 'unlocked':
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Lock Door', callback_data='lock_door')],

                ])
                bot.sendMessage(chat_id, 'Should i lock the door?', reply_markup=keyboard)

        elif msg['text'] == 'Security':
            keyboard = [['Shutdown Home', 'Activate Alarm', 'Deactivate Alarm'], ['Main Menu']]
            reply_markup = ReplyKeyboardMarkup(keyboard=keyboard, one_time_keyboard=True)
            bot.sendMessage(chat_id, 'What will you like to do?', reply_markup=reply_markup)

        elif msg['text'] == 'Shutdown Home':
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='SHUTDOWN', callback_data='All_OFF')],
                    ])
            bot.sendMessage(chat_id, 'You are about to shutdown all appliances?', reply_markup=keyboard)
        elif msg['text'] == 'Activate Alarm':
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Activate', callback_data='ALARM_ON')],
                    ])
            bot.sendMessage(chat_id, 'You are about to activate the alarm?', reply_markup=keyboard)
        elif msg['text'] == 'Deactivate Alarm':
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Deactivate', callback_data='ALARM_OFF')],
                    ])
            bot.sendMessage(chat_id, 'You are about to activate the alarm?', reply_markup=keyboard)



        elif msg['text'] == 'Home Status':
            keyboard = [['Main Menu']]
            reply_markup = ReplyKeyboardMarkup(keyboard=keyboard, one_time_keyboard=True)
            bot.sendMessage(chat_id, 'Living-Room light is  ' + liv_light_status)
            bot.sendMessage(chat_id, ' Living-Room fan is   ' + liv_fan_status)
            bot.sendMessage(chat_id, 'Bedroom Light is   ' + bed_light_status)
            bot.sendMessage(chat_id, 'Bedroom fan is  ' + bed_fan_status)
            bot.sendMessage(chat_id, 'Door is   ' + door_status, reply_markup=reply_markup)
    
        elif msg['text'] == 'Bedroom Fan':
            if bed_fan_status == 'OFF':
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Turn ON', callback_data='BEDFan_ON')],
                ])
                bot.sendMessage(chat_id, 'Should i turn on the fan?', reply_markup=keyboard)
            elif bed_fan_status == 'ON':
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                 [InlineKeyboardButton(text='Turn OFF', callback_data='BEDFan_OFF')],
                 ])
                bot.sendMessage(chat_id, 'Should i turn off the fan?', reply_markup=keyboard)

        elif msg['text'] == 'Bedroom Light':
            if bed_light_status == 'OFF':
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Turn ON', callback_data='BEDLight_ON')],
                ])
                bot.sendMessage(chat_id, 'Should i turn on the light?', reply_markup=keyboard)
            elif bed_light_status == 'ON':
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Turn OFF', callback_data='BEDLight_OFF')],
                ])
                bot.sendMessage(chat_id, 'Should i turn off the light?', reply_markup=keyboard)
        elif msg['text'] == 'Living-Room Fan':
            if liv_fan_status == 'OFF':
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Turn ON', callback_data='LIVFAN_ON')],
                ])
                bot.sendMessage(chat_id, 'Should i turn on the fan?', reply_markup=keyboard)
            elif liv_fan_status == 'ON':
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Turn OFF', callback_data='LIVFAN_OFF')],
                ])
                bot.sendMessage(chat_id, 'Should i turn off the fan?', reply_markup=keyboard)

        elif msg['text'] == 'Living-Room Light':
            if liv_light_status == 'OFF':
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Turn ON', callback_data='LIVLight_ON')]
                ])
                bot.sendMessage(chat_id, 'Should i turn on the light?', reply_markup=keyboard)
            elif liv_light_status == 'ON':
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Turn OFF', callback_data='LIVLight_OFF')],
                ])
                bot.sendMessage(chat_id, 'Should i turn off the light?', reply_markup=keyboard)
        else:
            bot.sendMessage(chat_id, 'please that command is invalid. Please send "/start" if you need help ')

################################################################################################################

#########################################Definition of callback query###########################################
def on_callback_query(msg):
    global door_status
    global bed_light_status
    global bed_fan_status
    global liv_fan_status
    global liv_light_status
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')

    if query_data == 'LIVFAN_OFF':
        bot.answerCallbackQuery(query_id, 'Fan Turned OFF')
        GPIO.output(liv_fan, False)
        liv_fan_status = 'OFF'

    elif query_data == 'LIVFAN_ON':
        bot.answerCallbackQuery(query_id, 'Fan Turned ON')
        GPIO.output(liv_fan, True)
        liv_fan_status = 'ON'

    elif query_data == 'LIVLight_ON':
        bot.answerCallbackQuery(query_id, 'Light Turned ON')
        GPIO.output(liv_light, True)
        liv_light_status= 'ON'

    elif query_data == 'LIVLight_OFF':
        bot.answerCallbackQuery(query_id, 'Light Turned OFF')
        GPIO.output(liv_light, False)
        liv_light_status = 'OFF'

    elif query_data == 'BEDLight_ON':
        bot.answerCallbackQuery(query_id, 'Light Turned ON')
        GPIO.output(bed_light, True)
        bed_light_status = 'ON'

    elif query_data == 'BEDLight_OFF':
        bot.answerCallbackQuery(query_id, 'Light Turned OFF')
        bed_light_status = 'OFF'
        GPIO.output(bed_light, False)

    elif query_data == 'BEDFan_ON':
        bot.answerCallbackQuery(query_id, 'Fan Turned ON')
        GPIO.output(bed_fan, True)
        bed_fan_status = 'ON'
        bot.sendMessage(chaat, 'click on the menu', reply_markup=reply_markup)

    elif query_data == 'BEDFan_OFF':
        bot.answerCallbackQuery(query_id, 'Fan Turned OFF')
        GPIO.output(bed_fan, False)
        bed_fan_status = 'OFF'
    elif query_data == 'unlock_door':
        bot.answerCallbackQuery(query_id, 'Door Unlocked')
        GPIO.output(door_motor1, True)
        GPIO.output(door_motor2, False)
        door_status = 'unlocked'

    elif query_data == 'lock_door':
        bot.answerCallbackQuery(query_id, 'Door Locked')
        GPIO.output(door_motor1, False)
        GPIO.output(door_motor2, True)
        door_status = 'locked'
    elif query_data == 'All_OFF':
        bot.answerCallbackQuery(query_id, 'Home shutdown')
        GPIO.output(liv_fan, False)
        #GPIO.output(pin_door, False)
        GPIO.output(bed_fan, False)
        GPIO.output(bed_light, False)
        GPIO.output(liv_light, False)
        door_status = 'OFF'
        bed_light_status = 'OFF'
        bed_fan_status = 'OFF'
        liv_fan_status = 'OFF'
        liv_light_status = 'OFF'
    elif query_data == 'ALARM_ON':
        bot.answerCallbackQuery(query_id, 'Alarm Activated')
        thread.start_new_thread(alarm, ())
    elif query_data == 'ALARM_OFF':
        GPIO.output(buzzer, False)
        bot.answerCallbackQuery(query_id, 'Alarm Deactivated')

    print('Callback Query:', query_id, from_id, query_data)
#########################################################################################################

