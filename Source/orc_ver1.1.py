import pyautogui
import tkinter as tk
from PIL import Image
import pyocr
import os
import numpy as np
import keyboard
import pyperclip
from pystray import Icon as icon, Menu as menu, MenuItem as item

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
   img3=Image.new('RGB',size)

   """轉灰階"""
   for x in range(size[0]):
      for y in range(size[1]):
         r,g,b=img.getpixel((x,y))
         gray = (r*30+g*59+b*11+50)//100
         img2.putpixel((x,y),(gray,gray,gray))
         if gray < border:
             gray = 0
         else:
             gray = 255
         img3.putpixel((x,y),(gray,gray,gray))

   img2.save('temp2.png')
   img3.save('temp3.png')
   
   builder = pyocr.builders.TextBuilder(tesseract_layout=6)
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

   if event.x+120 > root.winfo_screenwidth() or event.y+100 > root.winfo_screenheight():
      slider.geometry('120x100+{0}+{1}'.format(xstart-120, ystart-100))
   else:
      slider.geometry('120x100+{0}+{1}'.format(event.x, event.y))
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
   rec = cv.create_rectangle(0,0,0,0,outline = 'white')

def change_border(event):
   global border
   border = s.get()
   #print(border)

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
   s = tk.Scale(slider, from_=20, to=240,orient="horizontal",command = change_border)
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
   border=180
   
   keyboard.add_hotkey('shift+esc', exitp)
   keyboard.add_hotkey('print screen', creat)
   
   ico=Image.open("icon.ico")
   icon('orc', ico, menu=menu(item('exit',exitp))).run()
   
   keyboard.wait()
   
if __name__ == "__main__":
   main()

