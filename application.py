from cv2 import data
from flask import Flask, render_template, request, Response, redirect, url_for,json
from flask_bootstrap import Bootstrap
import flask_bootstrap
from object_detection import *
from camera_settings import *


application = Flask(__name__)
Bootstrap(application)
VIDEO=None
CAMERA_URL=0

def initVideoCapture(camera_url=0,width=1920,height=1080,fps=60):
    check_settings()
    global VIDEO
    VIDEO = VideoStreaming(camera_url=camera_url,width=width,height=height,fps=fps)

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
    initVideoCapture(camera_url=0,width=640,height=480,fps=60)
    return Response(
        VIDEO.show(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

@application.route("/reset_frame_info",methods=["POST"])
def reset_frame_info():
    try:
        data=json.loads(request.get_data())
        width=int(data["width"])
        height=int(data["height"])
        fps=int(data["fps"])
        #print(width,height,fps)
        initVideoCapture(CAMERA_URL,width=width,height=height,fps=fps)
    except Exception as e:
        print(str(e))
    
    return "nothing"

@application.route("/reset_camera_url",methods=["POST"])
def reset_camera_url():
    data=json.loads(request.get_data())
    CAMERA_URL=data["url"]
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
    application.run(debug=True)
