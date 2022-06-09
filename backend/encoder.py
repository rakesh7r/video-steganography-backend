import cv2 as cv
import numpy as np
from PIL import Image
import random

def encrypt(text): 
  # returning just binary data, Encryption not implemented yet
  return ''.join(format(ord(i), '08b') for i in text)

def encode(newimg,binData,length):     
  bindataindex = 0
  width, height = newimg.size
  newimg.putpixel((width-1,height-1), (len(binData), 0, 0))
  for i in range(width):
      for j in range(height):
          if bindataindex >= len(binData):break
          r,g,b = newimg.getpixel((i, j))
          r = str(np.binary_repr(r, width=8))
          g = str(np.binary_repr(g, width=8))
          b = str(np.binary_repr(b, width=8))
          r = r[:7] + str(binData[bindataindex])
          bindataindex += 1
          if bindataindex >= len(binData):break
          g = g[:7] + str(binData[bindataindex])
          bindataindex += 1
          if bindataindex >= len(binData):break
          b = b[:7] + str(binData[bindataindex])
          bindataindex += 1
          if bindataindex >= len(binData):break
          newimg.putpixel((i, j), (int(r, 2), int(g, 2), int(b, 2)))
          if(i == width-1 and j == height-1):
              break
      if bindataindex >= len(binData): break
  return newimg

def decode(newimg) :
  width, height = newimg.size

  datalen = newimg.getpixel((width-1,height-1))[0]
  index = 0
  data = ""

  for i in range(width):
      for j in range(height):
          r,g,b = newimg.getpixel((i, j))
          r = str(np.binary_repr(r, width=8))
          g = str(np.binary_repr(g, width=8))
          b = str(np.binary_repr(b, width=8))
          data += r[7]
          if len(data) >= datalen: break
          data +=g[7]
          if len(data) >= datalen: break
          data +=b[7]
          if len(data) >= datalen: break
      if len(data) == datalen : break
  temp_data = ""
  text = ""
  for i in range(len(data)):
      temp_data += data[i]
      if len(temp_data) == 8 :
          text+= chr(int(temp_data,2))
          temp_data = ""
  return text[0:len(text)-1]

vid = cv.VideoCapture('input.mp4')
total_frames = last_frame_number =  vid.get(cv.CAP_PROP_FRAME_COUNT)
print("Total number of frames : ",last_frame_number)

count = 0
# starting_frame = random.randint(1,150)
starting_frame = 1
text = input("Enter Text to be transmitted: ")
if len(text) == 0: 
    raise Exception('Data is empty')
  
text +=  "0"
enc_data = encrypt(text)

vid.set(1,starting_frame)

ret, frame = vid.read()
img_pil = Image.fromarray(frame)
new_img = encode(img_pil,enc_data,len(enc_data))
new_cv_img = np.asarray(new_img)

gray = cv.cvtColor(new_cv_img, cv.IMREAD_COLOR)
gray = Image.fromarray(gray)
gray.save("gray.jpg")


# inserting editted frame number into the last frame of the video
vid.set(1,last_frame_number-1)
ret, frame = vid.read()

img_pil = Image.fromarray(frame)
width, height = img_pil.size
video_fps = vid.get(cv.CAP_PROP_FPS),

r,g,b =img_pil.getpixel((width-1, height-1)) 
print(r,g,b)
img_pil.putpixel((width-1, height-1),(r,g,starting_frame))
r,g,b =img_pil.getpixel((width-1, height-1)) 
print(r,g,b)


fourcc = cv.VideoWriter_fourcc(*'avc1')
writer = cv.VideoWriter("output.mp4", apiPreference=0, fourcc=fourcc,fps=video_fps[0], frameSize=(width, height))

frame_number = -1
while(True):
    frame_number += 1
    vid.set(1,frame_number)
    ret, frame = vid.read()
    if not ret : break  
    if frame_number >= last_frame_number: break
    if frame_number > 10 and frame_number < 100 :
      frame = new_cv_img
    writer.write(frame)

    # frame = np.asarray(frame)
    gray = cv.cvtColor(frame, cv.IMREAD_COLOR)
    # cv.imshow('frame',gray)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

vid.release()
writer.release()
cv.destroyAllWindows()

















# while(vid.isOpened()):
#   ret, frame = vid.read()
#   # if(count == starting_frame): 
#     # write the frame
#   if ret == True:
#     count += 1
#     # print(frame[2,2])
#     # cv.imshow('Frame',frame)      
#     if cv.waitKey(25) & 0xFF == ord('q'):
#       break
#   else:
#     break
  
# vid.release()
# vid.destroyAllWindows()