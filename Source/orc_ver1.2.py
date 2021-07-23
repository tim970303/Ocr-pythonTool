import pyautogui
import tkinter as tk
from PIL import Image,ImageTk
import pyocr
import os
import numpy as np
import keyboard
import pyperclip
import configparser

def gray_scale():
   global screen_shot
   size = screen_shot.size
   #imgG = Image.new('RGB',size)
   imgB = Image.new('RGB',size)

   for x in range(size[0]):
      for y in range(size[1]):
         r,g,b=screen_shot.getpixel((x,y))
         gray = (r*30+g*59+b*11+50)//100
         #imgG.putpixel((x,y),(gray,gray,gray))
         if gray < border:
             gray = 0
         else:
             gray = 255
         imgB.putpixel((x,y),(gray,gray,gray))
   return imgB

def OCR():
   global lenguage,path,layout
   os.environ['PATH'] += os.pathsep + path
   tools = pyocr.get_available_tools()
   pyocr.tesseract.TESSERACT_CMD = path+'\\tesseract.exe'
   #print(tools[0].get_name())
   tool = tools[0]

   img = gray_scale()
   
   builder = pyocr.builders.TextBuilder(tesseract_layout=layout)
   text = tool.image_to_string(img, lang=lenguage, builder=builder)
   print(text)
   pyperclip.copy(text.replace(' ',''))

def sleep(even):
   toolBox.destroy()
   root.destroy()

def R_button_on_click(event):
   global xstart,ystart,xend,yend
   cv.delete(rec)
   cv.place_forget()
   OCR()
   sleep(None)

def L_button_Release(event):
   global xend,yend,preview,preview_item,newpreview,screen_shot
   xend, yend = event.x, event.y
   screen_shot = pyautogui.screenshot(region=[xstart,ystart,xend-xstart,yend-ystart])
   newpreview = ImageTk.PhotoImage(gray_scale())
   preview.itemconfig(preview_item,image=newpreview)

def L_button_Motion(event):
   global x, y,xstart,ystart,toolBox,root,scale,border
   x, y = event.x, event.y
   #print("event.x, event.y = ", event.x, event.y)
   cv.configure(height = event.y - ystart)
   cv.configure(width = event.x - xstart)
   cv.coords(rec,0,0,event.x-xstart,event.y-ystart)

   if event.x+120 > root.winfo_screenwidth() or event.y+100 > root.winfo_screenheight():
      toolBox.geometry('120x100+{0}+{1}'.format(xstart-120, ystart-100))
   else:
      toolBox.geometry('120x100+{0}+{1}'.format(event.x, event.y))
   toolBox.lift()
   border = scale.get()

def L_button_on_click(event):
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
   global border,newpreview,preview,preview_item,scale
   border = scale.get()
   #print(border)
   newpreview = ImageTk.PhotoImage(gray_scale())
   preview.itemconfig(preview_item,image=newpreview)

def preview_click(event):
   global preview_lastx,preview_lasty,preview,preview_item
   preview_lastx = event.x
   preview_lasty = event.y
   
def preview_drag(event):
   global preview,preview_item,preview_lastx,preview_lasty
   preview.move(preview_item,event.x - preview_lastx, event.y - preview_lasty)
   preview_lastx = event.x
   preview_lasty = event.y
   
def creat():
   global border_max,border_min,toolbox_h,toolbox_w
   
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

   global toolBox,scale,preview,preview_item
   toolBox = tk.Toplevel()
   toolBox.overrideredirect(True)

   preview = tk.Canvas(toolBox, height=toolbox_h, width=toolbox_w)
   preview_img = ImageTk.PhotoImage(Image.open("temp.png"))
   preview_item = preview.create_image(preview_img.width()/2, preview_img.height()/2, anchor="center", image=preview_img)
   preview.bind('<Button-1>',preview_click)
   preview.bind('<B1-Motion>',preview_drag)
   preview.pack()
   
   scale = tk.Scale(toolBox, from_ = border_min, to = border_max,orient="horizontal")
   scale.set(border)
   scale.pack()
   
   toolBox.attributes('-topmost', True)
   try:
      toolBox.bind('<Escape>',sleep)
      toolBox.bind('<ButtonRelease-1>',change_border)
   except:
      pass
   
   root.bind('<Escape>',sleep)
   root.bind("<Button-1>", L_button_on_click)
   root.bind("<B1-Motion>", L_button_Motion)
   root.bind("<ButtonRelease-1>", L_button_Release)
   root.bind("<Button-3>",R_button_on_click)
   root.lift()
   root.mainloop()
   
def exit_p():
   os._exit(0)
   
def main():
   global border,border_max,border_min,toolbox_h,toolbox_w,lenguage,path,layout
   config = configparser.ConfigParser()
   config.read('config.ini')
   
   border = int(config['border']['border_value'])
   border_max = int(config['border']['border_max'])
   border_min = int(config['border']['border_min'])
   toolbox_h = int(config['toolbox']['height'])
   toolbox_w = int(config['toolbox']['width'])
   lenguage = config['lenguage']['code']
   path = config['engine']['path']
   layout = int(config['engine']['layout'])
   
   #print(lenguage)
   keyboard.add_hotkey('shift+esc', exit_p)
   keyboard.add_hotkey('print screen', creat)

   keyboard.wait()
   
if __name__ == "__main__":
   main()

