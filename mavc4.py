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
import math
from sklearn import neighbors
import os.path
import pickle
from PIL import Image, ImageDraw
from face_recognition.face_recognition_cli import image_files_in_folder


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
predicted_name = []
#classifier = train("known_persons_images_folders", model_save_path="trained_knn_model.clf", n_neighbors=2)
#print("Training complete!")
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
def train(train_dir, model_save_path=None, n_neighbors=None, knn_algo='ball_tree', verbose=False):
    X = []
    y = []
    for class_dir in os.listdir(train_dir):
        if not os.path.isdir(os.path.join(train_dir, class_dir)):
            continue
        for img_path in image_files_in_folder(os.path.join(train_dir, class_dir)):
            image = face_recognition.load_image_file(img_path)
            face_bounding_boxes = face_recognition.face_locations(image)

            if len(face_bounding_boxes) != 1:
                if verbose:
                    print("Image {} not suitable for training: {}".format(img_path, "Didn't find a face" if len(face_bounding_boxes) < 1 else "Found more than one face"))
            else:
                X.append(face_recognition.face_encodings(image, known_face_locations=face_bounding_boxes)[0])
                y.append(class_dir)
    if n_neighbors is None:
        n_neighbors = int(round(math.sqrt(len(X))))
        if verbose:
            print("Chose n_neighbors automatically:", n_neighbors)
    knn_clf = neighbors.KNeighborsClassifier(n_neighbors=n_neighbors, algorithm=knn_algo, weights='distance')
    knn_clf.fit(X, y)

    # Save the trained KNN classifier
    if model_save_path is not None:
        with open(model_save_path, 'wb') as f:
            pickle.dump(knn_clf, f)

    return knn_clf


def predict(X_img_path, knn_clf=None, model_path=None, distance_threshold=0.6):
    if not os.path.isfile(X_img_path) or os.path.splitext(X_img_path)[1][1:] not in ALLOWED_EXTENSIONS:
        raise Exception("Invalid image path: {}".format(X_img_path))

    if knn_clf is None and model_path is None:
        raise Exception("Must supply knn classifier either thourgh knn_clf or model_path")
    if knn_clf is None:
        with open(model_path, 'rb') as f:
            knn_clf = pickle.load(f)
    X_img = face_recognition.load_image_file(X_img_path)
    X_face_locations = face_recognition.face_locations(X_img)
    if len(X_face_locations) == 0:
        return []
    faces_encodings = face_recognition.face_encodings(X_img, known_face_locations=X_face_locations)
    closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)
    are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(X_face_locations))]
    return [(pred, loc) if rec else ("unknown", loc) for pred, loc, rec in zip(knn_clf.predict(faces_encodings), X_face_locations, are_matches)]


def show_prediction_labels_on_image(img_path, predictions):
    pil_image = Image.open(img_path).convert("RGB")
    draw = ImageDraw.Draw(pil_image)
    for name, (top, right, bottom, left) in predictions:
        draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))
        name = name.encode("UTF-8")
        text_width, text_height = draw.textsize(name)
        draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
        draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))
    del draw
    pil_image.show()


speak("MINERVA ACME PRESENTS ROBO")
'''images = []                         #Empty list to save all IMAGES of known persons
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
    index+=1'''
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

        elif "recognise me" in statement:
            print("Clicking Image Smile Please")
            count = 0
            for i in range(5):
                camera = cv2.VideoCapture(0)
                return_value, image = camera.read()
                cv2.imwrite(r"C:\Users\Abhi\Desktop\MinervaAcme\test\frame%d.jpg" % count, image)
                count+=1
                del(camera)
            print("Training KNN classifier...")
            classifier = train("known_persons_images_folders", model_save_path="trained_knn_model.clf", n_neighbors=2)
            print("Training complete!")
            for image_file in os.listdir("test"):
                full_file_path = os.path.join("test", image_file)
                print("Looking for faces in {}".format(image_file))
                predictions = predict(full_file_path, model_path="trained_knn_model.clf")
                if predictions == []:
                    pass
                else:
                    for items in predictions:
                        tup = items[0]
                        predicted_name.append(tup)
                    predicted_name  = list(dict.fromkeys(predicted_name))
            for names in predicted_name:
                if names == "unknown":
                    pass
                else:
                    print("Hello ",names)
            '''images = []                         #Empty list to save all IMAGES of known persons
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
                index+=1'''

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
