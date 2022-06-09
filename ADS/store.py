import random
import math
import numpy as np
import pandas as pd
from PIL import Image
import os
import cv2 as cv
from math import log10, sqrt
np.random.seed(7)

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

rows ,cols = np.shape(ar)
for i in ar:
    temp = []
    for j in range(len(i)*len(i)):
        temp.append(i[j%len(i)])
    random_matrix.append(temp)
random_matrix = np.array(random_matrix)
print(random_matrix)

img = "colorpic.png"
image = Image.open(img, 'r')
newimg = image.copy()
i_width, i_height = newimg.size

# secret = "this text will be encoded"
secret = " ABCDEFGHIJKL"
converted_secret = convert(secret)
print(converted_secret)


# Encoding starts here
index = 0
i = j = 0
p = q = 0
flag = False

data_len = 0
for i in range(len(converted_secret)):
    data_len += len(converted_secret[i])
        
index = 0
i = j = 0
converted_text = ''.join(map(str, converted_secret))

for i in range(i_height) :
    for j in range(i_width) :
        if index >= len(converted_text) :break
        cols = []
        bit = converted_text[index]
        index += 1
        rand_row = rand_col = None
        while len(cols) == 0:
            rand_row = random.randint(0,len(random_matrix)-1)
            # print(random_matrix[rand_row])
            cols = np.where(random_matrix[rand_row] == int(bit))[0]
        rand_col = random.choice(cols)
        r,g,b = newimg.getpixel((i,j))
        r1 = r
        g1 = g
        b1 = b
        g = str(g)
        b = str(b)
        g = int(g[:len(g)-1]+str(rand_row))
        b = int(b[:len(b)-1]+str(rand_col))
        # print(bit,"=",rand_row,rand_col,(r,g,b),(r1,g1,b1))
        newimg.putpixel((i,j),(r,g,b))

newimg.save("res.png")

index = 0
data = ""
# i = j = 0
print(converted_text)
for i in range(i_height):
    for j in range(i_width):
        if(index >=len(converted_text)) : break
        r,g,b = newimg.getpixel((i,j))
        # newimg.putpixel((i,j),(1,1,1))
        # print((g,b))
        row = str(g)[len(str(g)) - 1]
        col = str(b)[len(str(b)) - 1]
        # print(row,col)
        data = data + str(random_matrix[int(row)][int(col)])
        index += 1        
# print(data,len(data))

# # converting into base 10 
index = 0
text = ""
for i in range(0,len(data),3):
    num = data[i:i+3]
    num = toDeci(num,9)
    text += chr(num)
    # print(np.base_repr(int(num),10))
print(text,type(text))

cover = cv.imread("colorpic.png")
stego = cv.imread("result.png")
print(PSNR(cover,stego))