from js import document, window, setInterval, requestAnimationFrame
from pyodide.ffi import create_proxy
import threading
import math
import random

class Ball:
  def __init__(self, stageWidth, stageHeight, radius, speed) -> None:
    self.radius = radius
    self.vx = speed
    self.vy = speed

    diameter = self.radius * 2
    self.x = diameter + (random.random() * stageWidth - diameter)
    self.y = diameter + (random.random() * stageHeight- diameter)
  
  def draw(self, ctx, stageWidth, stageHeight, block):
    self.x += self.vx
    self.y += self.vy

    self.bounceWindow(stageWidth, stageHeight)
    self.bounceBlock(block)

    ctx.fillStyle = '#fdd700'
    ctx.beginPath()
    ctx.arc(self.x, self.y, self.radius, 0, math.pi * 2, False)
    ctx.fill()
  
  def bounceWindow(self, stageWidth, stageHeight):
    minX = self.radius
    maxX = stageWidth - self.radius
    minY = self.radius
    maxY = stageHeight - self.radius

    if self.x <= minX or self.x >= maxX:
      self.vx *= -1
      self.x += self.vx
    elif self.y <= minY or self.y >= maxY:
      self.vy *= -1
      self.y += self.vy
    
  def bounceBlock(self, block):
    minX = block.x - self.radius
    maxX = block.maxX + self.radius
    minY = block.y - self.radius
    maxY = block.maxY + self.radius

    if minX < self.x < maxX and minY < self.y < maxY:
      x1 = abs(minX - self.x)
      x2 = abs(self.x - maxX)
      y1 = abs(minY - self.y)
      y2 = abs(self.y - maxY)
      min1 = min(x1, x2)
      min2 = min(y1, y2)
      min3 = min(min1, min2)

      if min3 == min1:
        self.vx *= -1
        self.x += self.vx
      elif min3 == min2:
        self.vy *= -1
        self.y += self.vy
      


class Block:
  def __init__(self, width, height, x, y) -> None:
    self.width = width
    self.height = height
    self.x = x
    self.y = y
    self.maxX = x + width
    self.maxY = y + height
  
  def draw(self, ctx):
    xGap = 80
    yGap = 60

    ctx.fillStyle = '#ff384e'
    ctx.beginPath()
    ctx.rect(self.x, self.y, self.width, self.height)
    ctx.fill()

    ctx.fillStyle = '#190f3a'
    ctx.beginPath()
    ctx.moveTo(self.maxX, self.maxY)
    ctx.lineTo(self.maxX - xGap, self.maxY + yGap)
    ctx.lineTo(self.x - xGap, self.maxY + yGap)
    ctx.lineTo(self.x, self.maxY)
    ctx.fill()
    
    ctx.fillStyle = '#9d0919'
    ctx.beginPath()
    ctx.moveTo(self.x, self.y)
    ctx.lineTo(self.x, self.maxY)
    ctx.lineTo(self.x - xGap, self.maxY + yGap)
    ctx.lineTo(self.x - xGap, self.maxY + yGap - self.height)
    ctx.fill()


class App:
  def __init__(self) -> None:
    self.canvas = document.getElementById('my_canvas')
    self.ctx = self.canvas.getContext('2d')

    self.stageWidth = self.canvas.clientWidth
    self.stageHeigh = self.canvas.clientHeight

    window.addEventListener('resize', create_proxy(self.resize), False)
    self.resize()

    self.ball = Ball(self.stageWidth, self.stageHeigh, 60, 10)
    self.block = Block(700, 30, 300, 450)

    window.requestAnimationFrame(create_proxy(self.animate))
  
  def resize(self, *argv):
    self.stageWidth = document.body.clientWidth
    self.stageHeigh = document.body.clientHeight

    self.canvas.width = self.stageWidth * 2
    self.canvas.heifht = self.stageHeigh * 2
    self.ctx.scale(2, 2)

    self.ball = Ball(self.stageWidth, self.stageHeigh, 60, 10)

  def draw_wrapper(self):
    self.canvas.width = self.canvas.width
    self.block.draw(self.ctx)
    self.ball.draw(self.ctx, self.stageWidth, self.stageHeigh, self.block)
  
  def animate(self, t):
    setInterval(create_proxy(self.draw_wrapper), 10)


App()