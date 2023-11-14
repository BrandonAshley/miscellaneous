import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import os
from googlesearch import search
import randfacts

def checkWord(s):
    if ("task manager" in s):
        return "taskmgr"
    elif ('calendar'in s):
        return "outlookcal:"
    elif ('mail' in s):
        return "outlookmail:"
    elif ('settings' in s):
        return 'ms-settings:'
    elif ('windows defender'in s):
        return 'windowsdefender:'
    elif ('file explorer' in s):
        return 'explorer'
    elif (('netflix' or 'twitch'or 'origin'or 'discord'or 'calculator')in s):
        return s+':'
    else:
        return s

def Calc_results(s):    
    if ('+' in s):
        mid=s.find('+')
        f=s[0:mid-1].strip()
        f=int(f)
        l=s[mid+1:len(s)].strip()
        l=int(l) 
        res=f+l
        return (res)

    elif('-' in s):
        mid=s.find('-')
        f=s[0:mid-1].strip()
        f=int(f)
        l=s[mid+1:len(s)].strip()
        l=int(l) 
        res=f-l
        return (res)
    
    elif ('*' in s):
        mid=s.find('*')
        f=s[0:mid-1].strip()
        f=int(f)
        l=s[mid+1:len(s)].strip()
        l=int(l) 
        res=f*l
        return (res)
    
    elif ('/'  in s):
        mid=s.find('/')
        f=s[0:mid-1].strip()
        f=int(f)
        l=s[mid+1:len(s)].strip()
        l=int(l) 
        res=f/l
        return (res)
    
    
listener= sr.Recognizer()
engine = pyttsx3.init()
voices=engine.getProperty('voices')
engine.setProperty('voices',voices[0].id)

text="Hi I am Jarvis how can I help you?"

def talk(text):
    engine.say(text)
    engine.runAndWait()



def takeCommand():
    try:
        with sr.Microphone() as source:
            print("listening")
            voice=listener.listen(source)
            command= listener.recognize_google(voice)
            command= command.lower()
            if 'jarvis' in command:
                command=command.replace('jarvis','')
                talk(command)
                print(command)
    except:
        print("fail")
        pass
    return command


def run_jarvis():
    talk(text)
    command=takeCommand()
    command.strip()
    
    if 'play' in command:
        song= command.replace('play','')
        talk('Playing'+song)
        pywhatkit.playonyt(song)
        
    elif 'what is the time' in command:
        time = datetime.datetime.now().strftime('%H:%M')
        talk('the time is '+time)
        
    elif 'what is the date' in command:
        date=datetime.datetime.now().strftime('%Y-%B-%d')
        talk('the date is '+date)
        
    elif 'wikipedia' in command:
        statement=command.replace("wikipedia",'')
        info=wikipedia.summary(statement, 2)
        talk(info)
        
    elif 'open' in command:
        statement= command.replace("open",'')
        new_statement=checkWord(statement);
        try:
            os.system("start "+new_statement)
            talk("Opening "+ statement)
        except :
            talk("Failed to open"+ statement+"Please try again")
             
    elif 'search' in command:
        statement=command.replace('search','')
        print(statement)
        for j in search(statement,num=1,lang="en"): 
            site=j
        print(site)
        os.system("start "+ site)
        
    elif ('hello' or 'hi') in command:
        talk("Hallo i can hear you")
        
    elif 'tell me a fact' in command:
        facts=randfacts.getFact()
        print(facts)
        talk(facts)
    elif 'calculate' in command:
        s=command.replace('calculate','')
        results=Calc_results(s)
        talk(results)
        
        
        
        
while True:
    run_jarvis()
























