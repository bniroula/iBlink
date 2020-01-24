import cv2, time

class Webcam():
    # Constructor...
    def __init__(self):
        width = 640  
        height = 480  
        FramePerSec = 60.0  

        resolution = (width, height)  
        self.cap = cv2.VideoCapture(0)  
       
        time.sleep(1)
        
        self.ret, self.frame = self.cap.read()


    # Frame generation for Browser streaming
    def get_frame(self):
        success, image = self.cap.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()


    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()
        
     
        return ()

