from flask import Flask, render_template, Response, redirect
import cv2, numpy
from webpage import *
from cv2 import aruco as aruco
import lib

# web_image_processor = image_processor(flipframe=False,imshow=False,key=None)

app = Flask(__name__)

static_back = numpy.array
detection_threshold = 5000
motion = 0
current_feed = 0

camera = cv2.VideoCapture(0)

@app.route('/')
def index():
    return render_template('index.html')

def reg_gen_frames():  
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            frame = cv2.flip(frame,1)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

def gen_frames():

    global current_feed

    check, frame = camera.read()
    frameD = frame

    loop_count = 0
    static_back = None

    feeds = [frame,frameD]

    while True:
        check, frame = camera.read()
        frameD = frame


        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if (static_back is None) or (loop_count == 10):
            static_back = gray
            loop_count = 0
            continue

        diff_frame = cv2.absdiff(static_back, gray)

        thresh_frame = cv2.threshold(diff_frame, 32.5, 255, cv2.THRESH_BINARY)[1]
        thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)

        cnts,_ = cv2.findContours(thresh_frame.copy(), 
                       cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in cnts:
            if cv2.contourArea(contour) < detection_threshold:
                continue
            motion = 1
  
            (x, y, w, h) = cv2.boundingRect(contour)
        # making green rectangle arround the moving object

            
            check, frame = camera.read()
            
            cv2.rectangle(frameD, (x, y), (x + w, y + h), (0, 255, 0), 1)

            

            ret, buffer = cv2.imencode(".jpg",frameD)
            out_frame = buffer.tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n'+out_frame+b'\r\n')
        loop_count += 1

def gen_gray():
    while True:
        check, frame = camera.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if not check:
            break
        else:
            gray = cv2.flip(gray,1)
            frame_n, buffer = cv2.imencode('.jpg', gray)
            frame_n = buffer.tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame_n + b'\r\n') 

def gray_inverted():
    
    while True:
        check, frame = camera.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.bitwise_not(gray)

        if not check:
            break
        else:
            
            gray = cv2.flip(gray,1)
            frame_in, buffer = cv2.imencode('.jpg', gray)
            frame_in = buffer.tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame_in + b'\r\n') 

def detect_aruco():
    while True:
        fixing = getattr(aruco, f'DICT_4X4_{100}')
        check, frame_aruco = camera.read()

        if not check:
            break
        else:
            lib_dictionnary = aruco.Dictionary_get(fixing)
            totalMarkers = 100
            frame_aruco_gray = cv2.cvtColor(frame_aruco, cv2.COLOR_BGR2GRAY)
            Param = aruco.DetectorParameters_create()
            for i in [4,5,6,7]:
                key = getattr(aruco, f'DICT_{i}X{i}_{totalMarkers}')
                corners, extreme, rejected = aruco.detectMarkers(cv2.bitwise_not(frame_aruco_gray), lib_dictionnary, parameters = Param)
                arucoDict = aruco.Dictionary_get(key)
                arucoParam = aruco.DetectorParameters_create()
                if i == 4:
                    corners, ids_a, rejected = aruco.detectMarkers(frame_aruco_gray, arucoDict, parameters = arucoParam)
                    aruco.drawDetectedMarkers(frame_aruco,corners,ids_a,(0,255,0))
                if i == 5:
                    corners, ids_b, rejected = aruco.detectMarkers(frame_aruco_gray, arucoDict, parameters = arucoParam)                    
                    aruco.drawDetectedMarkers(frame_aruco,corners,ids_b,(0,255,0))
                if i == 6:
                    corners, ids_c, rejected = aruco.detectMarkers(frame_aruco_gray, arucoDict, parameters = arucoParam)                    
                    aruco.drawDetectedMarkers(frame_aruco,corners,ids_c,(0,255,0))
                if i == 7:
                    corners, ids_d, rejected = aruco.detectMarkers(frame_aruco_gray, arucoDict, parameters = arucoParam)                    
                    aruco.drawDetectedMarkers(frame_aruco,corners,ids_d,(0,255,0))
            if "9" in str(extreme):
                exit()
            if "6" in str(extreme):
                lib.equalize()
            frame_aruco = cv2.flip(frame_aruco,1)
            frame_in, buffer = cv2.imencode('.jpg', frame_aruco)
            frame_in = buffer.tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame_in + b'\r\n') 

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/unaltered")
def unaltered():
    return Response(reg_gen_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/gray")
def gray():
    return Response(gen_gray(),mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/gray_inv")
def gray_inv():
    return Response(gray_inverted(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/aruco")
def show_aruco():
    return Response(detect_aruco(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/index")
def here():
    return render_template('index.html')

https = False
if __name__ == "__main__" and https == True:
    app.run(debug=True,ssl_context='adhoc')
    lib.equalize()
elif __name__ == "__main__" and https == False:
    app.run(debug=True)
    lib.equalize()