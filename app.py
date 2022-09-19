import base64
from flask import Flask, jsonify, request
from flask_cors import CORS
import urllib.request
import urllib.error
import time
import json
import pymongo
import certifi
import math
import tinify


app=Flask(__name__)
CORS(app)
client = pymongo.MongoClient("mongodb+srv://Eric:zx50312zx@training.9vikg.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",tlsCAFile=certifi.where())
db = client.cosme #選擇操作cosme資料庫

### 首頁，測試用
@app.route("/",methods=["GET","POST"])
def index():
    return jsonify({"success":True,"message":"It's face++ api."})

############################################ 取得臉部分析資料
####### function
def FacePlus_features(base64Data):
    ### get imgfile represented in base64 
    analysis_result={}
    imgData = base64.b64decode(base64Data)
    #print(type(imgData))

    http_url = 'https://api-cn.faceplusplus.com/facepp/v1/facialfeatures'
    key = "0nzG98sy92I9MJeW_RwrSlxkTNiylvdJ"
    secret = "tckC6RMYCSTD1DNRvnYsoe4XpLr4F_dN"
    filepath = "https://i0.wp.com/post.medicalnewstoday.com/wp-content/uploads/sites/3/2020/03/GettyImages-1092658864_hero-1024x575.jpg?w=1155&h=1528"

    boundary = '----------%s' % hex(int(time.time() * 1000))
    data = []
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_key')
    data.append(key)
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_secret')
    data.append(secret)
    data.append('--%s' % boundary)
    
    data.append('Content-Disposition: form-data; name="%s"; filename=" "' % 'image_file')
    data.append('Content-Type: %s\r\n' % 'application/octet-stream')
    data.append(imgData)

    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'return_landmark')
    data.append('1')
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'return_attributes')
    data.append(
        "gender,age,smiling,headpose,facequality,blur,eyestatus,emotion,ethnicity,beauty,mouthstatus,eyegaze,skinstatus")
    data.append('--%s--\r\n' % boundary)

    for i, d in enumerate(data):
        if isinstance(d, str):
            data[i] = d.encode('utf-8')

    http_body = b'\r\n'.join(data)

    # build http request
    req = urllib.request.Request(url=http_url, data=http_body)

    # header
    req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)

    try:
        # post data to server
        resp = urllib.request.urlopen(req, timeout=None)
        # get response
        qrcont = resp.read()
        # if you want to load as json, you should decode first,
        # for example: json.loads(qrount.decode('utf-8'))
        #print(type(json.loads(qrcont.decode('utf-8'))))
        qrcont = json.loads(qrcont.decode('utf-8'))
        analysis_result["nose_type"] = qrcont["result"]["nose"]["nose_type"]
        analysis_result["face_type"] = qrcont['result']['face']["face_type"]
        analysis_result["jaw_type"] =  qrcont['result']['jaw']["jaw_type"]
        analysis_result["eyebrow_type"] = qrcont['result']['eyebrow']["eyebrow_type"]
        analysis_result["eye_type"] = qrcont['result']['eyes']["eyes_type"]
        return jsonify(analysis_result)
        
    except urllib.error.HTTPError as e:
        print(e.read().decode('utf-8'))

def FacePlus_featuresOrigin(base64Data):
    ### get imgfile represented in base64 
    imgData = base64.b64decode(base64Data)
    #print(type(imgData))

    http_url = 'https://api-cn.faceplusplus.com/facepp/v1/facialfeatures'
    key = "0nzG98sy92I9MJeW_RwrSlxkTNiylvdJ"
    secret = "tckC6RMYCSTD1DNRvnYsoe4XpLr4F_dN"

    boundary = '----------%s' % hex(int(time.time() * 1000))
    data = []
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_key')
    data.append(key)
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_secret')
    data.append(secret)
    data.append('--%s' % boundary)
    
    data.append('Content-Disposition: form-data; name="%s"; filename=" "' % 'image_file')
    data.append('Content-Type: %s\r\n' % 'application/octet-stream')
    data.append(imgData)

    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'return_landmark')
    data.append('1')
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'return_attributes')
    data.append(
        "gender,age,smiling,headpose,facequality,blur,eyestatus,emotion,ethnicity,beauty,mouthstatus,eyegaze,skinstatus")
    data.append('--%s--\r\n' % boundary)

    for i, d in enumerate(data):
        if isinstance(d, str):
            data[i] = d.encode('utf-8')

    http_body = b'\r\n'.join(data)

    # build http request
    req = urllib.request.Request(url=http_url, data=http_body)

    # header
    req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)

    try:
        # post data to server
        resp = urllib.request.urlopen(req, timeout=None)
        # get response
        qrcont = resp.read()
        # if you want to load as json, you should decode first,
        # for example: json.loads(qrount.decode('utf-8'))
        #print(type(json.loads(qrcont.decode('utf-8'))))
        qrcont = json.loads(qrcont.decode('utf-8'))
        return qrcont["result"]
        
    except urllib.error.HTTPError as e:
        print(e.read().decode('utf-8'))

