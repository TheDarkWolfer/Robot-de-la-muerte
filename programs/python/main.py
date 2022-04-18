from datetime import datetime
import keyboard, numpy, cv2, time, pandas

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

window_types = ["Non-filtered feed","Movement detection feed","Human detection feed","Red feed","Green feed","Blue feed","Gray feed","Gray-scaled Inverted feed","Threshold feed","Difference feed","Inverted feed"]
rasputin = 1
threshold = 0
threat_level = 0
current_window = 0
detection_threshold = 5000
freeze = False
save_vid = False

# Assigning our static_back to None
static_back = None
  
# List when any moving object appear
motion_list = [ None, None ]
  
# Time of movement
time1 = []

# Initializing DataFrame, one column is start 
# time and other column is end time
df = pandas.DataFrame(columns = ["Start", "End"])
  
# Capturing video

video = cv2.VideoCapture(0)


Hdetect = False

robert = 5 #The amount of times the [while True:] loop has to run before actually starting the program

x = int()
jose = 0

frame_type = int()

movement_time = int()
loop_count = int()

action_time = int()
action = str()
action_limit = 30

save_date = datetime.now()
save_date = str(save_date)
save_date = save_date.replace(":","_")

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(save_date+'.avi', fourcc, 20.0, (640, 480))


ww = int(video.get(cv2. CAP_PROP_FRAME_WIDTH ))
hh = int(video.get(cv2. CAP_PROP_FRAME_HEIGHT ))

m = 1.25 #Window size multiplier

display_width = round(ww*m)
display_height = round(hh*m)

