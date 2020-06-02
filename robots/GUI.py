import tkinter as tk

from setting import (
    MAP_SIZE,
)

ZOOM_SIZE=5 # 地图缩放倍率

def BeginSim():
    '''将主函数移植进来'''
    explore_map=[0,0,0,0,1,1,1,1,1,1,1]
    barrier_map=[0,0,0,0,0,0,0,1,1,0,0] # just a example
    for i in range(0,len(explore_map)):
        if explore_map[i]==1:
            if barrier_map[i]==1:
                canvas.create_rectangle(ZOOM_SIZE*i//MAP_SIZE[0],ZOOM_SIZE*i%MAP_SIZE[1],ZOOM_SIZE*i//MAP_SIZE[0]+ZOOM_SIZE,ZOOM_SIZE*i%MAP_SIZE[1]+ZOOM_SIZE,fill='white')
            else:
                canvas.create_rectangle(ZOOM_SIZE*i//MAP_SIZE[0],ZOOM_SIZE*i%MAP_SIZE[1],ZOOM_SIZE*i//MAP_SIZE[0]+ZOOM_SIZE,ZOOM_SIZE*i%MAP_SIZE[1]+ZOOM_SIZE,fill='black')



MainWindow=tk.Tk()
MainWindow.title('Demo')
MainWindow.geometry('1200x900')

B=tk.Button(MainWindow,text='Begin Simulating',font=('Arial',12),width=15,height=1,command=BeginSim)
B.pack()

canvas=tk.Canvas(MainWindow,width=MAP_SIZE[0]*ZOOM_SIZE,height=MAP_SIZE[1]*ZOOM_SIZE)
for i in range(0,MAP_SIZE[0]):
    for j in range(0,MAP_SIZE[1]):
        canvas.create_rectangle(ZOOM_SIZE*i,ZOOM_SIZE*j,ZOOM_SIZE*(i+1),ZOOM_SIZE*(j+1),fill='blue')
canvas.pack()

MainWindow.mainloop()