def FacePlus_eyesLandmarks(base64Data):
    imgData = base64.b64decode(base64Data)
    #print(type(imgData))

    http_url = 'https://api-cn.faceplusplus.com/facepp/v1/face/thousandlandmark'
    key = "0nzG98sy92I9MJeW_RwrSlxkTNiylvdJ"
    secret = "tckC6RMYCSTD1DNRvnYsoe4XpLr4F_dN"

    boundary = '----------%s' % hex(int(time.time() * 1000))
    data = []
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_key')
    data.append(key)
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_secret')
    data.append(secret)
    data.append('--%s' % boundary)
    
    data.append('Content-Disposition: form-data; name="%s"; filename=" "' % 'image_file')
    data.append('Content-Type: %s\r\n' % 'application/octet-stream')
    data.append(imgData)

    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'return_landmark')
    data.append('right_eye')
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'return_attributes')
    data.append(
        "gender,age,smiling,headpose,facequality,blur,eyestatus,emotion,ethnicity,beauty,mouthstatus,eyegaze,skinstatus")
    data.append('--%s--\r\n' % boundary)

    for i, d in enumerate(data):
        if isinstance(d, str):
            data[i] = d.encode('utf-8')

    http_body = b'\r\n'.join(data)

    # build http request
    req = urllib.request.Request(url=http_url, data=http_body)

    # header
    req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)

    try:
        # post data to server
        resp = urllib.request.urlopen(req, timeout=None)
        # get response
        qrcont = resp.read()
        # if you want to load as json, you should decode first,
        # for example: json.loads(qrount.decode('utf-8'))
        #print(type(json.loads(qrcont.decode('utf-8'))))
        qrcont = json.loads(qrcont.decode('utf-8'))
        
        return qrcont['face']['landmark']
    except urllib.error.HTTPError as e:
        print(e.read().decode('utf-8'))

def FacePLus_faceDetect(base64Data):
    ### get imgfile represented in base64 
    imgData = base64.b64decode(base64Data)
    #print(type(imgData))
    http_url = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
    key = "0nzG98sy92I9MJeW_RwrSlxkTNiylvdJ"
    secret = "tckC6RMYCSTD1DNRvnYsoe4XpLr4F_dN"
    filepath = "https://i0.wp.com/post.medicalnewstoday.com/wp-content/uploads/sites/3/2020/03/GettyImages-1092658864_hero-1024x575.jpg?w=1155&h=1528"

    boundary = '----------%s' % hex(int(time.time() * 1000))
    data = []
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_key')
    data.append(key)
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_secret')
    data.append(secret)
    data.append('--%s' % boundary)
    
    data.append('Content-Disposition: form-data; name="%s"; filename=" "' % 'image_file')
    data.append('Content-Type: %s\r\n' % 'application/octet-stream')
    data.append(imgData)

    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'return_landmark')
    data.append('1')
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'return_attributes')
    data.append(
        "gender,age,smiling,headpose,facequality,blur,eyestatus,emotion,ethnicity,beauty,mouthstatus,eyegaze,skinstatus")
    data.append('--%s--\r\n' % boundary)

    for i, d in enumerate(data):
        if isinstance(d, str):
            data[i] = d.encode('utf-8')

    http_body = b'\r\n'.join(data)

    # build http request
    req = urllib.request.Request(url=http_url, data=http_body)

    # header
    req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)

    try:
        # post data to server
        resp = urllib.request.urlopen(req, timeout=None)
        # get response
        qrcont = resp.read()
        # if you want to load as json, you should decode first,
        # for example: json.loads(qrount.decode('utf-8'))
        print(type(json.loads(qrcont.decode('utf-8'))))
        return jsonify(json.loads(qrcont.decode('utf-8')))
        
    except urllib.error.HTTPError as e:
        print(e.read().decode('utf-8'))

