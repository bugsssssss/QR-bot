import telebot
from PIL import Image
import qrcode
import json
import datetime
from telebot import types

TOKEN = "6900424648:AAH8XASmWfcqtqb-UEgmy6yPi3k5Y5HvtYQ"


bot = telebot.TeleBot(token=TOKEN)
user_data = []
assert_colors = []
all_colors = {}


@bot.message_handler(commands=['start'])
def start(message):
    global count, all_colors
    count = 1
    if message.from_user.last_name is None:
        greeting = f'''🚀 Hello {message.from_user.first_name}.\nWelcome to QR-code bot. I can do two things for you:\n
- 🕵️‍ Scan a QR or Barcode: Send me a photo and I will do my best to decode it.
- ⚙️ Generate a QR Code image: Send any information (even emoji) you may have and I will create a QR code image.\n\n\n💻 Created by @buggsssss\n
        '''
        bot.send_message(message.chat.id, greeting, parse_mode='html')
    else:
        greeting = f'''🚀 Hello {message.from_user.first_name}.\nWelcome to QR-code bot. I can do two things for you:\n
- 🕵️‍ Scan a QR or Barcode: Send me a photo and I will do my best to decode it.
- ⚙️ Generate a QR Code image: Send any information you may have and I will create a QR code image.\n\n\n💻 Created by @buggsssss\n
        '''
        bot.send_message(message.chat.id, greeting, parse_mode='html')
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(
        'Instagram', url='https://www.instagram.com/_1nurbek/')
    button2 = types.InlineKeyboardButton(
        'Github', url='https://github.com/bugsssssss')
    markup.add(button1, button2)
    bot.send_message(message.chat.id, 'Find me on: ', reply_markup=markup)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    white = types.KeyboardButton('⚫️⚪️ Black-white')
    red = types.KeyboardButton('⚫️🔴 Black-red')
    blue = types.KeyboardButton('⚫️🔵 Black-blue')
    purple = types.KeyboardButton('⚫️🟣 Black-purple')
    orange = types.KeyboardButton('⚫️🟠 Black-orange')
    yellow = types.KeyboardButton('⚫️🟡 Black-yellow')
    bp_edition = types.KeyboardButton('🖤💖 Black-pink')
    all_buttons = [white, red, blue, purple, orange, yellow, bp_edition]
    markup.add(white, red, blue, purple, orange, yellow, bp_edition)
    all_colors = {
        white.text: '#ffffff',
        red.text: '#DD5353',
        blue.text: '#5F9DF7',
        purple.text: '#7743DB',
        orange.text: '#FD841F',
        yellow.text: '#FCE700',
        bp_edition.text: 'pink'
    }
    for clr in all_buttons:
        assert_colors.append(clr.text)
    # print(assert_colors, all_colors)
    bot.send_message(
        message.chat.id, text=f'Please choose the style\nor just send any text to start ', reply_markup=markup)


count = 1
style = 'white'
style_data = 'default'


@bot.message_handler(content_types=['text'])
def get_background(message):
    global style, count, style_data
    if message.text in assert_colors:
        for clr in all_colors:
            if message.text == clr:
                style = all_colors[clr]
                style_data = clr
        bot.send_message(
            message.chat.id, f'Alright, style was updated. Its almost done, send your text i will make QR-img for you 🤔')
    print(style, count)

    # color edit
    if message.text not in assert_colors:
        version = 2
        size = 10
        border = 1
        fcolor = 'black'
        bcolor = style
        qr = qrcode.QRCode(version=version, box_size=size, border=border)
        qr.add_data(message.text)
        qr.make(fit=True)
        img = qr.make_image(fill_color=fcolor, back_color=bcolor)
        # img = qrcode.make(message.text)
        # type(img)
        img.save('myqr.png')
        user_data.append({
            message.from_user.first_name: message.text,
            'time': datetime.datetime.today().strftime('%D %H:%M:%S'),
            'style': style_data[3:].strip()
        })
        with open('user_data.json', 'w', encoding='utf-8') as file:
            file.write(json.dumps(user_data, indent=3, ensure_ascii=False))
        bot.send_message(message.chat.id, 'Processing...')
        bot.send_photo(message.chat.id, photo=open(
            'myqr.png', 'rb'), caption='Here is your QR-code 🥳')
        response_for_me = f'''
user: <b>{message.from_user.first_name}</b>
username: <b>@{message.from_user.username}</b>
text: <b>{message.text}</b>
time: <b>{datetime.datetime.today().strftime('%D %H:%M:%S')}</b> 
'''
        bot.send_message(657061394, response_for_me, parse_mode='HTML')


