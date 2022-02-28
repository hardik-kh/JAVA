from os import name
import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import urllib.request
import urllib.parse
import re
import smtplib
from translate import Translator
from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from javaUI import Ui_MainWindow
import sys
from keyboard import press_and_release
import cv2
import numpy as np
from face_recognition import face_encodings,compare_faces


engine = pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
global val
val=3
engine.setProperty('voice',voices[val].id)
print(voices)
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
        translator= Translator(from_lang="hindi",to_lang="english")
        content = translator.translate(content)
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
    if(hour>12):
        hour=str(hour-12)
        if(lang=="en-ind"):
            speak("It is "+hour+min+"pm"+new_name[0])
        else:

            print("अभी"+hour+min+"pm हो रहे हैं")
            speak(new_name[0])
            speak("अभी")
            speak(hour+min)
            speak("बज रहे हैं")
    else:
        hour=str(hour)
        if(lang=="en-ind"):
            speak("It is "+hour+min+"am"+new_name[0])
        else:
            speak(new_name[0])
            speak("अभी")
            speak(hour+min)
            speak("बज रहे हैं")

def intro():
    if(lang=='en-ind'):
        speak("My name is java. Short for just awesome voice assistant. I was created by hardik khandelwal to take commands through voice")
    else:
        speak("मेरा नाम जावा है। मुझे हार्दिक खंडेलवाल ने आवाज के जरिए कमांड लेने के लिए बनाया है")

def recognition():
    global name
    query=""
    frameWidth = 640
    frameHeight = 480
    cap = cv2.VideoCapture(0)
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
    for i in range(0,n//129):  
        for j in range(a,a+128):
            l.append(float(v[j]))
        a=a+129
        results = compare_faces([l],encode1)
        results[0] = str(results[0])
        if(results[0]=="True"):
            print("working")
            name=v[j+1]
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
        while(query==""):
            query = takeCommand('en-ind')
        query= query.lower()
        query = query.replace('my','')
        query = query.replace('name','')
        query = query.replace('is','')
        name = query
        fl.write(name)
        fl.close()


    

def beginning():
    speak("Opening camera for face recognition. This might take few seconds")

    recognition()
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
                    wikipedia.set_lang('hi')
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
                query=query.replace("play","")
                query=query.replace("song","")
                query=query.replace("music","")
                query=query.replace("गाना","")
                query=query.replace("संगीत","")
                '''webbrowser.get(chrome_path).open('youtube.com/results?search_query='+query)'''
                query_string = urllib.parse.urlencode({"search_query" : query})
                html_content = urllib.request.urlopen("https://www.youtube.com.hk/results?"+query_string)
                search_results = re.findall(r'url\"\:\"\/watch\?v\=(.*?(?=\"))', html_content.read().decode())
                if search_results:
                    speak("Do you want me to play "+query)
                    permission=takeCommand(lang)
                    permission=permission.lower()
                    if(permission=='yes' or permission=="हां"):
                        webbrowser.open_new("http://www.youtube.com/watch?v={}".format(search_results[0]))
                        check=1
                else:
                    press_and_release('play/pause')
                    check=1
            
            elif('youtube' in query or 'यूट्यूब' in query):
                webbrowser.get(chrome_path).open_new('youtube.com')

            elif('google' in query or 'गूगल' in query):
                webbrowser.get(chrome_path).open_new('google.com')
            
            elif('time' in query or 'समय' in query or 'टाइम' in query):
                time()

            elif('goodbye' in query or 'bye' in query or 'exit' in query or 'close' in query or 'quit' in query or 'बंद' in query or 'बाय' in query):
                if(lang=='en-ind'):
                    speak("Goodbye "+new_name[0]+". I am going for a small nap. Do call, if u need me")
                else:
                    speak("नमसते । अगर आपको मेरी जरूरत हो तो कॉल करें")
                break

            elif('mail' in query or 'मेल' in query):
                try:
                    if(lang=='en-ind'):
                        speak("What should i say")
                        content = takeCommand(lang)
                        speak("To whom should i send")
                        speak("Please tell the mail id letter by letter")
                        to = takeCommand(lang)
                        to=to.lower()
                        to=to.replace('at','@')
                        to=to.replace(' ','')
                        speak("Do you want to send it to"+to)
                        permission= takeCommand(lang)
                        permission = permission.lower()
                        if(permission=="yes"):
                            sendEmail(to,content)
                            speak("Email has been sent")
                    else:
                        speak("क्या लिखूं मैं")
                        content = takeCommand(lang)
                        speak("मुझे किसे भेजना है")
                        
                        ##to = takeCommand(lang)
                        to='sunil.khan@gmail.com'
                        speak("क्या आप "+to+"भेजना चाहते हैं")
                        permission= takeCommand(lang)
                        permission = permission.lower()
                        print(permission)
                        if(permission=="हा" or permission=="हां"):
                            sendEmail(to,content)
                            speak("ईमेल भेजा जा चुका है")
                except Exception as e:
                    if(lang=='en-ind'):
                        speak("Sorry. The email was not sent")
                    else:
                        speak("माफ़ करना। ईमेल नहीं भेजा गया हैं")

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




