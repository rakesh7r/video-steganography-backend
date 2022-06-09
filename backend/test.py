from io import BytesIO
import json
import os
from flask import Flask,request,jsonify, send_file
from flask_cors import CORS
import cv2 as cv
import numpy as np
from PIL import Image
import uuid
import numpy as np
from math import log10,sqrt
import cv2 as cv
import random

def PSNR(original, compressed):
    mse = np.mean((original - compressed) ** 2)
    if(mse == 0):
        return 100
    max_pixel = 255.0
    psnr = 20 * log10(max_pixel / sqrt(mse))
    return psnr


def val(c):
    if c >= '0' and c <= '9':
        return ord(c) - ord('0')
    else:
        return ord(c) - ord('A') + 10;
def toDeci(str,base):
    llen = len(str)
    power = 1 
    num = 0     
    for i in range(llen - 1, -1, -1):
        if val(str[i]) >= base:
            print('Invalid Number')
            return -1
        num += val(str[i]) * power
        power = power * base
    return num

def convert(secret):
    sec = []
    for c in secret:
        n = np.base_repr(ord(c),9)
        n = str(n)
        if(len(n) == 1):
            n = "00"+n
        elif(len(n) == 2):
            n = "0"+n
        sec.append(n)
    return sec

def generateRandomMatrix(seed):
    np.random.seed(seed)
    a = np.random.randint( 0,9,size = (40))
    random_matrix = []
    b = 9
    r = []
    i = 0
    while(i < len(a) or len(r) < b):
        if(a[i] not in r):
            r.append(a[i])
        i = i+1        
    ar = np.reshape(r,(3,3))
    rows = cols = 3
    for i in range(0,6):
        c = []
        for j in range(len(ar[i])):
            c.append(ar[i][j])
        np.random.shuffle(c)
        ar = np.append(ar,c)    
        rows += 1
        ar = np.reshape(ar,(rows,3))

    rows,cols = np.shape(ar)
    for i in ar:
        temp = []
        for j in range(len(i)*len(i)):
            temp.append(i[j%len(i)])
        random_matrix.append(temp)
    random_matrix = np.array(random_matrix)
    print(random_matrix)
    return random_matrix

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_PATH'] = "C:/Users/rakes/Desktop/Steganography/Video-steganography/backend/"
filename = ""

def encode(newimg,seed,secret):     
    random_matrix = generateRandomMatrix(seed)
    # img = "colorpic.png"
    # image = Image.open(img, 'r')
    # newimg = image.copy()
    width, height = newimg.size
    secret = "this text will be encoded"
    converted_secret = convert(secret)
    # Encoding starts here
    index = 0
    i = j = 0
    p = q = 0
    flag = False
    index = 0
    i = j = 0
    converted_text = ''.join(map(str, converted_secret))
    data_len = len(converted_text)

    r,g,b = newimg.getpixel((width-1,height-1))
    b = data_len
    newimg.putpixel((width-1,height-1),(r,g,b))

    for i in range(height) :
        for j in range(width) :
            if index >= len(converted_text) :break
            cols = []
            bit = int(converted_text[index])
            index += 1
            rand_row = rand_col = None
            r,g,b = newimg.getpixel((i,j))
            row = int(str(g)[len(str(g)) - 1])
            col = int(str(b)[len(str(b)) - 1])
            
            if row >= 0 and row < 9 and col >= 0 and col < 9 and(random_matrix[row][col] == bit) :
                rand_row = row
                rand_col = col
            elif row-1 >= 0 and row < 9 and col >= 0 and col < 9 and (random_matrix[row-1][col] == bit) :
                rand_row = row-1
                rand_col = col
            elif row+1 < 9 and row-1 >= 0 and col >= 0 and col < 9 and  (random_matrix[row+1][col] == bit) :
                rand_row = row+1
                rand_col = col
            elif col-1 >= 0 and col < 9 and row >= 0 and row < 9 and (random_matrix[row][col-1] == bit) :
                rand_row = row
                rand_col = col-1
            elif col+1 < 9 and col >= 0 and row >= 0 and row < 9 and (random_matrix[row][col+1] == bit) :
                rand_row = row
                rand_col = col+1
            else :
                while len(cols) == 0:
                    rand_row = random.randint(0,len(random_matrix)-1)
                    cols = np.where(random_matrix[rand_row] == int(bit))[0]
                rand_col = random.choice(cols)
            g = str(g)
            b = str(b)
            g = int(g[:len(g)-1]+str(rand_row))
            b = int(b[:len(b)-1]+str(rand_col))
            # print(bit,"=",rand_row,rand_col,(r,g,b),(r1,g1,b1))
            newimg.putpixel((i,j),(r,g,b))
    # newimg.save("res.png")
    return newimg

