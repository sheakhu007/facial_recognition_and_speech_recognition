import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import time
import subprocess
from ecapture import ecapture as ec
import wolframalpha
import json
import requests
import cv2
import face_recognition


print('LOADING MINERVA ACME ROBO')

engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
engine.setProperty('voice','voices[0].id')


def speak(text):
    engine.say(text)
    engine.runAndWait()

def wishMe():
    hour=datetime.datetime.now().hour
    if hour>=0 and hour<12:
        speak("Good Morning")
        print("Good Morning")
    elif hour>=12 and hour<18:
        speak("Good Afternoon")
        print("Good Afternoon")
    else:
        speak("Good Evening")
        print("Good Evening")

def takeCommand():
    r=sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        audio=r.listen(source)

        try:
            statement=r.recognize_google(audio,language='en-in')
            print(f"{statement}\n")

        except Exception as e:
            #speak("please say that again")
            return "None"
        return statement

speak("MINERVA ACME PRESENTS ROBO")
images = []                         #Empty list to save all IMAGES of known persons
person_names = []                   # Empty list to save all NAMES of known persons
path = "known_persons"
image_list = os.listdir(path)       # file names of all the known images
#print(image_list)

for img_names in image_list:       #fetching all the images from known_person folder
    current_image = cv2.imread(f'{path}/{img_names}')
    images.append(current_image)   #adding image files
    person_names.append(os.path.splitext(img_names)[0]) #Seprating Person's name from the image file name
#print(person_names)



# Function to Genrate known faces encodings
def known_persons_encodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList
encodeListknown = known_persons_encodings(images)
print("Encoding Complete")

# Clicking image from webcam
captureDevice = cv2.VideoCapture(0, cv2.CAP_DSHOW) #captureDevice = camera
for i in range(1):

    return_value, image = captureDevice.read()
    file = 'live_pic'+'.jpg'   #file_name
    cv2.imwrite(file, image)
del(captureDevice)

#speak('picture has been taken')
unknown_picture = face_recognition.load_image_file("live_pic.jpg")
unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]
#unknown_face_loc = face_recognition.face_locations(file)
results_list = []
for each in encodeListknown:
    results = face_recognition.compare_faces([each], unknown_face_encoding)
    results_list.append(results)

index = 0
for j in results_list:
    #print(j)
    if j[0] == True:
        speak("Hello " +person_names[index])
        print("Hello "+person_names[index])
    else:
        #print(index)
        pass
    index+=1
speak("I AM ROBO")
wishMe()


if __name__=='__main__':


    while True:
        #speak(" how can I help you?")
        statement = takeCommand().lower()
        speak(" how can I help you?")
        if statement=='hello robo':
            continue

        elif "good bye" in statement or "ok bye" in statement or "stop" in statement:
            speak('')
            speak('Nice to meet you,Thanks for your time to talk with me ')
            break

        elif "picture" in statement:
            images = []                         #Empty list to save all IMAGES of known persons
            person_names = []                   # Empty list to save all NAMES of known persons
            path = "known_persons"
            image_list = os.listdir(path)       # file names of all the known images
			#print(image_list)

            for img_names in image_list:       #fetching all the images from known_person folder
                current_image = cv2.imread(f'{path}/{img_names}')
                images.append(current_image)   #adding image files
                person_names.append(os.path.splitext(img_names)[0]) #Seprating Person's name from the image file name
			#print(person_names)
			# Function to Genrate known faces encodings
            def known_persons_encodings(images):
                encodeList = []
                for img in images:
                    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
                    encode = face_recognition.face_encodings(img)[0]
                    encodeList.append(encode)
                return encodeList
            encodeListknown = known_persons_encodings(images)
            print("Encoding Complete")

			# Clicking image from webcam
            captureDevice = cv2.VideoCapture(0, cv2.CAP_DSHOW) #captureDevice = camera
            for i in range(1):

                return_value, image = captureDevice.read()
                file = 'live_pic'+'.jpg'   #file_name
                cv2.imwrite(file, image)
            del(captureDevice)

            speak('picture has been taken')
            unknown_picture = face_recognition.load_image_file("live_pic.jpg")
            unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]
			#unknown_face_loc = face_recognition.face_locations(file)
            results_list = []
            for each in encodeListknown:
                results = face_recognition.compare_faces([each], unknown_face_encoding)
                results_list.append(results)

            index = 0
            for j in results_list:
				#print(j)
                if j[0] == True:
                    speak("Hello " +person_names[index])
                    print("Hello "+person_names[index])
                else:
					#print(index)
                    pass
                index+=1

        elif 'wikipedia' in statement:
            speak('Searching Wikipedia...')
            statement =statement.replace("wikipedia", "")
            results = wikipedia.summary(statement, sentences=3)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif "weather" in statement:
            api_key="8ef61edcf1c576d65d836254e11ea420"
            base_url="https://api.openweathermap.org/data/2.5/weather?"
            speak("whats the city name")
            city_name=takeCommand()
            complete_url=base_url+"appid="+api_key+"&q="+city_name
            response = requests.get(complete_url)
            x=response.json()
            if x["cod"]!="404":
                y=x["main"]
                current_temperature = y["temp"]
                current_humidiy = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                speak(" Temperature in kelvin unit is " +
                      str(current_temperature) +
                      "\n humidity in percentage is " +
                      str(current_humidiy) +
                      "\n description  " +
                      str(weather_description))
                print(" Temperature in kelvin unit = " +
                      str(current_temperature) +
                      "\n humidity (in percentage) = " +
                      str(current_humidiy) +
                      "\n description = " +
                      str(weather_description))

            else:
                speak(" City Not Found ")



        elif 'time' in statement:
            strTime=datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"the time is {strTime}")

        elif 'who are you' in statement or 'what can you do' in statement:
            speak('I am Robo version 1 point O your robotic friend. I am programmed to perform minor tasks like'
                  'take a photo,predict time,search wikipedia,predict weather'
                  'in different cities , get top headline news from times of india and you can ask me computational or geographical questions too!')


        elif "who made you" in statement or "who created you" in statement or "who discovered you" in statement:
            speak("I am Devloped by the Devloper's Team of Minerva Acme")

        elif "camera" in statement or "take a photo" in statement:
            ec.capture(0,"robo camera","img.jpg")

        elif 'ask' in statement:
            speak('I can answer to computational and geographical questions and what question do you want to ask now')
            question=takeCommand()
            app_id="R2K75H-7ELALHR35X"
            client = wolframalpha.Client('R2K75H-7ELALHR35X')
            res = client.query(question)
            answer = next(res.results).text
            speak(answer)
            print(answer)



time.sleep(3)
