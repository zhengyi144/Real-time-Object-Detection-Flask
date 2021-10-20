from cv2 import data
from flask import Flask, render_template, request, Response, redirect, url_for,json
from flask_bootstrap import Bootstrap
import flask_bootstrap
from object_detection import *
from camera_settings import *


application = Flask(__name__)
Bootstrap(application)
VIDEO=None
CAMERA_URL="http://admin:admin@192.168.214.122:8081"
WIDTH=1920
HEIGHT=1080
FPS=30

def initVideoCapture():
    check_settings()
    global VIDEO
    VIDEO = VideoStreaming(camera_url=CAMERA_URL,width=WIDTH,height=HEIGHT,fps=FPS)

@application.route('/')
def home():
    TITLE = '订单商品自动计数'
    return render_template('index.html', TITLE=TITLE)

@application.route('/video_feed')
def video_feed():
    '''
    Video streaming route.
    '''
    print("初始化video!")
    if VIDEO is None:
        initVideoCapture()
    return Response(
        VIDEO.show(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

@application.route("/reset_frame_info",methods=["POST"])
def reset_frame_info():
    global WIDTH,HEIGHT,FPS
    try:
        data=json.loads(request.get_data())
        width=int(data["width"])
        height=int(data["height"])
        fps=int(data["fps"])
        WIDTH=width
        HEIGHT=height
        FPS=fps
        VIDEO=None
    except Exception as e:
        print(str(e))
    
    return "nothing"

@application.route("/reset_camera_url",methods=["POST"])
def reset_camera_url():
    global CAMERA_URL
    data=json.loads(request.get_data())
    CAMERA_URL=data["url"]
    VIDEO=None
    return "nothing"


# Button requests called from ajax
@application.route('/request_preview_switch')
def request_preview_switch():
    VIDEO.preview = not VIDEO.preview
    print('*'*10, VIDEO.preview)
    return "nothing"

@application.route('/request_flipH_switch')
def request_flipH_switch():
    VIDEO.flipH = not VIDEO.flipH
    print('*'*10, VIDEO.flipH)
    return "nothing"

@application.route('/request_model_switch')
def request_model_switch():
    VIDEO.detect = not VIDEO.detect
    print('*'*10, VIDEO.detect)
    return "nothing"

@application.route('/request_exposure_down')
def request_exposure_down():
    VIDEO.exposure -= 1
    print('*'*10, VIDEO.exposure)
    return "nothing"

@application.route('/request_exposure_up')
def request_exposure_up():
    VIDEO.exposure += 1
    print('*'*10, VIDEO.exposure)
    return "nothing"

@application.route('/request_contrast_down')
def request_contrast_down():
    VIDEO.contrast -= 4
    print('*'*10, VIDEO.contrast)
    return "nothing"

@application.route('/request_contrast_up')
def request_contrast_up():
    VIDEO.contrast += 4
    print('*'*10, VIDEO.contrast)
    return "nothing"

@application.route('/reset_camera')
def reset_camera():
    STATUS = reset_settings()
    print('*'*10, STATUS)
    return "nothing"


if __name__ == '__main__':
    application.run(host="0.0.0.0", port=8080,debug=True)
