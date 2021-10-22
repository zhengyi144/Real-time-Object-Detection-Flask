import time
import cv2
import numpy as np
import json
import requests
import base64
from PIL import Image,ImageFont,ImageDraw


def drawImage(image,out_boxes, out_scores, out_classes):
    #---------------------------------------------------------#
    #   图像绘制
    #---------------------------------------------------------#
    class_colors={"apple":(0,0,255),"carrot":(0,100,255),"banana":(0,160,160),"orange":(56,235,185),"broccoli":(92,240,131)}
    out_classes=eval(out_classes)
    statistics={"apple":0,"carrot":0,"banana":0,"orange":0,"broccoli":0}

    for i, c in list(enumerate(out_classes)):
        if c not in class_colors.keys():
            continue
        statistics[c]+=1
        predicted_class = out_classes[i]#self.class_names[int(c)]
        box= out_boxes[i]
        score=out_scores[i]
        top, left, bottom, right = box
        top = max(0, np.floor(top).astype('int32'))
        left = max(0, np.floor(left).astype('int32'))
        bottom = min(image.shape[0], np.floor(bottom).astype('int32'))
        right = min(image.shape[1], np.floor(right).astype('int32'))

        #绘制框框
        label = '{}'.format(predicted_class)
        cv2.rectangle(image,(left,top),(right,bottom),class_colors[c],2)
        cv2.putText(image,label,(left,top),cv2.FONT_HERSHEY_SIMPLEX,1,class_colors[c],2)
    slabel=""
    for c in statistics.keys():
        if statistics[c]>0:
            slabel+='<{}:{}>'.format(c,statistics[c])
    cv2.putText(image,slabel,(10,20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(50,0,0),2)
        
    return image


def requestYoloResult(image):
    try:
        #rImage=cv2.resize(image,(416,416))
        #print(np.shape(image),np.shape(image))
        #先将图片进行base64编码
        retval, buffer = cv2.imencode('.jpg', image)
        base64image = base64.b64encode(buffer)
        #print(base64image)
        r1 = requests.post(url='http://192.168.23.10:8777/predict/',
                  data=json.dumps({'img':base64image.decode()}),
                  headers={'content-type': 'application/json'}
                  )
        res_data = json.loads(r1.text)
        #print(res_data)
        img_b64decode = base64.b64decode(str.encode(res_data['data']))  # base64解码
        out_boxes = np.frombuffer(img_b64decode, np.float32).reshape(res_data['data_shape'])
        out_scores = np.frombuffer(base64.b64decode(str.encode(res_data['out_scores'])),np.float32 ) # base64解码
        out_classes = res_data['out_classes']
        #print(out_boxes,out_scores,out_classes)

        #对图片进行绘制
        dImage=drawImage(image,out_boxes, out_scores, out_classes)

        result=cv2.resize(dImage,(image.shape[1],image.shape[0]))
        #print(np.shape(result))
        #img_b64decode = base64.b64decode(str.encode(res_data['data']))  # base64解码
        #parr = np.frombuffer(img_b64decode, np.uint8).reshape(res_data['shape'])
        # # 从nparr中读取数据，并把数据转换(解码)成图像格式
        #res_img = Image.fromarray(parr)
        #snap=cv2.cvtColor(parr,cv2.COLOR_RGB2BGR)
        return result
    except Exception as e:
        print("yolo4检测失败:{}".format(str(e)))

class ObjectDetection:
    def __init__(self):
        """
        self.MODEL = cv2.dnn.readNet(
            'models/yolov3.weights',
            'models/yolov3.cfg'
        )
        """
        

        self.CLASSES = []
        with open("models/coco.names", "r") as f:
            self.CLASSES = [line.strip() for line in f.readlines()]

        #self.OUTPUT_LAYERS = [self.MODEL.getLayerNames()[i[0] - 1] for i in self.MODEL.getUnconnectedOutLayers()]
        self.COLORS = np.random.uniform(0, 255, size=(len(self.CLASSES), 3))
        self.COLORS /= (np.sum(self.COLORS**2, axis=1)**0.5/255)[np.newaxis].T

    def detectObj(self, snap):
        height, width, channels = snap.shape
        blob = cv2.dnn.blobFromImage(snap, 1/255, (416, 416), swapRB=True, crop=False)

        self.MODEL.setInput(blob)
        outs = self.MODEL.forward(self.OUTPUT_LAYERS)

        # Showing informations on the screen
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    # Object detected
                    center_x = int(detection[0]*width)
                    center_y = int(detection[1]*height)
                    w = int(detection[2]*width)
                    h = int(detection[3]*height)

                    # Rectangle coordinates
                    x = int(center_x - w/2)
                    y = int(center_y - h/2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        font = cv2.FONT_HERSHEY_PLAIN
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(self.CLASSES[class_ids[i]])
                color = self.COLORS[i]
                cv2.rectangle(snap, (x, y), (x + w, y + h), color, 2)
                cv2.putText(snap, label, (x, y - 5), font, 2, color, 2)
        return snap

class VideoStreaming(object):
    def __init__(self,camera_url=0,width=1920,height=1080,fps=60):
        super(VideoStreaming, self).__init__() 
        #ip_camera_url =0  # 'http://admin:admin@192.168.213.189:8081'

        self._preview = True
        self._flipH = False
        self._detect = False
        self._width=width
        self._height=height
        self._fps=fps
        
        self.CAP = cv2.VideoCapture(camera_url)
        self.CAP.set(cv2.CAP_PROP_FRAME_WIDTH, self._width)
        self.CAP.set(cv2.CAP_PROP_FRAME_HEIGHT, self._height)
        self.CAP.set(cv2.CAP_PROP_FPS, self._fps)
        self._exposure = self.CAP.get(cv2.CAP_PROP_EXPOSURE)
        self._contrast = self.CAP.get(cv2.CAP_PROP_CONTRAST)
    
    @property
    def preview(self):
        return self._preview

    @preview.setter
    def preview(self, value):
        self._preview = bool(value)

    @property
    def flipH(self):
        return self._flipH

    @flipH.setter
    def flipH(self, value):
        self._flipH = bool(value)
    
    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value
        #

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value
        #

    @property
    def fps(self):
        return self._fps

    @fps.setter
    def fps(self, value):
        self._fps= value

    @property
    def detect(self):
        return self._detect

    @detect.setter
    def detect(self, value):
        self._detect = bool(value)


    """
    @property
    def exposure(self):
        return self._exposure

    @exposure.setter
    def exposure(self, value):
        self._exposure = value
        self.CAP.set(cv2.CAP_PROP_EXPOSURE, self._exposure)

    @property
    def contrast(self):
        return self._contrast

    @contrast.setter
    def contrast(self, value):
        self._contrast = value
        self.CAP.set(cv2.CAP_PROP_CONTRAST, self._contrast)
    """
    

    def convertImage(self,image,outSize):
        #图像转换
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_data = cv2.resize(image, (outSize, outSize))
        image_data = image_data / 255.
        image_data = image_data[np.newaxis, ...].astype(np.float32)
        return image_data

    def show(self):
        i=0
        while(self.CAP.isOpened()):
            ret, snap = self.CAP.read()
            if self.flipH:
                snap = cv2.flip(snap, 1)
            if ret == True:
                if self._preview:
                    # snap = cv2.resize(snap, (0, 0), fx=0.5, fy=0.5)
                    if self.detect:
                        #print("此处检查显示!")
                        snap=requestYoloResult(snap)

                        #self.detect=False
                        #cv2.imwrite("/Users/zhengyi/imageset/{}.jpg".format(i),snap)
                        #i+=1
                else:
                    snap = np.zeros((
                        int(self.CAP.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                        int(self.CAP.get(cv2.CAP_PROP_FRAME_WIDTH))
                    ), np.uint8)
                    label = 'camera disabled'
                    H, W = snap.shape
                    font = cv2.FONT_HERSHEY_COMPLEX
                    color = (255,255,255)
                    cv2.putText(snap, label, (W//2, H//2), font, 2, color, 2)

                frame = cv2.imencode('.jpg', snap)[1].tobytes()
                yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                time.sleep(0.01)

            else:
                break
        print('off')


if __name__=="__main__":
    image=cv2.imread("static/banana.jpg")
    result=requestYoloResult(image)
    cv2.imshow("test",result)
    cv2.waitKey(0)

