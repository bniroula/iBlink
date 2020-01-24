from scipy.spatial import distance
import imutils
import cv2
from iBlink_Dictionary import MorseDictionary
from collections import deque
import numpy as np
import dlib
import winsound
from imutils import face_utils
import pyautogui

class DetectEyes():

   
    def __init__(self):
        self.startTime = 0
        self.openTime = 0

        self.Message = ''
        self.finalString = []
        global L
        self.codeArr = []

        self.closed = False
        self.timer = 0
        self.final = ''
        self.pts = deque(maxlen=512)
        self.thresh = 0.25
       
        self.detect = dlib.get_frontal_face_detector()
        self.getFace = dlib.shape_predictor("Face_Model.dat")  

        (self.leftStart, self.leftEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        (self.rightStart, self.rightEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    def eye_aspect_ratio(self,eye):
        A = distance.euclidean(eye[1], eye[5])
        B = distance.euclidean(eye[2], eye[4])
        C = distance.euclidean(eye[0], eye[3])
        self.ear = (A + B) / (2.0 * C)
        return self.ear


    def calculate(self,frame):

        decoded = cv2.imdecode(np.frombuffer(frame, np.uint8), -1)
        frame = imutils.resize(decoded, width=640)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        subjects = self.detect(gray, 0)
        for subject in subjects:
            shape = self.getFace(gray, subject)
            shape = face_utils.shape_to_np(shape)  # converting to NumPy Array
            leftEye = shape[self.leftStart:self.leftEnd]
            rightEye = shape[self.rightStart:self.rightEnd]
            leftEAR = self.eye_aspect_ratio(leftEye)
            rightEAR = self.eye_aspect_ratio(rightEye)
            ear = (leftEAR + rightEAR) / 2.0
            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
            if ear < self.thresh:  # closed eyes
                self.startTime += 1
                self.pts.appendleft(self.startTime)
                self.openTime = 0
            else:
                self.openTime += 1
                self.startTime = 0
                self.pts.appendleft(self.startTime)

            for i in range(1, len(self.pts)):
                if self.pts[i] > self.pts[i - 1]:
                    
                    if self.pts[i] > 9 and self.pts[i] < 15:
                   
                        self.codeArr.append("-")
                        self.pts = deque(maxlen=512)
                        winsound.Beep(1500, 250)
                        break
                    elif self.pts[i] > 5 and self.pts[i] < 9:
                       
                       
                        self.codeArr.append(".")
                        winsound.Beep(2500, 250)
                        self.pts = deque(maxlen=512)
                        break

                    elif self.pts[i] > 17:
                        if(len(self.codeArr)!= 0):
                          
                           
                            winsound.Beep(3500, 250)
                            self.codeArr.pop()
                            self.pts = deque(maxlen=512)
                        break

        if (self.codeArr != []):
           
            print(self.codeArr)
        if self.openTime > 17:
            if (self.codeArr != []):
              
                print(self.codeArr)
            self.Message = MorseDictionary(''.join(self.codeArr))

        

            if self.Message != None:

                #pyautogui.click(x=378, y=60)
                
                if(self.Message == 'backspace'):
                    self.final = self.final[:-1]
                    self.Message = self.Message[:-1]
                    self.finalString.pop()
                    pyautogui.press('backspace')
                elif(self.Message == 'clear'):
                    self.final = ''
                    self.Message = ''
                    self.finalString.clear()
                elif(self.Message=='enter'):
                    pyautogui.press('return')
                else:
                    self.finalString.append(self.Message)
                    self.final = ''.join(self.finalString)
                    pyautogui.typewrite(self.Message)

            if self.Message == None:
                self.codeArr = []
            self.codeArr = []
        
        ret, png = cv2.imencode('.png', frame)
        return png, self.codeArr


