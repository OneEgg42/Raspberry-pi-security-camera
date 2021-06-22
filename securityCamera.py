import os
import time
import smtplib as smtp
from picamera import PiCamera
from email.message import EmailMessage

cam = PiCamera()
dest = ''

data_sent = False

sender = 'sender@gmail.com'
password = 'sender_password'
reciever = 'reciever@gmail.com'
subject = ''

def send_data(photo_path, photo_name):
    print('sending data...')

    server = smtp.SMTP_SSL('smtp.gmail.com', 465)
    server.login(sender, password)
    
    message = EmailMessage()
    message['Subject'] = subject
    message['To'] = reciever
    message['From'] = sender
    message.set_content('data from raspberry pi')

    with open(photo_path, 'rb') as file:
        data = file.read()
        name = photo_name
        file.close()

    message.add_attachment(data, maintype='image', subtype='jpeg', filename=name)

    server.send_message(message)
    

def take_photo(path, name):
    print('photo taken!')

    cam.capture(path + '/' + name + '.jpg')
    global subject
    subject = name + '.jpg'
    send_data(path + '/' + name + '.jpg', name + '.jpg')

def is_in_list(_list, _item):
    for i in _list:
        #print(i + ' ' + _item)
        if i == _item:
            #print('true')
            return True
    return False

time_of_day = ['','','']
just_photographed = False

#the numbers are the minute that a photo will be taken eg: 37 minutes past
minute_to_take_photo = ['37', '38']

while True:
    date = time.strftime('%d-%m-%y', time.localtime())
    time_of_day[0] = time.strftime('%H', time.localtime())
    time_of_day[1] = time.strftime('%M', time.localtime())
    time_of_day[2] = time.strftime('%S', time.localtime())
    photo_name = date+'-'+time_of_day[0]+'-'+time_of_day[1]+'-'+time_of_day[2]
    dest = '/home/pi/pythonstuff/securityCamTesting/' + date

    print(time_of_day)

    #print(date)

    #check if a folder had been created today:
    if not os.path.exists(date):
        #print('morning, creating a folder...')
        os.mkdir(date)
    else:
        pass
        #print('folder already created today')

    #taking photo
    if is_in_list(minute_to_take_photo, time_of_day[1]) and not just_photographed and time_of_day[2] == '00':
        take_photo(dest, photo_name)
        just_photographed = True
    if not time_of_day[2] == '00':
        just_photographed = False
    #\taking photo

    #print('just_photogrpahed = ' + str(just_photographed))
    time.sleep(0.5)
