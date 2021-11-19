import cv2
import time
import datetime
import shutil
import os

camera = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
full_body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_fullbody.xml")

detection = False
detection_stopped_time = None
timer_started = False
SECONDS_TO_RECORD_AFTER_DETECTION = 5

frame_size = (int(camera.get(3)), int(camera.get(4)))
fourcc = cv2.VideoWriter_fourcc(*"mp4v")

def transfer_files_to_recordings_folder():
    files = os.listdir()
    for file in files:
        if file.endswith(".mp4"):
            shutil.move(file,"Videos")
while True:
    _,frame = camera.read()

    gray_img = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_img, 1.3, 5)
    bodies = full_body_cascade.detectMultiScale(gray_img, 1.3, 5)

    if len(faces) + len(bodies) > 0:
        if detection:
            # We are dectecting a person
            timer_started = False
        else:
            # If no person had been detected, but now has been
            detection = True
            current_time = datetime.datetime.now().strftime("%d-%m-%Y-%I-%M-%S")
            out = cv2.VideoWriter(f"{current_time}.mp4",fourcc,20,frame_size)

            print("Started Recording!")

    # Check if we were recording
    elif detection: 
        # If timer has started
        if timer_started:
            if time.time() - detection_stopped_time >= SECONDS_TO_RECORD_AFTER_DETECTION:
                detection = False
                timer_started = False
                out.release()

                print("Stoped Recording!")

        else:
            timer_started = True
            detection_stopped_time = time.time()

    if detection:
        out.write(frame)
    
    for (x, y, width, height) in faces:
        cv2.rectangle(frame, (x,y),(x+width,y+height),(255,0,0),3)

    if cv2.waitKey(1) == ord('q'):
        break

    cv2.imshow("Camera",frame)

out.release()
camera.release()
cv2.destroyAllWindows()
transfer_files_to_recordings_folder()
os.system("git add .")
os.system(f'git commit -a -m "Added Video {current_time}.mp4" ')
os.system("git push")
