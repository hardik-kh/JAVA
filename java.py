from os import name
import os
import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import urllib.request
import urllib.parse
import re
import smtplib
from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from javaUI import Ui_MainWindow
import sys
from keyboard import press_and_release
import cv2
from face_recognition import face_encodings,compare_faces
import json
import requests
from googletrans import Translator
import random
import geocoder
import threading

engine = pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
global val
val=3
engine.setProperty('voice',voices[val].id)
# print(voices)
engine. setProperty("rate", 150)
chrome_path = '"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" %s'
password="your password"


def takeCommand(lang):
    ## It takes command from microphone 
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 100
        r.adjust_for_ambient_noise(source=source,duration=1)
        audio = r.listen(source)
        
    try:
        print("Recognizing...")
        query = r.recognize_google(audio,language=lang)
        print("User said : ",query)
    except Exception as e:
        ##print(e)
        if(lang=="en-ind"):
            print("Say that again")
        else:
            print("फिर से कहो")
        return "None"
    return query

def sendEmail(to,content):
    server= smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login('your mail',password)
    if(lang=='hi-IN'):
        translator = Translator(service_urls=['translate.googleapis.com'])
        content = translator.translate(text=content, dest='hi', src='en').text
    server.sendmail('your mail',to,content)
    server.close()  

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour=int(datetime.datetime.now().hour)
    if(hour>=5 and hour<12):
        speak("Good Morning "+name+" How can i help you")
    elif(hour>=12 and hour<=16):
        speak("Good afternoon "+name+" How can i help you")
    else:
        speak("Good evening "+name+" How can i help you")

def time():
    hour=int(datetime.datetime.now().hour)
    min=str(datetime.datetime.now().minute)
    l=['शून्य','एक ',	'दो  ',	'तीन ',	'चार ',	'पांच ',	'छह ',	'सात ',	'आठ ',	'नौ ',	'दस',	'ग्यारह ',	'बारह',
        'तेरह ',	'चोदह',	'पंद्रह ',	'सोलह ',	'सत्त्रह ',	'अट्ठारह ',	'उन्नीस ',	'बीस ',	'इक्कीस',	'बाइस ',	'तेईस ',
            'चौबीस ',	'पच्चीस ',	'छब्बीस ',	'सत्ताइस ',	'अट्ठाइस ',	'उन्तीस ',	'तीस ',	'इकतीस',	'बत्तीस ',	'तैतीस ',
                'चौतीस',	'पैतीस ',	'छत्तीस',	'सैतीस ',	'अड़तीस',	'उन्तालीस ',	'चालीस ',	'इकतालीस ',	'बयालीस',
                    'तिरतालिस',	'चौवालीस ',	'पैतालीस ',	'छयालीस ',	'सैतालिस ',	'अड़तालीस ',	'उनचास ',	'पचास ',
                        'इक्क्यावन',	'बावन ',	'तिरपन',	'चौवन ',	'पचपन ',	'छप्पन ',	'सत्तावन ',	'अट्ठावन ',
                            'उनसठ ',	'साठ ',]
    if(hour>12):
        hour=str(hour-12)
        if(lang=="en-ind"):
            print("It is "+hour+min+" pm "+new_name[0])
            speak("It is "+hour+min+" pm "+new_name[0])
        else:
            speak("अभी "+l[int(hour)]+" बजकर "+l[int(min)]+" मिनट हो रहे हैं")
    else:
        hour=str(hour)
        if(lang=="en-ind"):
            print("It is "+hour+min+" am "+new_name[0])
            speak("It is "+hour+min+" am "+new_name[0])
        else:
            speak("अभी "+l[int(hour)]+" बजकर "+l[int(min)]+" मिनट हो रहे हैं")

def intro():
    if (lang == 'en-ind'):
        speak(
            "My name is java. Short for just awesome voice assistant. I was created by hardik khandelwal and Sarthak Tyagi to take commands through voice")
    else:
        speak("मेरा नाम जावा है। मुझे हार्दिक खंडेलवाल और सार्थक त्यागी ने आवाज के जरिए कमांड लेने के लिए बनाया है")

