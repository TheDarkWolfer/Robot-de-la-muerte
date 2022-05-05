from datetime import datetime
import keyboard, numpy, cv2, time, pandas
from cv2 import aruco as aruco
import numpy as np
import PIL
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
class image_processor:
 
    """A class used to process images through opencv-python, mainly for our end-of-the-year
    project in our STI2D class. The class is fairly easy to use, as you can switch feeds by changing the `key`
    attribute with `image_processor.key = [insert wanted frame]`. Good luck using it, if it ever fucks up just
    pretend it's a normal, wanted occurance, because this took too long to code, and too long to implement
    as Object-Oriented, and I might commit war crimes if I ever have to rewrite this.
    Oh and also, unless explicitely stated by me, you have to give credits would you ever use this code in yours,
    and if you don't I'll send the boogeyman after you. You also agree to defend my honor as well as my friends and family
    in time of need, and to forfeit all mortal possessions to me if I ever summon you to do so.
    If you're not ok with this, don't use my hellspawn- I mean, my class.
    
    -TheDarkWolfer"""


    def __init__(self):


        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

        self.window_types = ["Non-filtered feed","Movement detection feed","Human detection feed","Red feed","Green feed","Blue feed","Gray feed","Gray-scaled Inverted feed","Threshold feed","Difference feed","Inverted feed"]
        self.rasputin = 1
        self.threshold = 0
        self.threat_level = 0
        self.current_window = 0
        self.detection_threshold = 5000
        self.freeze = False
        self.save_vid = False
        self.marker_list = []


# Assigning our static_back to None
        self.static_back = None
  
# List when any moving object appear
        self.motion_list = [ None, None ]
  
# Time of movement
        self.time1 = []




  
# Capturing video

        self.video = cv2.VideoCapture(0)


        self.Hdetect = False

        self.robert = 5 #The amount of times the [while True:] loop has to run before actually starting the program

        self.x = int()
        self.jose = 0

        self.frame_type = int()

        self.movement_time = int()
        self.loop_count = int()

        self.action_time = int()
        self.action = str()
        self.action_limit = 30

        self.save_date = datetime.now()
        self.save_date = str(self.save_date)
        self.save_date = self.save_date.replace(":","_")

        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out = cv2.VideoWriter(self.save_date+'.avi', self.fourcc, 20.0, (640, 480))


        self.ww = int(self.video.get(cv2. CAP_PROP_FRAME_WIDTH ))
        self.hh = int(self.video.get(cv2. CAP_PROP_FRAME_HEIGHT ))

        self.m = 1.25 #Window size multiplier

        self.display_width = round(self.ww*self.m)
        self.display_height = round(self.hh*self.m)


    def findArucoMarkers(self,img, markerSize = 5, totalMarkers=250, draw=True):
        self.gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        self.key = getattr(aruco, f'DICT_{markerSize}X{markerSize}_{totalMarkers}')
        self.arucoDict = aruco.Dictionary_get(self.key)
        self.arucoParam = aruco.DetectorParameters_create()
        self.bboxs, self.ids, self.rejected = aruco.detectMarkers(self.gray, self.arucoDict, parameters = self.arucoParam)
    # if ids != None:
    #     print(ids)


