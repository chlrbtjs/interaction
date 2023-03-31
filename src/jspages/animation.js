const canvas = document.getElementById("my_canvas");
const context = canvas.getContext("2d");

const point = {
  x: 0,
  y: 0,
  vx: 0,
  vy: 0,
  k: 0.001,
  r: 10,
  color: '#000000'
}

const mouse = {
  x: 0,
  y: 0,
}

const draw = () => {
  canvas.width = canvas.width;

  point.vx += point.k*(mouse.x - point.x);
  point.vy += point.k*(mouse.y - point.y);

  point.vx *= 0.99;
  point.vy *= 0.99;

  point.x += point.vx;
  point.y += point.vy;
  
  context.fillStyle = point.color;
  context.beginPath();
  context.arc(point.x, point.y, point.r, 0, Math.PI * 2, false);
  context.closePath();
  context.fill();
};

const move = e => {
  mouse.x = e.offsetX;
  mouse.y = e.offsetY;
}

const down = e => {
  point.r = 30;
  point.color = "#ff0000";
}

const up = e => {
  point.r = 10;
  point.color = "#000000";
}

document.getElementById('body').addEventListener("mousemove", move);
document.getElementById('body').addEventListener("mousedown", down);
document.getElementById('body').addEventListener("mouseup", up);

setInterval(() => {
  requestAnimationFrame(() => draw())
}, 10);