def recognition():
    global name , role
    query=""
    frameWidth = 640
    frameHeight = 480
    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    cap.set(3, frameWidth)
    cap.set(4, frameHeight)
    cap.set(10,150)
    encode1=0
    while (type(encode1)==int):
        success, img1 = cap.read()
        imgGray = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
        img1 = cv2.flip(img1,1)
        imgGray = cv2.flip(imgGray,1)
        try:
            encode1 = face_encodings(img1)[0]
            if type(encode1)!=int:
                break
        except Exception as e:
            print("",end="")
    l=[]
    fl = open("data.txt","r")
    v=fl.readlines()
    n=len(v)
    check=0
    a=0
    for i in range(0,n//130):  
        for j in range(a,a+128):
            l.append(float(v[j]))
        a=a+130
        results = compare_faces([l],encode1)
        results[0] = str(results[0])
        if(results[0]=="True"):
            print("working")
            name=v[j+1]
            role = v[j+2]
            check=1
            break
        l.clear()    
    fl.close()
    if(check==0):
        fl = open("data.txt","a")
        fl.write("\n")
        for i in encode1:
            fl.write(str(i)+"\n")
        speak("What is your name")
        while(query=="" or type(query)==None or query=="none" or query =="None"):
            query = takeCommand('hi-IN')
        # query= query.lower()
        print(type(query))
        query = query.replace('माई','')
        query = query.replace('माय','')
        query = query.replace('नेम','')
        query = query.replace('इज','')
        query = "मेरा" + " नाम " + '"' +query+ '"' + " है" 
        print(query)
        a = Translator(service_urls=['translate.googleapis.com'])
        query = a.translate(text=query, dest='en', src='hi').text
        query = query.lower()
        print(query)
        query = query.replace('my','')
        query = query.replace('name','')
        query = query.replace('is','')
        name = query
        fl.write(name)
        fl.write('\nuser')
        fl.close()


def recog():
    query,name1,role1 = "","",""
    frameWidth = 640
    frameHeight = 480
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(3, frameWidth)
    cap.set(4, frameHeight)
    cap.set(10, 150)
    encode1 = 0
    while (type(encode1) == int):
        success, img1 = cap.read()
        imgGray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        img1 = cv2.flip(img1, 1)
        imgGray = cv2.flip(imgGray, 1)
        try:
            encode1 = face_encodings(img1)[0]
            if type(encode1) != int:
                break
        except Exception as e:
            print("", end="")
    l = []
    fl = open("data.txt", "r")
    v = fl.readlines()
    n = len(v)
    check = 0
    a = 0
    for i in range(0, n // 130):
        for j in range(a, a + 128):
            l.append(float(v[j]))
        a = a + 130
        results = compare_faces([l], encode1)
        results[0] = str(results[0])
        if (results[0] == "True"):
            print("working")
            name1 = v[j + 1]
            role1 = v[j + 2]
            check = 1
            break
        l.clear()
    fl.close()
    if(name1!=""):
        if(lang == 'en-ind'):
            speak("you are "+ name1)
        else:
            speak("आपका नाम "+name1 +" है")
    else:
        if(lang == 'en-ind'):
            speak("Sorry , I dont know you")
        else:
            speak("मैं आपको नहीं जानता")


    

def beginning():
    t1= threading.Thread(target=recognition)
    t2= threading.Thread(target=speak('Opening camera for face recognition. This might take few seconds.'))
    t1.start()
    t2.start()
    t1.join()
    wishMe()
    global lang,wait,new_name
    new_name=name.split()
    wait=0
    check=0
    lang='en-ind'   
    while(True):
        query=takeCommand(lang).lower()
        if(wait==0):
            if('wikipedia' in query or 'who is' in query or 'विकीपीडिया' in query or 'कौन है' in query):
                if(lang=='en-ind'):
                    speak("Searching Wikipedia")
                    query=query.replace("wikipedia","")
                    query=query.replace("who is","")
                    result = wikipedia.summary(query,sentences=2)
                    #wikipedia.set_lang('hi')
                    speak("According to wikipedia")
                else:
                    speak("विकिपीडिया में खोज रहे")
                    query=query.replace("विकिपीडिया","")
                    query=query.replace("कौन है ","")
                    wikipedia.set_lang('hi')
                    result = wikipedia.summary(query,sentences=2)
                    result = result[0:200]
                    speak("विकिपीडिया के अनुसार")
                print(result)
                speak(result)
            
            elif(("stop" in query or "pause" in query) and check==1):
                press_and_release('play/pause')
                check=0

            elif(("pause" in query or "break" in query or "sleep" in query or "timeout" in query or 'आराम' in query or 'सो जाओ' in query) and check==0):
                if(lang=="en-ind"):
                    speak("As you wish")
                else:
                    speak("जैसी आपकी इच्छा")
                wait=1
            

            elif('play' in query or 'song' in query or 'music' in query or 'गाना' in query or 'संगीत' in query ):
                if(role=='leader' or role=='leader\n'):
                    a = Translator(service_urls=['translate.googleapis.com'])
                    query = a.translate(text=query, dest='en', src='hi').text
                    print(query)
                    query=query.replace("play","")
                    query=query.replace("can you play","")
                    query=query.replace("song","")
                    query=query.replace("music","")
                    '''webbrowser.get(chrome_path).open('youtube.com/results?search_query='+query)'''
                    query_string = urllib.parse.urlencode({"search_query" : query})
                    html_content = urllib.request.urlopen("https://www.youtube.com.hk/results?"+query_string)
                    search_results = re.findall(r'url\"\:\"\/watch\?v\=(.*?(?=\"))', html_content.read().decode())
                    if search_results:
                        speak("Do you want me to play "+query)
                        permission=takeCommand(lang)
                        permission=permission.lower()
                        if('yes' in permission or "हां" in permission):
                            webbrowser.open_new("http://www.youtube.com/watch?v={}".format(search_results[0]))
                            check=1
                    else:
                        press_and_release('play/pause')
                        check=1
                else:
                    if(lang=="en-ind"):
                        speak('I am sorry . But you dont have the permission to play the songs')
                    else:
                        speak("मैं माफी चाहता हूं । लेकिन आपको गाने चलाने की अनुमति नहीं है")
            
            elif('news' in query or 'समाचार' in query or 'खबर' in query):
                if(lang=="hi-IN"):
                    bhasha='hi'
                else:
                    bhasha='en'
                if('india' in query or 'इंडिया' in query or'भारत' in query):
                    data = requests.get('https://gnews.io/api/v4/top-headlines?token=9060ccba0667f2e015587342f06d7df7&country=in&lang='+bhasha).text
                    
                elif('business' in query or 'व्यापार' in query):
                    data = requests.get('https://gnews.io/api/v4/top-headlines?token=9060ccba0667f2e015587342f06d7df7&topic=business&lang='+bhasha).text
                    
                elif('health' in query or 'स्वास्थ्य' in query):
                    data = requests.get('https://gnews.io/api/v4/top-headlines?token=9060ccba0667f2e015587342f06d7df7&topic=health&lang='+bhasha).text
                    
                elif('sports' in query or 'sports' in query or 'खेल' in query):
                    data = requests.get('https://gnews.io/api/v4/top-headlines?token=9060ccba0667f2e015587342f06d7df7&topic=sports&lang='+bhasha).text
                
                elif('technology' in query or 'तकनीकी' in query):
                    data = requests.get('https://gnews.io/api/v4/top-headlines?token=9060ccba0667f2e015587342f06d7df7&topic=technology&lang='+bhasha).text

                elif('entertainment' in query or 'मनोरंजन' in query):
                    data = requests.get('https://gnews.io/api/v4/top-headlines?token=9060ccba0667f2e015587342f06d7df7&topic=entertainment&lang='+bhasha).text
                else:
                    data = requests.get('https://gnews.io/api/v4/top-headlines?token=9060ccba0667f2e015587342f06d7df7&topic=world&lang='+bhasha).text
                data= json.loads(data)
                rand = random.randint(0,7)
                print(rand)
                j=rand
                while j<rand+2:
                    news=""
                    changer=""
                    counter=0
                    for i in (data['articles'][j]['description']):
                        if(lang=="hi-IN" and i==" " and changer!=""):
                            #print(changer)
                            a = Translator(service_urls=['translate.googleapis.com'])
                            changer = a.translate(text=changer, dest='hi', src='en').text
                            news= news + changer + " "
                            changer="" 
                        if(lang=="hi-IN" and ((i>='a' and i<='z')or(i>='A' and i<='Z'))):
                            changer=changer+i
                        else:
                            news = news + i
                        if(counter==2):
                            break
                        if(i=='।' or i=="."):
                            counter = counter+1
                    print("News:-",news)
                    speak(news)
                    j=j+1

            
            elif('youtube' in query or 'यूट्यूब' in query):
                webbrowser.get(chrome_path).open_new('youtube.com')

            elif ('who am i' in query or 'who i am' in query or 'मैं कौन हूं' in query or 'मैं कौन हू' in query):
                recog()

            elif('google' in query or 'search' in query or 'what is' in query or 'गूगल' in query or 'खोजो' in query or 'क्या है' in query):
                query = query.replace("google", "")
                query = query.replace("search", "")
                query = query.replace("what is", "")
                query = query.replace("गूगल", "")
                query = query.replace("खोजो", "")
                query = query.replace("the", "")
                query = query.replace(" ", "+")
                webbrowser.get(chrome_path).open_new('https://www.google.com/search?q=' + query)
            
            elif('time' in query or 'समय' in query or 'टाइम' in query):
                time()

            elif('goodbye' in query or 'bye' in query or 'exit' in query or 'close' in query or 'quit' in query or 'बंद' in query or 'बाय' in query):
                if(lang=='en-ind'):
                    speak("Goodbye "+new_name[0]+". I am going for a small nap. Do call, if u need me")
                else:
                    speak("नमसते । अगर आपको मेरी जरूरत हो तो कॉल करें")
                break

            elif('joke' in query or 'चुटकुला' in query or 'चुटकुले' in query):
                data=requests.get('https://v2.jokeapi.dev/joke/Dark,Pun,Spooky?blacklistFlags=nsfw').text
                data=json.loads(data)
                joke=""
                if(data['type']=='twopart'):
                    joke = joke + data['setup'] + data['delivery']
                else:
                    joke = data['joke']
                print(joke)
                speak(joke)

            elif ('write a note' in query or 'take a note' in query):
                file = open('note.txt', 'a')
                curr_time = QTime.currentTime()
                curr_day = str(datetime.date.today())
                curr_day = curr_day.split('-')

                labell_time = curr_time.toString("hh:mm:ss")
                file.write("date "+curr_day[2]+' '+curr_day[1] +' ' + curr_day[0] + "\n")
                file.write(labell_time + "\n")

                speak('what should i write sir?')
                while(True):
                    note = takeCommand(lang)
                    if('save file' in note or 'save note' in note ):
                        note = note.replace('save file', '')
                        note = note.replace('save note', '')
                        file.write(note + "\n")
                        speak("The note has been saved")
                        break
                    else:
                        file.write(note + "\n")

                file.close()
            
            elif('read' in query or 'note' in query):
                l=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
                fl = open("note.txt", "r")
                path='note.txt'
                os.startfile(path)
                v = fl.readlines()
                n = len(v)
                for i in range(0,n):
                    if('date' in v[i]):
                        num=int(v[i][9:11])
                        v[i] = v[i].replace(v[i][9:11],l[num-1])
                    speak(v[i])                         
            
            elif('where is' in query or 'map' in query or 'direction' in query or 'कहां है' in query or 'कहा है' in query):
                print(role)
                print(type(role))
                if(role=='leader' or role=='leader\n'):
                    query = query.replace("where is","")
                    query = query.replace("map","")
                    query = query.replace("कहां है","")
                    query = query.replace("कहा है","")
                    query = query.replace("direction","")
                    try:
                        g = geocoder.ip('me')
                        webbrowser.open_new('https://www.google.co.in/maps/dir/'+str(g.latlng[0]-.08)+','+str(g.latlng[1]-.2)+"/"+query)
                    except Exception as e:
                        speak("There is no such place by that name")
                else:
                    if(lang=="en-ind"):
                        speak("I am sorry . But you dont have the permission to access the maps")
                    else:
                        speak("मैं माफी चाहता हूं । लेकिन आपको नक्शों तक पहुंचने की अनुमति नहीं है")

            # elif('mail' in query or 'मेल' in query):
            #     try:
            #         if(lang=='en-ind'):
            #             speak("What should i say")
            #             content = takeCommand(lang)
            #             speak("To whom should i send")
            #             speak("Please write the mail id")
            #             to = input("Enter the mail here: ")
            #             speak("Do you want to send it to "+to)
            #             permission= takeCommand(lang)
            #             permission = permission.lower()
            #             if(permission=="yes"):
            #                 sendEmail(to,content)
            #                 speak("Email has been sent")
            #         else:
            #             speak("क्या लिखूं मैं")
            #             content = takeCommand(lang)
            #             speak("मुझे किसे भेजना है")
                        
            #             ##to = takeCommand(lang)
            #             to='sunil.khan@gmail.com'
            #             speak("क्या आप "+to+"भेजना चाहते हैं")
            #             permission= takeCommand(lang)
            #             permission = permission.lower()
            #             print(permission)
            #             if(permission=="हा" or permission=="हां"):
            #                 sendEmail(to,content)
            #                 speak("ईमेल भेजा जा चुका है")
            #     except Exception as e:
            #         if(lang=='en-ind'):
            #             speak("Sorry. The email was not sent")
            #         else:
            #             speak("माफ़ करना। ईमेल नहीं भेजा गया हैं")

            elif('hindi' in query):
                lang='hi-IN'
                val=1
                engine.setProperty('voice',voices[val].id)
                speak('अब भाषा हिंदी में है')

            elif('अंग्रेजी' in query or 'इंग्लिश' in query):
                lang='en-ind'
                val=3
                engine.setProperty('voice',voices[val].id)
                speak('now the language is in english')

            elif('your name' in query or 'who are you' in query or 'तुम कोन हो' in query or 'तुम्हारा नाम'in query):
                intro()
                
            elif('weather' in query or 'temperature' in query or 'climate' in query or 'मौसम' in query or 'तापमान' in query):
                g = geocoder.ip('me')
                url = "https://api.weatherbit.io/v2.0/forecast/daily?&lat=" +str(g.latlng[0]-.08)+ "&lon="+str(g.latlng[1]-.2) +"&key=c8a42097ee0148de82b6fe4c5e85b6b5"
                response = requests.get(url).text
                x= json.loads(response)
                city_name  = str(x["city_name"])
                temp = str(x["data"][0]["high_temp"])
                desc = str(x["data"][0]["weather"]["description"])
                print("It is " + temp + " degree in " + city_name + " and the weather is "+ desc)
                if(lang=='en-ind'):
                    speak("It is " + temp + " degree in " + city_name + " and the weather is "+ desc)
                else:
                    d={'Thunderstorm with light rain':'हल्की बारिश के साथ आंधी','Thunderstorm with rain':'बारिश के साथ तूफान','Thunderstorm with heavy rain':'भारी बारिश के साथ तूफान',	'Thunderstorm with light drizzle':'हल्की बूंदा बांदी के साथ तूफान',	'Thunderstorm with drizzle':'बूंदा बांदी के साथ तूफान',	'Thunderstorm with heavy drizzle':'भारी बूंदा बांदी के साथ तूफान',	'Thunderstorm with Hail':'गरज के साथ छींटे','Light Drizzle':'हल्की बूंदाबांदी',	'Drizzle':'बूंदा बांदी','Heavy Drizzle':'बूंदा बांदी',	'Light Rain':'हलकी बारिश',	'Moderate Rain':'औसत दर्जे की वर्षा',	'Heavy Rain':'भारी वर्षा','Freezing rain':'हिमीकरण बारिश','Light shower rain':'हल्की बौछार बारिश','Shower rain':'बौछार बारिश','Heavy shower rain':'भारी बारिश',	'Light snow':'हलकी बर्फ','Snow':'बर्फ',	'Heavy Snow':'भारी बर्फ',	'Mix snow/rain':'बर्फ',	'Sleet':'ओले के साथ वर्षा',	'Heavy sleet':'भारी स्लीट',	'Snow shower':'स्नो शॉवर',	'Heavy snow shower':'भारी बर्फबारी',	'Flurries':'आंधी',	'Mist':'कोहरा',	'Smoke':'धुआं',	'Haze':'धुंध',	'Sand/dust':'धूल',	'Fog':'कोहरा',	'Freezing Fog':'अत्यधिक ठंडा कोहरा',	'Clear sky':'साफ आसमान',	'Few clouds':'थोडे बादल',	'Scattered clouds':'बिखरे हुए बादल',	'Broken clouds':'बादल','Overcast clouds':'बादल छाए',	'Unknown Precipitation':'अज्ञात वर्षा',	'Thunderstorm with light rain':'हल्की बारिश के साथ आंधी',	'Thunderstorm with rain':'बारिश के साथ तूफान',	'Thunderstorm with heavy rain':'भारी बारिश के साथ तूफान',	'Thunderstorm with light drizzle':'हल्की बूंदा बांदी के साथ तूफान',	'Thunderstorm with drizzle':'बूंदा बांदी के साथ तूफान',	'Thunderstorm with heavy drizzle':'भारी बूंदा बांदी के साथ तूफान',	'Thunderstorm with Hail':'गरज के साथ छींटे',	'Light Drizzle':'हल्की बूंदाबांदी',	'Drizzle':'बूंदा बांदी',	'Heavy Drizzle':'बूंदा बांदी',	'Light Rain':'हलकी बारिश',	'Moderate Rain':'औसत दर्जे की वर्षा',	'Heavy Rain':'भारी वर्षा',	'Freezing rain':'हिमीकरण बारिश',	'Light shower rain':'हल्की बौछार बारिश','Shower rain':'बौछार बारिश',	'Heavy shower rain':'भारी बारिश',	'Light snow':'हलकी बर्फ',	'Snow':'बर्फ',	'Heavy Snow':'भारी बर्फ',	'Mix snow/rain':'बर्फ',	'Sleet':'ओले के साथ वर्षा',	'Heavy sleet':'भारी स्लीट',	'Snow shower':'स्नो शॉवर','Heavy snow shower':'भारी बर्फबारी',	'Flurries':'आंधी',	'Mist':'कोहरा',	'Smoke':'धुआं',	'Haze':'धुंध',	'Sand/dust':'धूल','Fog':'कोहरा',	'Freezing Fog':'अत्यधिक ठंडा कोहरा',	'Clear sky':'साफ आसमान',	'Few clouds':'थोडे बादल','Scattered clouds':'बिखरे हुए बादल',	'Broken clouds':'बादल','Scattered clouds':'बिखरे हुए बादल','Broken clouds':'बादल',	'Overcast clouds':'बादल छाए','Unknown Precipitation':'अज्ञात वर्षा'}
                    translator = Translator(service_urls=['translate.googleapis.com'])
                    l=['शून्य','एक ',	'दो  ',	'तीन ',	'चार ',	'पांच ',	'छह ',	'सात ',	'आठ ',	'नौ ',	'दस',	'ग्यारह ',	'बारह',
                            'तेरह ',	'चोदह',	'पंद्रह ',	'सोलह ',	'सत्त्रह ',	'अट्ठारह ',	'उन्नीस ',	'बीस ',	'इक्कीस',	'बाइस ',	'तेईस ',
                                'चौबीस ',	'पच्चीस ',	'छब्बीस ',	'सत्ताइस ',	'अट्ठाइस ',	'उन्तीस ',	'तीस ',	'इकतीस',	'बत्तीस ',	'तैतीस ',
                                    'चौतीस',	'पैतीस ',	'छत्तीस',	'सैतीस ',	'अड़तीस',	'उन्तालीस ',	'चालीस ',	'इकतालीस ',	'बयालीस',
                                        'तिरतालिस',	'चौवालीस ',	'पैतालीस ',	'छयालीस ',	'सैतालिस ',	'अड़तालीस ',	'उनचास ',	'पचास ',
                                            'इक्क्यावन',	'बावन ',	'तिरपन',	'चौवन ',	'पचपन ',	'छप्पन ',	'सत्तावन ',	'अट्ठावन ',
                                                'उनसठ ',	'साठ ',]
                    temp = temp.split('.')
                    city_name = translator.translate(text=city_name, dest='hi', src='en').text
                    print("अभी "+city_name+" में तापमान "+l[int(temp[0])]+" दशमलव "+l[int(temp[1])]+" है और " + d[desc]+" की संभावना है")
                    speak("अभी "+city_name+" में तापमान "+l[int(temp[0])]+" दशमलव "+l[int(temp[1])]+" है और " + d[desc]+" की संभावना है")

            elif('is love' in query or 'प्रेम' in query or 'प्यार' in query):
                if(lang=='en-ind'):
                    speak("It is 7th sense that destroy all other senses")
                else:
                    speak("प्यार धोखा है")

            else:
                if(lang=='en-ind' and query!="none"):
                    print(query)
                    speak("Can you say that again")
                else:
                    speak("क्या आप फिर से कह सकते हैं")
        
        elif(("java" in query or 'जावा' in query) and  wait==1):
            if(lang=="en-ind"):
                speak("I am back again")
            else:
                speak("मैं वापस आ गया हूँ")
            wait=0
        
        


class MainThread(QThread):

    def __init__(self): 

        super(MainThread,self).__init__()

    def run(self):
        self.Task_Gui()
    
    def Task_Gui(self):
        beginning()


startFunctions = MainThread() 

class Gui_Start(QMainWindow):

    def __init__(self):

        super().__init__()

        self.java_ui = Ui_MainWindow()
        
        self.java_ui.setupUi(self)

        self.java_ui.start.clicked.connect(self.startFunc)

        self.java_ui.stop.clicked.connect(self.close)

    def startFunc(self):

        self.java_ui.movies = QtGui.QMovie("animation.gif")

        self.java_ui.gif1.setMovie(self.java_ui.movies)

        self.java_ui.movies.start()



        self.java_ui.movies_2 = QtGui.QMovie("sounds.gif")

        self.java_ui.label.setMovie(self.java_ui.movies_2)

        self.java_ui.movies_2.start()


        timer = QTimer(self)

        timer.timeout.connect(self.showtime)

        timer.start(1000)

        startFunctions.start()

    def showtime(self):
        
        current_time = QTime.currentTime()
        day=str(datetime.date.today())

        label_time = current_time.toString("hh:mm:ss")

        labbel = " Time - " + label_time + "\n Date - " + day

        self.java_ui.textBrowser.setText(labbel)

Gui_App = QApplication(sys.argv)

Gui_java = Gui_Start()

Gui_java.show()

exit(Gui_App.exec_())




