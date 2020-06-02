import tkinter as tk

from robots.setting import MAP_SIZE, ZOOM_SIZE
import robots


def get_rectangle_loc(x: int, y: int):
    return ZOOM_SIZE * x, ZOOM_SIZE * y, ZOOM_SIZE * (x + 1), ZOOM_SIZE * (y + 1)


window = tk.Tk()
window.title('Demo')
window.geometry('1200x900')

canvas = tk.Canvas(window, width=MAP_SIZE[0] * ZOOM_SIZE, height=MAP_SIZE[1] * ZOOM_SIZE)
for i in range(0, MAP_SIZE[0]):
    for j in range(0, MAP_SIZE[1]):
        if robots.barrier_map[i, j]:
            canvas.create_rectangle(*get_rectangle_loc(i, j), fill='black')
        else:
            canvas.create_rectangle(*get_rectangle_loc(i, j), fill='gray')

for bot in robots.robots_list:
    canvas.create_rectangle(*get_rectangle_loc(*bot.loc()), fill='green')

canvas.pack()

# B = tk.Button(window, text='Begin Simulating', font=('Arial', 12), width=15, height=1, command=begin_sim)
# B.pack()

window.mainloop()
