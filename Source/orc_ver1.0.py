import pyautogui
import tkinter as tk
from PIL import Image
import pyocr
import os
import cv2
import numpy as np
import keyboard
import pyperclip
from pystray import Icon as icon, Menu as menu, MenuItem as item

def fill_color(image):
   copyImg = image.copy()
   h,w = image.shape[:2]
   mask = np.zeros([h+2,w+2],np.uint8)
   
   #cv2.floodFill(copyImg,mask,(5,5),(0,0,0),(10,10,10),(10,10,10),cv2.FLOODFILL_FIXED_RANGE)
   copyImg = 255 - copyImg
   cv2.imwrite('temp3.png',copyImg)
   copyImg = Image.fromarray(cv2.cvtColor(copyImg,cv2.COLOR_BGR2RGB))  
   return copyImg

def OCR():
   path='C:\\Program Files\\Tesseract-OCR'
   os.environ['PATH'] += os.pathsep + path
   tools = pyocr.get_available_tools()
   pyocr.tesseract.TESSERACT_CMD = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   #print(tools[0].get_name())
   tool = tools[0]

   img = Image.open("temp.png")
   
   img=img.convert('RGB')
   size=img.size
   img2=Image.new('RGB',size)

   """轉灰階"""
   for x in range(size[0]):
      for y in range(size[1]):
         r,g,b=img.getpixel((x,y))
         #print(r,g,b)
         if r > border and g > border and b > border:
            r = 255
            g = 255
            b = 255
         else:
            r = 0
            g = 0
            b = 0
         img2.putpixel((x,y),(r,g,b))
         
   img.putpixel((0,0),(122,122,122))
   img2.save('temp2.png')

   img3 = cv2.cvtColor(np.asarray(img2),cv2.COLOR_RGB2BGR)  
   img3 = fill_color(img3)
   """ 字是黑的 用 img2 border = 130 字是黑的 用 img3 border = 240"""
   builder = pyocr.builders.TextBuilder(tesseract_layout=6)
   if border <= 180 :
      text = tool.image_to_string(img2, lang="jpn", builder=builder)
   else:
      text = tool.image_to_string(img3, lang="jpn", builder=builder)
   print(text.replace(' ',''))
   pyperclip.copy(text.replace(' ',''))

def sys_out(even):
   slider.destroy()
   root.destroy()

def button_3(event):
   global xstart,ystart,xend,yend
   cv.delete(rec)
   cv.place_forget()
   img = pyautogui.screenshot(region=[xstart,ystart,xend-xstart,yend-ystart]) # x,y,w,h
   img.save('temp.png')
   OCR()
   sys_out(None)

def buttonRelease_1(event):
   global xend,yend
   xend, yend = event.x, event.y

def b1_Motion(event):
   global x, y,xstart,ystart,slider
   x, y = event.x, event.y
   #print("event.x, event.y = ", event.x, event.y)
   cv.configure(height = event.y - ystart)
   cv.configure(width = event.x - xstart)
   cv.coords(rec,0,0,event.x-xstart,event.y-ystart)

   slider.geometry('120x40+{0}+{1}'.format(event.x+2, event.y+2))
   slider.lift()
   border = s.get()

def button_1(event):
   global x, y ,xstart,ystart
   global rec
   x, y = event.x, event.y
   xstart,ystart = event.x, event.y
   #print("event.x, event.y = ", event.x, event.y)
   xstart,ystart = event.x, event.y  
   cv.configure(height=1)
   cv.configure(width=1)
   cv.config(highlightthickness=0)
   cv.place(x=event.x, y=event.y)
   rec = cv.create_rectangle(0,0,0,0)

def change_border(event):
   global border
   border = s.get()
   print(border)

def creat():
   global root
   root = tk.Tk()
   root.overrideredirect(True)
   root.attributes("-alpha", 0.5)
   root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
   root.configure(bg="black")
   root.attributes('-transparentcolor','white')
   root.attributes('-topmost', True)
   
   global cv
   cv = tk.Canvas(root,bg = 'white')
   x, y = 0, 0
   xstart,ystart = 0 ,0
   xend,yend = 0, 0
   rec = ''

   global slider,s
   slider = tk.Tk()
   slider.overrideredirect(True)#60 240
   s = tk.Scale(slider, from_=60, to=240,orient="horizontal",command = change_border)
   s.set(border)
   s.pack()
   slider.attributes('-topmost', True)
   try:
      slider.bind('<Escape>',sys_out)
   except:
      pass
   
   root.bind('<Escape>',sys_out)
   root.bind("<Button-1>", button_1)
   root.bind("<B1-Motion>", b1_Motion)
   root.bind("<ButtonRelease-1>", buttonRelease_1)
   root.bind("<Button-3>",button_3)
   root.lift()
   root.mainloop()

def exitp():
   os._exit(0)
   
def main():
   global border
   border=200
   
   keyboard.add_hotkey('shift+esc', exitp)
   keyboard.add_hotkey('print screen', creat)
   
   ico=Image.open("icon.ico")
   icon('orc', ico, menu=menu(item('exit',exitp))).run()
   
   keyboard.wait()
   
if __name__ == "__main__":
   main()

