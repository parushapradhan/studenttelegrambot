import json
import csv
import regex as re
import requests
from flask import Flask
from flask import request
from flask import Response
from flask_sslify import SSLify

# https://api.telegram.org/bot938702559:AAFbLXkr645nwkm5_pPZ4u9SFVPu7QxSg-Q/setWebHook?url=http://parushapradhan.pythonanywhere.com


token = "938702559:AAFbLXkr645nwkm5_pPZ4u9SFVPu7QxSg-Q"
app = Flask(__name__)


sslify = SSLify(app)


csvfile = open('SecA.csv', 'r')
jsonfile = open('SecA.json', 'w')

fieldnames = ("Day","8:45-9:45","9:45-10:45","10:45-10:55","10:55-11:55","11:55-12:55","12:55-1:30","1:30-2:30","2:30-3:30")
reader = csv.DictReader( csvfile, fieldnames)
for row in reader:
    json.dump(row, jsonfile)
    jsonfile.write('\n')





def write_json(msg, file):
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(msg, f, ensure_ascii=False, indent=4)

    f.close()
    print("doneee")

def parsemessage(msg):
    print("hpi")
    chat_id = msg['message']['chat']['id']
    message = msg['message']['text']
    # usn=re.findall(pattern,txt)
    print(message)
    return chat_id, message


def sendusn(chat_id, text):
    with open('STU_DETAILS.json') as json_file:
        data = json.load(json_file)
    i = 0
    studentdetails = data[0]
    flag=0
    print(type(text))
    print(type(data[i]['USN']))
    while i!=150:
        if data[i]['USN'] == text:
            print("condition sucess")
            flag=1
            studentdetails = data[i]
            break
        i = i+1
    if flag == 0:
        url = "https://api.telegram.org/bot938702559:AAFbLXkr645nwkm5_pPZ4u9SFVPu7QxSg-Q/sendMessage?chat_id=" + str(
            chat_id) + "&text=USN does not exist"
        payload = {chat_id: chat_id, text: text}
        r = requests.post(url, json=payload)
        return r
    else:
        message = json.dumps(studentdetails)
        print("After jsonfile")
        htmltrial="<b>hello</b><br>hi"
        url = "https://api.telegram.org/bot938702559:AAFbLXkr645nwkm5_pPZ4u9SFVPu7QxSg-Q/sendMessage?chat_id="+str(chat_id)+"&text="+message
        payload = {chat_id: chat_id, text: text}
        r = requests.post(url, json=payload)
        return r


def sendattendance(chat_id,usn):
    with open('ATTENDANCE.json') as json_file:
        data = json.load(json_file)
    i = 0
    studentdetails = data[0]
    while i!=150:
        if str(data[i]['USN']) == str(usn):
            print("condition sucess")
            studentdetails = data[i]
        i = i+1
    message = json.dumps(studentdetails)
    print("After jsonfile")
    url = 'https://api.telegram.org/bot938702559:AAFbLXkr645nwkm5_pPZ4u9SFVPu7QxSg-Q/sendMessage?chat_id='+str(chat_id)+'&text='+message
    payload = {chat_id: chat_id, usn: usn}
    r = requests.post(url, json=payload)
    return r


def sendscore(chat_id,usn):
    with open('SCORE.json') as json_file:
        data = json.load(json_file)
    i = 0
    studentdetails = data[0]
    flag=0
    print(usn)
    print(type(usn))
    while i!=150:
        print(data[i]['USN'])
        if data[i]['USN']==usn:
            flag=1
            print("condition sucess")
            studentdetails = data[i]
        i = i+1

    if flag==1:
        message = json.dumps(studentdetails)
        print("After jsonfile")
        url = "https://api.telegram.org/bot938702559:AAFbLXkr645nwkm5_pPZ4u9SFVPu7QxSg-Q/sendMessage?chat_id="+str(chat_id)+'&text='+message
        payload = {chat_id: chat_id, usn: usn}
        r = requests.post(url, json=payload)
        return r
    else:
        print("failed")


@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        msg = request.get_json()
        chat_id, message = parsemessage(msg)
        print(message)
        pattern="1NT16CS([0-9][0-9][0-9])"
        # usn = re.findall(pattern, message)
        m=re.match(pattern,message)
        if message =="/start":
            url = "https://api.telegram.org/bot938702559:AAFbLXkr645nwkm5_pPZ4u9SFVPu7QxSg-Q/sendMessage?chat_id=" + str(chat_id) + "&text=Please Enter your USN to start"
            payload = {chat_id: chat_id, message: message}
            requests.post(url, json=payload)
        if m:
            file1 = open("usn.txt", "w")
            file1.write(message)
            file1.close()
            sendusn(chat_id, message)
        elif message.lower() == "attendance":

            file1 = open("usn.txt","r")
            usn = file1.readline();
            print("Retrieved from txt file:"+usn)
            file1.close()

            sendattendance(chat_id,usn)

        elif message.lower() == "score":
            file1 = open("usn.txt", "r")
            usn = file1.readline();
            file1.close()
            sendscore(chat_id, usn)
        elif message.lower() =="command":
            url = "https://api.telegram.org/bot938702559:AAFbLXkr645nwkm5_pPZ4u9SFVPu7QxSg-Q/sendMessage?chat_id=" + str(chat_id) + "&text=The available commands are: attendance,score and your usn"
            payload = {chat_id: chat_id, message: message}
            requests.post(url, json=payload)
        else:
            url = "https://api.telegram.org/bot938702559:AAFbLXkr645nwkm5_pPZ4u9SFVPu7QxSg-Q/sendMessage?chat_id="+str(chat_id)+"&text=Sorry I do not recognize the command .Please only type in the commands that are available"
            payload = {chat_id: chat_id, message: message}
            requests.post(url, json=payload)

        return Response('OK', status=200)

    else:
        return Response("Ok",status=500)
        # return "<h1>not working</h1>"


def main():
    print("")


if __name__ == '__main__':
    app.run(debug=True)
