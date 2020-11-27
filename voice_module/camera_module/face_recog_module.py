import cv2
import face_recognition



#camera = cv2.VideoCapture(0)
captureDevice = cv2.VideoCapture(0, cv2.CAP_DSHOW) #captureDevice = camera
for i in range(1):
    
    return_value, image = captureDevice.read()
    file = 'live_pic'+'.jpg'
    cv2.imwrite(file, image)
del(captureDevice)



picture_of_me = face_recognition.load_image_file("me.jpg")
my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]

# my_face_encoding now contains a universal 'encoding' of my facial features that can be compared to any other picture of a face!

unknown_picture = face_recognition.load_image_file(file)
unknown_picture2 = face_recognition.load_image_file("unknown.jpeg")

try:
    unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]
except :
     unknown_face_encoding = face_recognition.face_encodings(unknown_picture2)[0]
# Now we can see the two face encodings are of the same person with `compare_faces`!

results = face_recognition.compare_faces([my_face_encoding], unknown_face_encoding)

if results[0] == True:
    print("It's a picture of me!")
else:
    print("It's not a picture of me!")



