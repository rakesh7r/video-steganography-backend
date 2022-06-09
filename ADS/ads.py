import random
import math
import numpy as np
import pandas as pd
from PIL import Image
import os
import cv2 as cv
from math import log10, sqrt

def PSNR(original, compressed):
    mse = np.mean((original - compressed) ** 2)
    if(mse == 0):
        return 100
    max_pixel = 255.0
    psnr = 20 * log10(max_pixel / sqrt(mse))
    return psnr

def MSE(cover,stego):
    mse = np.square(np.subtract(cover,stego)).mean()
    return mse


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

def encode(seed) :
    random_matrix = generateRandomMatrix(seed)
    img = "colorpic.png"
    image = Image.open(img, 'r')
    newimg = image.copy()
    width, height = newimg.size

    secret = "this text will be encoded"
    converted_secret = convert(secret)

    # Encoding starts here
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
            elif col-1 >= 0 and row-1 >=0 and random_matrix[row-1][col-1] == bit: 
                rand_row = row-1
                rand_col = col-1
            elif col+1 < 9 and row+1 < 9 and random_matrix[row+1][col+1] == bit:
                rand_row = row+1
                rand_col = col+1
            elif col-1 >= 0 and row+1 < 9 and random_matrix[row+1][col-1] == bit:
                rand_row = row+1
                rand_col = col-1
            elif col+1 < 9 and row-1 >= 0 and random_matrix[row-1][col+1] == bit:
                rand_row = row-1
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
    newimg.save("res.png")

def decode(seed):
    # decoding starts here
    random_matrix = generateRandomMatrix(seed)
    img = "res.png"
    image = Image.open(img, 'r')
    newimg = image.copy()
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
    print(text)

    cover = cv.imread("colorpic.png")
    stego = cv.imread("res.png")
    print("Peak signal to noise ratio : ", PSNR(cover,stego))
    print("Mean square Error : ",MSE(cover,stego))

encode(7)
decode(7)