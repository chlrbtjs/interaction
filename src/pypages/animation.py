from js import document, setInterval, clearInterval
from pyodide.ffi import create_proxy
import math
import threading


canvas = document.getElementById("my_canvas")
context = canvas.getContext("2d")

point = {
  'x': 0,
  'y': 0,
  'vx': 0,
  'vy': 0,
  'k': 0.001,
  'r': 10,
  'color': '#000000'
}

mouse = {
  'x': 0,
  'y': 0,
}

def draw():
  canvas.width = canvas.width

  point['vx'] += point['k']*(mouse['x'] - point['x'])
  point['vy'] += point['k']*(mouse['y'] - point['y'])

  point['vx'] *= 0.99
  point['vy'] *= 0.99

  point['x'] += point['vx']
  point['y'] += point['vy']
  
  context.fillStyle = point['color']
  context.beginPath()
  context.arc(point['x'], point['y'], point['r'], 0, math.pi * 2, False)
  context.closePath()
  context.fill()


def move(e):
  mouse['x'] = e.offsetX
  mouse['y'] = e.offsetY


def down(e):
  point['r'] = 30
  point['color'] = "#ff0000"


def up(e):
  point['r'] = 10
  point['color'] = "#000000"


document.getElementById('body').addEventListener("mousemove", create_proxy(move))
document.getElementById('body').addEventListener("mousedown", create_proxy(down))
document.getElementById('body').addEventListener("mouseup", create_proxy(up))

print(point['color'])
setInterval(create_proxy(draw), 10)