def decode(newimg,seed) :
    # decoding starts here
    random_matrix = generateRandomMatrix(seed)
    # img = "res.png"
    # image = Image.open(img, 'r')
    # newimg = image.copy()
    width, height = newimg.size
    index = 0
    data = ""
    data_len = newimg.getpixel((width-1,height-1))[2]
    for i in range(height):
        for j in range(width):
            if(index >=data_len) : break
            r,g,b = newimg.getpixel((i,j))
            row = str(g)[len(str(g)) - 1]
            col = str(b)[len(str(b)) - 1]
            data = data + str(random_matrix[int(row)][int(col)])
            index += 1 
    # converting into base 10 
    index = 0
    text = ""
    for i in range(0,len(data),3):
        num = data[i:i+3]
        num = toDeci(num,9)
        text += chr(num)
    # print(text)
    return text

insertedframe = None
insertedframetwo = None
starting_frame = 3

def encodeHandler(secret,filename,seed):
    vid = cv.VideoCapture('input.mp4')
    total_frames = last_frame_number =  vid.get(cv.CAP_PROP_FRAME_COUNT)
    print("Total number of frames : ",last_frame_number)
    # starting_frame = random.randint(1,150)

    text = secret
    if len(text) == 0: 
        return False
    
    text += "0"
    enc_data = convert(text)
    vid.set(1,starting_frame)
    ret, frame = vid.read()
    img_pil = Image.fromarray(frame)
    new_img = encode(img_pil,seed,enc_data)
    new_cv_img = np.asarray(new_img)
    # gray = cv.cvtColor(new_cv_img, cv.IMREAD_COLOR)
    gray = Image.fromarray(new_cv_img)
    insertedframe = gray
    insertedframetwo = new_cv_img
    print((gray))
    gray.save("./.cache/"+filename+".png")
    width, height = img_pil.size
    video_fps = vid.get(cv.CAP_PROP_FPS),
    fourcc = cv.VideoWriter_fourcc(*'avc1')
    writer = cv.VideoWriter("C:/Users/rakes/Downloads/"+filename+".mp4", apiPreference=0, fourcc=fourcc,fps=video_fps[0], frameSize=(width, height))

    frame_number = -1
    while(True):
        frame_number += 1
        vid.set(1,frame_number)
        ret, frame = vid.read()
        if not ret : break  
        if frame_number >= last_frame_number: break
        if frame_number == starting_frame :
            frame = np.asarray(gray)
        writer.write(frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    writer.release()
    cv.destroyAllWindows()
    return True


def decodeHandler(filename,seed):
    vid = cv.VideoCapture('output.mp4')
    vid.set(1,starting_frame)
    ret, frame = vid.read()
    img_pil = Image.open("./.cache/"+filename+".png", 'r')
    return (decode(img_pil,seed))


@app.route('/encode', methods = ['POST'])
def encodeRoute():
    secret = request.form['secret']
    seed = request.form['seed']
    print(seed)
    file = request.files['file']
    filename = file.filename[:-4]
    filename = str(uuid.uuid4())
    file.save(os.path.join(app.config['UPLOAD_PATH'],"input.mp4"))
    if encodeHandler(secret,filename,seed): 
        return jsonify({"status":"success","filename":filename+".mp4"})
    return jsonify({"status" : False})

@app.route("/decode",methods=["POST"])
def decodeRoute():
    file = request.files['file']
    seed = request.form['seed']
    filename = file.filename[:-4]
    file.save(os.path.join(app.config['UPLOAD_PATH'],filename+".mp4"))
    secret = decodeHandler(filename)
    return jsonify({"secret": secret })

if __name__ == '__main__':
    app.run(debug=True)