# Infinite while loop to treat stack of image as video
while True:
    c = current_window
    if freeze != True:
        checkH, frameH = video.read()
        frameH = cv2.flip(frameH,1)
        check, regular = video.read()
        regular = cv2.flip(regular,1)
        check, frame = video.read()
        frame = cv2.flip(frame, 1)


    else:
        action = f"Froze image"


    jose += 1

    
    # Initializing motion = 0(no motion)
    motion = 0
  
    # Converting color image to gray_scale image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #Aight let's invert the feed colors
    invertedFrame = cv2.bitwise_not(frame)
    #Inverted the colors of the feed. That was easy

    #Inverted gray frame. Let's go !
    grayInverted = cv2.bitwise_not(gray)

    if check == True:

        if current_window == 1:

            bounding_box_cordinates, weights =  hog.detectMultiScale(frame, winStride = (4, 4), padding = (8, 8), scale = 0.5)
        
            for x,y,w,h in bounding_box_cordinates:
                cv2.rectangle(frameH, (x,y), (x+w,y+h), (0,255,0), 2)


        height, width, layers = frame.shape
        zeroImgMatrix = numpy.zeros((height,width),dtype="uint8")
        (B, G, R) = cv2.split(frame)
        
        B = cv2.merge([B, zeroImgMatrix,zeroImgMatrix])
        G = cv2.merge([zeroImgMatrix,G,zeroImgMatrix])
        R = cv2.merge([zeroImgMatrix,zeroImgMatrix,R])

        final = numpy.zeros((height*2, width*2,3),dtype="uint8")
        final[0:height, width:width * 2] = B # 2nd Quarter= Blue
        final[height:height * 2, 0:width] = G   # 3rd Quarter= Red
        final[height:height * 2, width:width * 2] = R  # 4th Quarter= Green
        #R is the red channel
        #G is the green channel
        #B is the blue channel
    # Converting gray scale image to GaussianBlur 
    # so that change can be find easily
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
  
    # In first iteration we assign the value 
    # of static_back to our first frame
    if (static_back is None) or keyboard.is_pressed("r") or (refresh == True) or (jose == 5):
        jose = 0
        refresh = False
        static_back = gray
        continue
  
    # Difference between static background 
    # and current frame(which is GaussianBlur)
    diff_frame = cv2.absdiff(static_back, gray)
    
    # If change in between static background and
    # current frame is greater than 30 it will show white color(255)
    thresh_frame = cv2.threshold(diff_frame, 32.5, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)
    if loop_count == 99:
        refresh = True
    if loop_count > robert:
    # Finding contour of moving object

        
        cnts,_ = cv2.findContours(thresh_frame.copy(), 
                       cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  
        for contour in cnts:
            if cv2.contourArea(contour) < detection_threshold:
                continue
            motion = 1
  
            (x, y, w, h) = cv2.boundingRect(contour)
        # making green rectangle arround the moving object

            if Hdetect == False:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            movement_time += 1
            if movement_time == 100:
                static_back = gray
                movement_time = 0
  
    # Appending status of motion
    motion_list.append(motion)
  
    motion_list = motion_list[-2:]
  
    # Appending Start time of motion
    if motion_list[-1] == 1 and motion_list[-2] == 0:
        time1.append(datetime.now())
  
    # Appending End time of motion
    if motion_list[-1] == 0 and motion_list[-2] == 1:
        time1.append(datetime.now())

    feeds = [regular,frame,frameH,R,G,B,gray,grayInverted,thresh_frame,diff_frame,invertedFrame]

    cnts,_ = cv2.findContours(thresh_frame.copy(), 
                       cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    alpha_str = str()
    alpha_list = list()
    for i in cnts:
        alpha_list.append("|")
    movement_level = alpha_str.join(alpha_list)
    

    cv2.putText(feeds[current_window], f'[Current mode]>: {window_types[current_window]}', (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,0), 3)
    cv2.putText(feeds[current_window], f'[!]>{movement_level}', (10,45), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,0), 3)
    cv2.putText(feeds[current_window], f'[Resolution]>{ww}x{hh}', (10,475), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,0), 3)
    cv2.putText(feeds[current_window], f'[Display]>{display_width}x{display_height}', (10,450), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,0), 3)
    cv2.putText(feeds[current_window], f'[Current mode]>: {window_types[current_window]}', (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255,255,255), 2)
    cv2.putText(feeds[current_window], f'[!]>{movement_level}', (10,45), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255,255,255), 2)
    cv2.putText(feeds[current_window], f'[Resolution]>{ww}x{hh}', (10,475), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255,255,255), 2)
    cv2.putText(feeds[current_window], f'[Display]>{display_width}x{display_height}', (10,450), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255,255,255), 2)
    if action != "":
        cv2.putText(feeds[current_window], action, (300,475), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 3)
        cv2.putText(feeds[current_window], action, (300,475), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
    if save_vid == True:
        rec = "."
        cv2.putText(feeds[current_window], rec, (30,100), cv2.FONT_HERSHEY_SIMPLEX, 5, (0,0,255), 10)
    elif save_vid == False:
        rec = ""
        cv2.putText(feeds[current_window], rec, (5,60), cv2.FONT_HERSHEY_SIMPLEX, 5, (0,0,255), 10)

    action_time += 1
    if action_time >= action_limit:
        action = ""
        action_time = 0

    feeds[current_window] = cv2.resize(feeds[current_window],(display_width,display_height))

    cv2.imshow(f"OpenCV2-Python image processing",feeds[current_window])
    
    if save_vid == True:
        out.write(feeds[current_window])


    key = cv2.waitKey(1)

    if keyboard.is_pressed("space"):
        if freeze == True:
            freeze = False
        else:
            freeze = True
        time.sleep(0.5)

    if keyboard.is_pressed("left"):
        action = (f"Switching to [{window_types[current_window-1]}]")
        action_time = 0
        if current_window == (len(feeds)-1):
            current_window = 0
        else:
            current_window += 1
        time.sleep(0.1)

    elif keyboard.is_pressed("right"):
        action = (f"Switching to [{window_types[current_window-1]}]")
        action_time = 0
        if current_window == 0:
            current_window = (len(feeds)-1)
        else:
            current_window += -1
        time.sleep(0.1)
    
    elif keyboard.is_pressed("up"):
        threshold += 1000
        action = (f"Increasing detection threshold - {threshold}")
    
    elif keyboard.is_pressed("down"):
        threshold += -1000
        action = (f"Decreasing detection threshold - {threshold}")

    # if q entered whole process will stop
    if key == ord('q'):
        saving = False
        # if something is movingthen it append the end time of movement
        if motion == 1:
            time1.append(datetime.now())
        break
    if key == ord('w'):
        saving = True
        # if something is movingthen it append the end time of movement
        if motion == 1:
            time1.append(datetime.now())
        break
    
    
    elif key == ord("s"):
        current_date = datetime.now()
        current_date = str(current_date)
        current_date = current_date.replace(":","_")
        cv2.imwrite(current_date+".jpg",frame)
        action = (f"Saved frame as {current_date}.png ")
        action_time = 0

    if keyboard.is_pressed("i"):
        if save_vid == True:
            save_vid = False
        elif save_vid == False:
            save_vid = True
        time.sleep(0.25)

    elif key == ord('r'):
        threshold = 0
        threat_level = 0
        motion_list = [ None, None ]
        cnts = []
        motion = 0
    if loop_count <= (robert+1):
        loop_count += 1
    

# Appending time of motion in DataFrame
for i in range(0, len(time1), 2):
    df = df.append({"Start":time1[i], "End":time1[i + 1]}, ignore_index = True)
  
# Creating a CSV file in which time of movements will be saved
if saving == True:
    df.to_csv("Time_of_movements.csv")
  

out.release()
video.release()
  


# Destroying all the windows
cv2.destroyAllWindows()