from js import document, window, setInterval, requestAnimationFrame
from pyodide.ffi import create_proxy
import math
import random
mouse = {'x': -1, 'y': -1}


class Wave:
  def __init__(self, x, y) -> None:
    self.x = x
    self.y = y
    self.radius = 10
    self.r = math.floor(random.random()*(0xff))
    self.g = math.floor(random.random()*(0xff))
    self.b = math.floor(random.random()*(0xff))
    self.a = 1
  
  def draw(self, ctx):
    self.radius += 0.5
    self.a -= 0.001

    ctx.beginPath()

    g = ctx.createRadialGradient(
      self.x,
      self.y,
      self.radius * 0.01,
      self.x,
      self.y,
      self.radius
    )
    g.addColorStop(0, f'rgba({self.r}, {self.g}, {self.b}, 0)')
    # g.addColorStop(0.7, f'rgba({self.r}, {self.g}, {self.b}, 0)')
    g.addColorStop((self.radius - 4)/self.radius, f'rgba({self.r}, {self.g}, {self.b}, 0)')
    g.addColorStop((self.radius - 2)/self.radius, f'rgba({self.r}, {self.g}, {self.b}, {self.a})')
    g.addColorStop(1, f'rgba({self.r}, {self.g}, {self.b}, 0)')

    ctx.fillStyle = g
    ctx.arc(self.x, self.y, self.radius, 0, math.pi * 2, False)
    ctx.fill()


  
  

class App:
  def __init__(self) -> None:
    self.canvas = document.getElementById('my_canvas')
    self.ctx = self.canvas.getContext('2d')
    self.body = document.getElementById('body')
    Element('body').add_class('bcolor')

    self.stageWidth = self.canvas.clientWidth
    self.stageHeight = self.canvas.clientHeight

    # self.Wave = Wave(self.stageWidth / 2, self.stageHeight / 2)
    self.Waves = []
    self.body.addEventListener("mousedown", create_proxy(self.addWave))
    
    setInterval(create_proxy(self.animate), 10)

  def draw_wrapper(self, *e):
    self.canvas.width = self.canvas.width
    # self.Wave.draw(self.ctx)
    for i in range(len(self.Waves)-1, -1, -1):
      self.Waves[i].draw(self.ctx)
      if self.Waves[i].a <= 0:
        del self.Waves[i]

  def animate(self):
    window.requestAnimationFrame(create_proxy(self.draw_wrapper), 20)

  def addWave(self, *e):
    self.Waves.append(Wave(mouse['x'], mouse['y']))


def move(e):
  mouse["x"] = e.offsetX
  mouse["y"] = e.offsetY

document.getElementById('body').addEventListener("mousemove", create_proxy(move))

App()