# @bot.message_handler(content_types=['text'])
# def getUserText(message):
#     if message.text not in all_colors:
#         # user_data[message.from_user.first_name] = message.text
#         user_data.append({
#             message.from_user.first_name: message.text,
#             'time': datetime.datetime.today().strftime('%D %H:%M:%S')
#         })
#         with open('user_data.json', 'w') as file:
#             file.write(json.dumps(user_data, indent=3))


#         # color edit
#         version = 2
#         size = 10
#         border = 1
#         fcolor = foreground_color
#         bcolor = background_color
#         qr = qrcode.QRCode(version=version, box_size=size,border=border)
#         qr.add_data(message.text)
#         qr.make(fit=True)
#         img = qr.make_image(fill_color = fcolor, back_color = bcolor)
#         # img = qrcode.make(message.text)
#         # type(img)
#         img.save('myqr.png')
#         bot.send_message(message.chat.id, 'Processing...')
#         bot.send_photo(message.chat.id, photo=open(
#             'myqr.png', 'rb'), caption='Here is you QR-code :)')


@bot.message_handler(content_types=['photo'])
def handle_docs_photo(message):
    file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    src = 'decode_qr/last_decoded.png'
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.reply_to(message, "Let\'s see...")
    img = cv2.imread(src)
    detector = cv2.QRCodeDetector()
    data, bbox, straigh_qrcode = detector.detectAndDecode(img)
    if bbox is not None:
        bot.send_message(
            message.chat.id, f'Here is all data from your QR-code:\n\n<b>{data}</b>', parse_mode='html')
        response_for_me = f'''
user: <b>{message.from_user.first_name}</b>
username: <b>@{message.from_user.username}</b>
text: <b>{data}</b>
time: <b>{datetime.datetime.today().strftime('%D %H:%M:%S')}</b>  
'''
        bot.send_message(657061394, response_for_me, parse_mode='HTML')
    #     n_lines = len(bbox)
    #     for i in range(n_lines):
    #         point1 = tuple(bbox[i][0])
    #         point2 = tuple(bbox[(i+1)%n_lines][0])
    #         cv2.line(img, point1, point2, color=(255, 0, 0), thickness=2)
    # cv2.imshow('decode_qr/photos/file_1.jpg', img)
    else:
        bot.send_message(
            message.chat.id, f'Sorry, seems it is not a qr-code :(', parse_mode='html')
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    user_data.append({
        'Username': message.from_user.first_name,
        'type': 'decode',
        'decoded_text': data,
        'time': datetime.datetime.today().strftime('%H:%M:%S')
    })
    with open('user_data.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(user_data, indent=3, ensure_ascii=False))


# replying with buttons, here u can add some links and stuff like this
# @bot.message_handler(content_types=['text'])
# def button_message(message):
#     markup = types.InlineKeyboardMarkup()
#     item1 = types.InlineKeyboardButton('Кнопка', url='https://allplay.uz')
#     item2 = types.InlineKeyboardButton('Кнопка 2', url='https://allplay.uz')
#     markup.add(item1, item2)
#     bot.send_message(message.chat.id, "Choose background color: ", reply_markup=markup)


bot.infinity_polling()

# @bot.message_handler(content_types=['photo'])
# def get_user_photo(message):
#     bot.send_message(message.chat.id, 'Wow, cool pic, is this You?')
# @bot.message_handler(commands=['help'])
# def help(message):
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
#     website = types.KeyboardButton('Let\'s make QR!')
#     start = types.KeyboardButton('Start')
#     allplay = types.KeyboardButton('Allplay')
#     gitHub = types.KeyboardButton('GitHub')
#     markup.add(website)
#     bot.send_message(message.chat.id, 'Watch TV and movies!', reply_markup=markup)
# bot.polling(none_stop=True)
