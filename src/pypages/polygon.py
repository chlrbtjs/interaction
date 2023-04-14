from js import document, window, setInterval, requestAnimationFrame
from pyodide.ffi import create_proxy
import math
import random

PI2 = math.pi * 2

class Polygon:
  def __init__(self, x, y, radius, sides) -> None:
    self.x = x
    self.y = y
    self.radius = radius
    self.sides = sides
    self.rotate = 0
  
  def animate(self, ctx, moveX, mode):
    if mode == 0:
      ctx.save()
      ctx.fillStyle = '#000'
      # ctx.beginPath()

      angle = PI2 / self.sides
      angle2 = PI2 / 4

      ctx.translate(self.x, self.y)

      self.rotate -= moveX * 0.008
      ctx.rotate(self.rotate)

      for i in range(self.sides):
        x = self.radius * math.cos(angle * i)
        y = self.radius * math.sin(angle * i)

        # if i == 0:
        #   ctx.moveTo(x, y)
        # else:
        #   ctx.lineTo(x, y)

        # ctx.beginPath()
        # ctx.arc(x, y, 30, 0, PI2, False)
        # ctx.fill()

        ctx.save()
        ctx.translate(x, y)
        ctx.rotate(((360 / self.sides) * i + 45) * math.pi / 180)
        ctx.beginPath()
        for j in range(4):
          x2 = 60 * math.cos(angle2 * j)
          y2 = 60 * math.sin(angle2 * j)

          if j == 0:
            ctx.moveTo(x2, y2)
          else:
            ctx.lineTo(x2, y2)
          
        ctx.fill()
        ctx.closePath()
        ctx.restore()
      
      # ctx.fill()
      # ctx.closePath()
      ctx.restore()
    elif mode == 1:
      ctx.save()
      ctx.fillStyle = '#000'
      ctx.beginPath()

      angle = PI2 / self.sides
      angle2 = PI2 / 4

      ctx.translate(self.x, self.y)

      self.rotate -= moveX * 0.008
      ctx.rotate(self.rotate)

      for i in range(self.sides):
        x = self.radius * math.cos(angle * i)
        y = self.radius * math.sin(angle * i)

        if i == 0:
          ctx.moveTo(x, y)
        else:
          ctx.lineTo(x, y)

        # ctx.beginPath()
        # ctx.arc(x, y, 30, 0, PI2, False)
        # ctx.fill()

        # ctx.save()
        # ctx.translate(x, y)
        # ctx.rotate(((360 / self.sides) * i + 45) * math.pi / 180)
        # ctx.beginPath()
        # for j in range(4):
        #   x2 = 60 * math.cos(angle2 * j)
        #   y2 = 60 * math.sin(angle2 * j)

        #   if j == 0:
        #     ctx.moveTo(x2, y2)
        #   else:
        #     ctx.lineTo(x2, y2)
          
        # ctx.fill()
        # ctx.closePath()
        # ctx.restore()
      
      ctx.fill()
      ctx.closePath()
      ctx.restore()
    else:
      ctx.save()
      ctx.fillStyle = '#000'
      # ctx.beginPath()

      angle = PI2 / self.sides
      angle2 = PI2 / 4

      ctx.translate(self.x, self.y)

      self.rotate -= moveX * 0.008
      ctx.rotate(self.rotate)

      for i in range(self.sides):
        x = self.radius * math.cos(angle * i)
        y = self.radius * math.sin(angle * i)

        # if i == 0:
        #   ctx.moveTo(x, y)
        # else:
        #   ctx.lineTo(x, y)

        ctx.beginPath()
        ctx.arc(x, y, 30, 0, PI2, False)
        ctx.fill()

        # ctx.save()
        # ctx.translate(x, y)
        # ctx.rotate(((360 / self.sides) * i + 45) * math.pi / 180)
        # ctx.beginPath()
        # for j in range(4):
        #   x2 = 60 * math.cos(angle2 * j)
        #   y2 = 60 * math.sin(angle2 * j)

        #   if j == 0:
        #     ctx.moveTo(x2, y2)
        #   else:
        #     ctx.lineTo(x2, y2)
          
        # ctx.fill()
        # ctx.closePath()
        # ctx.restore()
      
      # ctx.fill()
      ctx.closePath()
      ctx.restore()


class App:
  def __init__(self) -> None:
    self.canvas = document.createElement("canvas")
    document.body.appendChild(self.canvas)
    self.ctx = self.canvas.getContext("2d")

    self.pixelRatio = 2 if window.devicePixelRatio > 1 else 1

    self.sides = 3
    self.mode = 0

    window.addEventListener("resize", create_proxy(self.resize), False)
    self.resize()

    self.isDown = False
    self.moveX = 0
    self.offsetX = 0

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

    self.polygon = Polygon(self.stageWidth / 2, self.stageHeight / 2, self.stageHeight / 3, self.sides)

  def animate(self, e):
    window.requestAnimationFrame(create_proxy(self.animate))

    self.ctx.clearRect(0, 0, self.stageWidth, self.stageHeight)

    self.moveX *= 0.92

    self.polygon.animate(self.ctx, self.moveX, self.mode)
  
  def ondown(self, e):
    self.isDown = True
    self.moveX = 0
    self.offsetX = e.clientX

  def onmove(self, e):
    if self.isDown:
      if e.clientY < self.stageHeight / 2:
        self.moveX = -e.clientX + self.offsetX
        self.offsetX = e.clientX
      else:
        self.moveX = e.clientX - self.offsetX
        self.offsetX = e.clientX

  def onup(self, e):
    self.isDown = False

  def onkeydown(self, e):
    if e.keyCode == 32:
      self.sides = self.sides + 1
      if self.sides > 12:
        self.sides = 3
      
      self.polygon = Polygon(self.stageWidth / 2, self.stageHeight / 2, self.stageHeight / 3, self.sides)
    elif e.keyCode == 13:
      self.mode = self.mode + 1
      if self.mode > 2:
        self.mode = 0
      
      self.polygon = Polygon(self.stageWidth / 2, self.stageHeight / 2, self.stageHeight / 3, self.sides)

    
App()