def cal_angle(point_1, point_2, point_3): 
    a=math.sqrt((point_2[0]-point_3[0])*(point_2[0]-point_3[0])+(point_2[1]-point_3[1])*(point_2[1] - point_3[1]))
    b=math.sqrt((point_1[0]-point_3[0])*(point_1[0]-point_3[0])+(point_1[1]-point_3[1])*(point_1[1] - point_3[1]))
    c=math.sqrt((point_1[0]-point_2[0])*(point_1[0]-point_2[0])+(point_1[1]-point_2[1])*(point_1[1]-point_2[1]))
    A=math.degrees(math.acos((a*a-b*b-c*c)/(-2*b*c)))
    B=math.degrees(math.acos((b*b-a*a-c*c)/(-2*a*c)))
    C=math.degrees(math.acos((c*c-a*a-b*b)/(-2*a*b)))
    return B

def byteString_to_byte(data):
        data=data.encode(encoding="ascii")
        result2 = data.decode('unicode-escape').encode('ISO-8859-1')
        base64Data = base64.b64encode(result2)
        return base64Data

def compressImg(data):
    data = base64.b64decode(data)
    # data = str(data[2:-1])[2:-1]
    tinify.key = "c10frTbWzgvTj7gbwwgKmNsJmnCXWgwh"
    result_data = tinify.from_buffer(data).to_buffer() 
    result_data =  byteString_to_byte((str(result_data))[2:-1])
    return result_data

### 取得 face_analysis 的資料
@app.route("/face_analysis",methods=["GET","POST"])
def face_analysis():
    data = request.values["data"]
    return FacePlus_features(compressImg(data))

### 取得 face_detect 的資料
@app.route("/face_detect",methods=["GET","POST"])
def face_detect():
    data = request.values["data"]
    return FacePlus_features(compressImg(data))

### 眼睛分析推薦
@app.route("/get-eyesRecommend",methods=["POST"])
def get_eyesRecommend():
    eyes_type={}
    eyes_type["BBAB"] = "清澈圓杏眼"
    eyes_type["BAAA"] = "清澈圓杏眼"
    eyes_type["BBAA"] = "清澈圓杏眼"
    eyes_type["BBBB"] = "狗狗無辜眼"
    eyes_type["BBBA"] = "狗狗無辜眼"
    eyes_type["BAAB"] = "狗狗無辜眼"
    eyes_type["BABB"] = "狗狗無辜眼"
    eyes_type["BABA"] = "狗狗無辜眼"
    eyes_type["AAAB"] = "古典丹鳳眼"
    eyes_type["ABAB"] = "古典丹鳳眼"
    eyes_type["AABB"] = "媚絲柳葉眼"
    eyes_type["ABBB"] = "媚絲柳葉眼"
    eyes_type["ABBA"] = "含情桃花眼"
    eyes_type["AABA"] = "含情桃花眼"
    eyes_type["ABAA"] = "清冷吊梢眼"
    eyes_type["AAAA"] = "清冷吊梢眼"
    analysis_eyes_type = ""
    result = {}
    data = request.values["data"]
    eyes_analysisData = FacePlus_featuresOrigin(compressImg(data))
    eye_width = eyes_analysisData["eyes"]["eye_width"]
    eye_heigh = eyes_analysisData["eyes"]["eye_height"]
    eangulus_oculi_medialis = eyes_analysisData["eyes"]["angulus_oculi_medialis"]
    ### landmark
    eyes_landmarkData = FacePlus_eyesLandmarks(compressImg(data))
    right_eye_0 = (eyes_landmarkData["right_eye"]["right_eye_0"]["x"],eyes_landmarkData["right_eye"]["right_eye_0"]["y"])
    right_eye_16 = (eyes_landmarkData["right_eye"]["right_eye_16"]["x"],eyes_landmarkData["right_eye"]["right_eye_16"]["y"])
    right_eye_31 = (eyes_landmarkData["right_eye"]["right_eye_31"]["x"],eyes_landmarkData["right_eye"]["right_eye_31"]["y"])
    angle = int(cal_angle(right_eye_0,right_eye_16,right_eye_31))
    right_eye_0_y = -eyes_landmarkData["right_eye"]["right_eye_0"]["y"]
    right_eye_31_y = -eyes_landmarkData["right_eye"]["right_eye_31"]["y"]

    if eye_width>eye_heigh*2:
        analysis_eyes_type = analysis_eyes_type+"A"
    else:
        analysis_eyes_type = analysis_eyes_type+"B"
    ######################################
    if int(eangulus_oculi_medialis) <= 45:
        analysis_eyes_type = analysis_eyes_type+"A"
    else:
        analysis_eyes_type = analysis_eyes_type+"B"
    ######################################
    if right_eye_0_y > right_eye_31_y:
        analysis_eyes_type = analysis_eyes_type+"A"
    else:
        analysis_eyes_type = analysis_eyes_type+"B"
    ######################################
    if angle<=165:
        analysis_eyes_type = analysis_eyes_type+"A"
    else:
        analysis_eyes_type = analysis_eyes_type+"B"

    #進資料庫取得資料
    collection = db["eyes_type"]
    result = collection.find_one({"name":eyes_type[analysis_eyes_type]})
    del result["_id"]
    result["eyes_example_image"] = "data:image/png;base64," + str(byteString_to_byte(result["eyes_example_image"][2:-1]))[2:-1]

    return jsonify(result)