# Infinite while loop to treat stack of image as video
    def image_processing(self,flipframe:bool,key:str):
        while True:
            self.c = self.current_window
            if self.freeze != True:
                self.checkH, self.frameH = self.video.read()
                self.check, self.regular = self.video.read()
                self.check, self.frame = self.video.read()

    

            else:
                self.action = f"Froze image"


            self.jose += 1
    
        # Initializing motion = 0(no motion)
            self.motion = 0
  
        # Converting color image to gray_scale image
            self.gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

    #Aight let's invert the feed colors
            self.invertedFrame = cv2.bitwise_not(self.frame)
    #Inverted the colors of the feed. That was easy

    #Inverted gray frame. Let's go !
            self.grayInverted = cv2.bitwise_not(self.gray)

            if self.check == True:

                if self.current_window == 1:

                    self.bounding_box_cordinates, self.weights =  self.hog.detectMultiScale(self.frame, winStride = (4, 4), padding = (8, 8), scale = 0.5)
        
                    for self.x,self.y,self.w,self.h in self.bounding_box_cordinates:
                        cv2.rectangle(self.frameH, (self.x,self.y), (self.x+self.w,self.y+self.h), (0,255,0), 2)


                self.height, self.width, self.layers = self.frame.shape
                zeroImgMatrix = numpy.zeros((self.height,self.width),dtype="uint8")
                (self.B, self.G, self.R) = cv2.split(self.frame)
        
                self.B = cv2.merge([self.B, zeroImgMatrix,zeroImgMatrix])
                self.G = cv2.merge([zeroImgMatrix,self.G,zeroImgMatrix])
                self.R = cv2.merge([zeroImgMatrix,zeroImgMatrix,self.R])

                self.final = numpy.zeros((self.height*2, self.width*2,3),dtype="uint8")
                self.final[0:self.height, self.width:self.width * 2] = self.B # 2nd Quarter= Blue
                self.final[self.height:self.height * 2, 0:self.width] = self.G   # 3rd Quarter= Red
                self.final[self.height:self.height * 2, self.width:self.width * 2] = self.R  # 4th Quarter= Green
        #R is the red channel
        #G is the green channel
        #B is the blue channel
    # Converting gray scale image to GaussianBlur 
    # so that change can be find easily
            self.gray = cv2.GaussianBlur(self.gray, (21, 21), 0)
  
    # In first iteration we assign the value 
    # of static_back to our first frame
            if (self.static_back is None) or keyboard.is_pressed("r") or (self.refresh == True) or (self.jose == 5):
                self.jose = 0
                self.refresh = False
                self.static_back = self.gray
                continue
  
    # Difference between static background 
    # and current frame(which is GaussianBlur)
            self.diff_frame = cv2.absdiff(self.static_back, self.gray)
    
    # If change in between static background and
    # current frame is greater than 30 it will show white color(255)
            self.thresh_frame = cv2.threshold(self.diff_frame, 32.5, 255, cv2.THRESH_BINARY)[1]
            self.thresh_frame = cv2.dilate(self.thresh_frame, None, iterations = 2)
            if self.loop_count == 99:
                self.refresh = True
            if self.loop_count > self.robert:
    # Finding contour of moving object

        
                self.cnts,_ = cv2.findContours(self.thresh_frame.copy(), 
                               cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  
                for self.contour in self.cnts:
                    if cv2.contourArea(self.contour) < self.detection_threshold:
                        continue
                    self.motion = 1
  
                    (self.x, self.y, self.w, self.h) = cv2.boundingRect(self.contour)
        # making green rectangle arround the moving object

                    if self.Hdetect == False:
                        cv2.rectangle(self.frame, (self.x, self.y), (self.x + self.w, self.y + self.h), (0, 0, 255), 2)
                    self.movement_time += 1
                    if self.movement_time == 100:
                        self.static_back = self.gray
                        self.movement_time = 0
  
    # Appending status of motion
            self.motion_list.append(self.motion)
  
            self.motion_list = self.motion_list[-2:]
  
    # Appending Start time of motion
            if self.motion_list[-1] == 1 and self.motion_list[-2] == 0:
                self.time1.append(datetime.now())
    
    # Appending End time of motion
            if self.motion_list[-1] == 0 and self.motion_list[-2] == 1:
                self.time1.append(datetime.now())

            self.feeds = [self.regular,self.frame,self.frameH,self.R,self.G,self.B,self.gray,self.grayInverted,self.thresh_frame,self.diff_frame,self.invertedFrame]

            cnts,_ = cv2.findContours(self.thresh_frame.copy(), 
                               cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            self.alpha_str = str()
            self.alpha_list = list()
            for i in self.cnts:
                self.alpha_list.append("|")
            self.movement_level = self.alpha_str.join(self.alpha_list)


            self.findArucoMarkers(self.frame)

    
            marker_size = 5

            totalMarkers = 100

            for i in [4,5,6,7]:
                self.aruco_key = getattr(aruco, f'DICT_{i}X{i}_{totalMarkers}')
                self.arucoDict = aruco.Dictionary_get(self.aruco_key)
                self.arucoParam = aruco.DetectorParameters_create()
                self.corners, self.ids, self.rejected = aruco.detectMarkers(self.gray, self.arucoDict, parameters = self.arucoParam)                    
                self.aruco.drawDetectedMarkers(self.feeds[self.current_window],self.corners,self.ids,(0,255,0))

            if self.marker_list != None:
                self.marker_list = str(self.ids)#.replace("[[","").replace("]]","")


            cv2.putText(self.feeds[self.current_window], f'[Current mode]>: {self.window_types[self.current_window]}', (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,0), 3)
            cv2.putText(self.feeds[self.current_window], f'[!]>{self.movement_level}', (10,45), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,0), 3)
            cv2.putText(self.feeds[self.current_window], f'[Resolution]>{self.ww}x{self.hh}', (10,475), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,0), 3)
            cv2.putText(self.feeds[self.current_window], f'[Display]>{self.display_width}x{self.display_height}', (10,450), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,0), 3)
            cv2.putText(self.feeds[self.current_window], f'[Current mode]>: {self.window_types[self.current_window]}', (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255,255,255), 2)
            cv2.putText(self.feeds[self.current_window], f'[Markers]>{self.marker_list}', (10,420), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,0), 3)
            cv2.putText(self.feeds[self.current_window], f'[!]>{self.movement_level}', (10,45), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255,255,255), 2)
            cv2.putText(self.feeds[self.current_window], f'[Resolution]>{self.ww}x{self.hh}', (10,475), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255,255,255), 2)
            cv2.putText(self.feeds[self.current_window], f'[Display]>{self.display_width}x{self.display_height}', (10,450), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255,255,255), 2)
            cv2.putText(self.feeds[self.current_window], f'[Markers]>{self.marker_list}', (10,420), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255,255,255), 2)
    
            if self.action != "":
                cv2.putText(self.feeds[self.current_window], self.action, (300,475), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 3)
                cv2.putText(self.feeds[self.current_window], self.action, (300,475), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
            if self.save_vid == True:
                self.rec = "."
                cv2.putText(self.feeds[self.current_window], self.rec, (30,100), cv2.FONT_HERSHEY_SIMPLEX, 5, (0,0,255), 10)
            elif self.save_vid == False:
                self.rec = ""
                cv2.putText(self.feeds[self.current_window], self.rec, (5,60), cv2.FONT_HERSHEY_SIMPLEX, 5, (0,0,255), 10)

            self.action_time += 1
            if self.action_time >= self.action_limit:
                self.action = ""
                self.action_time = 0

            self.feeds[self.current_window] = cv2.resize(self.feeds[self.current_window],(self.display_width,self.display_height))


            if flipframe == True:
                self.frame = cv2.flip(self.frame, 1)
                self.frameH = cv2.flip(self.frameH,1)
                self.regular = cv2.flip(self.regular,1)

    # cv2.imshow(f"OpenCV2-Python image processing",feeds[current_window])

            self.returned_frame = self.feeds[self.current_window]

    
            if self.save_vid == True:
                self.out.write(self.feeds[self.current_window])


            key = None #Replace with interaction with webserver

            if key == ("space"):
                if freeze == True:
                    freeze = False
                else:
                    freeze = True
                time.sleep(0.5)

            if key == ("left"):
                self.action = (f"Switching to [{self.window_types[self.current_window-1]}]")
                self.action_time = 0
                if self.current_window == (len(self.feeds)-1):
                    self.current_window = 0
                else:
                    self.current_window += 1
                time.sleep(0.1)

            elif key == ("right"):
                self.action = (f"Switching to [{self.window_types[self.current_window-1]}]")
                self.action_time = 0
                if self.current_window == 0:
                    self.current_window = (len(self.feeds)-1)
                else:
                    self.current_window += -1
                time.sleep(0.1)
    
            elif key == ("up"):
                self.threshold += 1000
                self.action = (f"Increasing detection threshold - {self.threshold}")
    
            elif key == ("down"):
                self.threshold += -1000
                self.action = (f"Decreasing detection threshold - {self.threshold}")

    # if q entered whole process will stop
            if key == ('q'):
        # if something is movingthen it append the end time of movement
                if self.motion == 1:
                    self.time1.append(datetime.now())
                break
    
    
            elif key == ("s"):
                self.current_date = datetime.now()
                self.current_date = str(self.current_date)
                self.current_date = self.current_date.replace(":","_")
                cv2.imwrite(self.current_date+".jpg",self.frame)
                self.action = (f"Saved frame as {self.current_date}.png ")
                self.action_time = 0

            elif key == ("help"):
                return

            if self.loop_count <= (self.robert+1):
                self.loop_count += 1


  

        self.out.release()
        self.video.release()
  


# Destroying all the windows
        cv2.destroyAllWindows()
