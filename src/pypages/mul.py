from js import document, requestAnimationFrame, setInterval
import threading
from datetime import datetime
import math
from pyodide.ffi import create_proxy
import random

canvas = document.getElementById("my_canvas")
context = canvas.getContext("2d")

# 마우스 위치
mouse = {'x': 0, 'y': 0}

def move(e):
  mouse["x"] = e.offsetX
  mouse["y"] = e.offsetY

document.getElementById('body').addEventListener("mousemove", create_proxy(move))

# 존재하는 점들
points = []

class point:
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.vx = 0
    self.vy = 0
    self.ax = 0
    self.ay = 0
    self.m = 0.001; # mass
    self.f = 0.99;  # friction
    self.r = 10;    # radius
    self.c = "#000000" # color

    setInterval(create_proxy(self.move), 10)
  

  def set_acceleration(self, ax, ay):
    self.ax = ax
    self.ay = ay


  def increase_velocity(self, vx, vy):
    self.vx += vx
    self.vy += vy
  

  def set_color(self, c):
    self.c = c
  

  def move(self):
    self.vx += self.m * self.ax
    self.vy += self.m * self.ay

    self.vx *= self.f
    self.vy *= self.f

    self.x += self.vx
    self.y += self.vy


# draw
def draw(*e):
  canvas.width = canvas.width
  
  for p in points:
    p.set_acceleration(mouse["x"] - p.x, mouse["y"] - p.y)

    context.fillStyle = p.c
    context.beginPath()
    context.arc(p.x, p.y, p.r, 0, math.pi * 2, False)
    context.closePath()
    context.fill()


#make point
def mkpoint(e):
  points.append(point(mouse["x"], mouse["y"]))


document.getElementById('body').addEventListener("mousedown", create_proxy(mkpoint))

#explode
def explode(*e):
  for p in points:
    vx = (random.random() - 0.5)*20
    vy = random.random() * math.sqrt(100 - (vx ** 2))
    if random.random() > 0.5:
      vy *= -1
    
    p.increase_velocity(vx, vy)
    p.set_color("#" + hex(math.floor(random.random()*(0xffffff)))[2:])


document.getElementById('body').addEventListener("mousedown", create_proxy(explode))

def w_draw():
  requestAnimationFrame(create_proxy(draw))

setInterval(create_proxy(w_draw), 10)
setInterval(create_proxy(explode), 1500)