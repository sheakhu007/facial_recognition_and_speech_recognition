import cv2
import face_recognition
import os

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
		print("Hello "+person_names[index])
	else:
		#print(index)
		pass
	index+=1
		
	

#if results is True in results_list.any():
#    print("Me me!")
#else:
#    print("NOT NOT me!")