### 臉部分析推薦
@app.route("/get-faceRecommend",methods=["POST"])
def get_faceRecommend():
    data = request.values["data"]
    faceCategory = FacePlus_featuresOrigin(compressImg(data))["face"]["face_type"]
    collection = db["face_type"]
    result = collection.find_one({"type":faceCategory})
    del result["_id"]
    result["face_example_image"] = "data:image/png;base64," + str(byteString_to_byte(result["face_example_image"][2:-1]))[2:-1]
    result["eyebrow_example_image"] = "data:image/png;base64," + str(byteString_to_byte(result["eyebrow_example_image"][2:-1]))[2:-1]
    return jsonify(result)

@app.route("/getResult",methods=["POST"])
def get_result():
    pass

############################################ 化妝品資料
####### function
def get_data(cosmetics_name):
    ### convert byte to base64
    def byteString_to_byte(data):
        data=data.encode(encoding="ascii")
        result2 = data.decode('unicode-escape').encode('ISO-8859-1')
        base64Data = base64.b64encode(result2)
        return base64Data
    collection = db[cosmetics_name]
    result = collection.find()
    data = []
    frontSentence = "data:image/png;base64,"
    for id , x in enumerate(result):
        del x["_id"]
        x["key"] = id+1
        x["image"] = frontSentence + str(byteString_to_byte(x["image"][2:-1]))[2:-1]
        data.append(x)
    return jsonify(data)

### 取得唇膏資料
@app.route("/get-lipstick")
def get_lipstick():
    return get_data("lipstick")

### 取得腮紅資料
@app.route("/get-blush")
def get_blush():
    return get_data("blush")

### 取得唇蜜資料
@app.route("/get-lipgloss")
def get_lip_gloss():
    return get_data("lip_gloss")

### 取得眼影資料
@app.route("/get-eyeshadow")
def get_eye_shadow():
    return get_data("eye_shadow")

### 取得香水資料
@app.route("/get-perfume")
def get_perfume():
    return get_data("perfume")

### 取得睫毛膏
@app.route("/get-mascara")
def get_mascara():
    return get_data("mascara")

### 取得眉筆
@app.route("/get-eyebrow_pencil")
def get_eyebrow_pencil():
    return get_data("eyebrow_pencil")

### 取得防曬
@app.route("/get-sun_protection")
def get_sun_protection():
    return get_data("sun_protection")

### 取得底妝
@app.route("/get-base_makeup")
def get_base_makeup():
    return get_data("base_makeup")

### 取得修容
@app.route("/get-trimming")
def get_trimming():
    return get_data("Trimming")

### 取得打亮
@app.route("/get-light_up")
def get_light_up():
    return get_data("light_up")


############################################ 懶人包資料
### 資料處理function
def get_cosme_set_data(set_name,cosme_category):
    ### convert byte to base64
    def byteString_to_byte(data):
        data=data.encode(encoding="ascii")
        result2 = data.decode('unicode-escape').encode('ISO-8859-1')
        base64Data = base64.b64encode(result2)
        return base64Data
    
    collection = db["cosme_set"]
    result = collection.find({"set_name":set_name,"product_category":cosme_category})
    data = []
    frontSentence = "data:image/png;base64,"
    for x in result:
        del x["_id"]
        x["image"] = frontSentence + str(byteString_to_byte(x["image"][2:-1]))[2:-1]
        data.append(x)
    return jsonify(data)

@app.route("/get-set",methods=["POST"])
def get_set():
    set_name = request.values["set_name"]
    category_name = request.values["category_name"]
    return get_cosme_set_data(set_name,category_name)


if __name__=="__main__":
    app.run(host="0.0.0.0",debug=True)
