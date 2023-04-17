from js import document, window, setInterval, requestAnimationFrame
from pyodide.ffi import create_proxy
import math
import random

class Circle:
  def __init__(self, x, y, radius) -> None:
    self.x = x
    self.y = y
    self.radius = radius
    self.color = '#87CEFA'

  def animate(self, ctx):
    ctx.fillStyle = self.color
    ctx.beginPath()
    ctx.arc(self.x, self.y, self.radius, 0, math.pi * 2, False)
    ctx.fill()
    ctx.closePath()

class Plane:
  def __init__(self, x, y, z, size, radius) -> None:
    self.x = x
    self.y = y
    self.z = z
    self.size = size
    self.radius = radius

    self.circle = Circle(self.x, self.y, math.sqrt(self.radius ** 2 - self.z ** 2) if self.radius ** 2 - self.z ** 2 > 0 else 0)
  
  def animate(self, ctx):
    # js.console.log(1)
    # ctx.save()
    ctx.strokeStyle = '#aaaaaa'
    ctx.lineWidth = 2
    ctx.beginPath()

    for i in range(11):
      X = self.x - self.size + (self.size * i / 5)

      ctx.moveTo(X, self.y - self.size)
      ctx.lineTo(X, self.y + self.size)
      
    for i in range(11):
      Y = self.y - self.size + (self.size * i / 5)

      ctx.moveTo(self.x - self.size, Y)
      ctx.lineTo(self.x + self.size, Y)
    
    ctx.stroke()
    ctx.closePath()

    self.circle.animate(ctx)

class Z_text:
  def __init__(self, z, r, x1, x2, y) -> None:
    self.z = z
    self.r = r
    self.x1 = x1
    self.x2 = x2
    self.y = y
  
  def animate(self, ctx):
    ctx.font = '20px Verdana'
    ctx.fillStyle = '#000000'
    ctx.fillText(f'Z-axis spacing: {self.z:.2f}, radius: {self.r:.2f}', self.x1, self.y)

class Moveplane:
  def __init__(self, mid, x, y, z, size, radius) -> None:
    self.mid = mid
    self.x = x
    self.y = y + size * 2 + 30
    self.z = z * (self.mid - self.x) * 0.9
    self.size = size
    self.radius = radius
    
    self.circle = Circle(self.x, self.y, math.sqrt(self.radius ** 2 - self.z ** 2) if self.radius ** 2 - self.z ** 2 > 0 else 0)
  
  def animate(self, ctx):
    ctx.strokeStyle = '#bbbbbb'
    ctx.lineWidth = 2
    ctx.beginPath()

    for i in range(11):
      X = self.x - self.size + (self.size * i / 5)

      ctx.moveTo(X, self.y - self.size)
      ctx.lineTo(X, self.y + self.size)
      
    for i in range(11):
      Y = self.y - self.size + (self.size * i / 5)

      ctx.moveTo(self.x - self.size, Y)
      ctx.lineTo(self.x + self.size, Y)
    
    ctx.stroke()
    ctx.closePath()

    self.circle.animate(ctx)

class Planes:
  def __init__(self, x, y, plane_num, circle_radius_Ratio, idxRatio, moveplaneX) -> None:
    self.x = x
    self.y = y
    self.plane_num = plane_num * 2 + 1
    self.idxRatio = idxRatio

    self.moveplaneX = moveplaneX

    self.planes = []

    size_plus_inter = x / self.plane_num
    size = size_plus_inter * 0.9
    z = size_plus_inter * idxRatio

    self.size = size

    self.circle_radius = size * circle_radius_Ratio

    self.txt = Z_text(z, self.circle_radius, self.x - (size_plus_inter*2), self.x, min(self.y - size_plus_inter, self.y - self.circle_radius - 10))

    for i in range(self.plane_num):
      idx = (math.floor(self.plane_num / 2)) - i
      # js.console.log(idx)
      
      self.planes.append(Plane(self.x - (size_plus_inter * 2 * idx), self.y, idx*z, size, self.circle_radius))
    
    self.moveplane = Moveplane(self.x, self.moveplaneX, self.y, self.idxRatio/2, size, self.circle_radius)
  
  def animate(self, ctx):
    # self.moveplane = Moveplane(self.x, self.moveplaneX, self.y, self.idxRatio/2, self.size, self.circle_radius)
    for p in self.planes:
      p.animate(ctx)
    
    self.txt.animate(ctx)
    self.moveplane.animate(ctx)

class App:
  def __init__(self) -> None:
    self.canvas = document.createElement("canvas")
    document.body.appendChild(self.canvas)
    self.ctx = self.canvas.getContext("2d")

    self.pixelRatio = 2 if window.devicePixelRatio > 1 else 1

    self.idxRatio = 0.4
    self.circle_radius_Ratio = 1

    self.moveplaneX = document.body.clientWidth / 2 + 30

    self.planes_num = 2

    window.addEventListener("resize", create_proxy(self.resize), False)
    self.resize()

    self.isDown = False

    document.addEventListener('mousedown', create_proxy(self.ondown), False)
    document.addEventListener('mousemove', create_proxy(self.onmove), False)
    document.addEventListener('mouseup', create_proxy(self.onup), False)

    document.addEventListener('keydown', create_proxy(self.onkeydown), False)

    window.requestAnimationFrame(create_proxy(self.animate))

  def resize(self, *e):
    self.stageWidth = document.body.clientWidth
    self.stageHeight = document.body.clientHeight

    self.canvas.width = self.stageWidth * self.pixelRatio
    self.canvas.height = self.stageHeight * self.pixelRatio
    self.ctx.scale(self.pixelRatio, self.pixelRatio)

    # self.circle = Circle(self.stageWidth / 2, self.stageHeight / 2, 100)
    # self.plane = Plane(self.stageWidth / 2, self.stageHeight / 2, 0, 150, 100)
    self.planes = Planes(self.stageWidth/2, self.stageHeight/3, self.planes_num, self.circle_radius_Ratio, self.idxRatio, self.moveplaneX)

  def animate(self, e):
    window.requestAnimationFrame(create_proxy(self.animate))

    self.ctx.clearRect(0, 0, self.stageWidth, self.stageHeight)

    # self.circle.animate(self.ctx)
    self.planes.animate(self.ctx)
  
  def ondown(self, e):
    self.isDown = True
    self.moveplaneX = e.clientX
    js.console.log(self.moveplaneX)
    self.resize()

  def onmove(self, e):
    if self.isDown:
      self.moveplaneX = e.clientX
      self.resize()
  
  def onup(self, e):
    self.isDown = False
  
  def onkeydown(self, e):
    if e.keyCode == 38:
      self.circle_radius_Ratio += 0.02
    
    if e.keyCode == 40:
      self.circle_radius_Ratio -= 0.02
      
    if e.keyCode == 39:
      self.idxRatio += 0.02
    
    if e.keyCode == 37:
      self.idxRatio -= 0.02
    
    if e.keyCode == 32:
      self.planes_num += 1
      if self.planes_num > 4:
        self.planes_num = 2
    
    self.resize()

    
App()
