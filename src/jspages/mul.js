const canvas = document.getElementById("my_canvas");
const context = canvas.getContext("2d");

// 마우스 위치
const mouse = {
  x: 0,
  y: 0,
}

const move = e => {
  mouse.x = e.offsetX;
  mouse.y = e.offsetY;
}

document.getElementById('body').addEventListener("mousemove", move);

// 존재하는 점들
const points = []

class point {
  constructor(x, y) {
    this.x = x;
    this.y = y;
    this.vx = 0;
    this.vy = 0;
    this.ax = 0;
    this.ay = 0;
    this.m = 0.001; //mass
    this.f = 0.99;  //friction
    this.r = 10;    //radius
    this.c = "#000000" //color

    setInterval(() => {
      this.move();
    }, 10);
  }

  set_acceleration = (ax, ay) => {
    this.ax = ax;
    this.ay = ay;
  }

  increase_velocity = (vx, vy) => {
    this.vx += vx;
    this.vy += vy;
  }

  set_color = c => {
    this.c = c;
  }

  move = () => {
    this.vx += this.m * this.ax;
    this.vy += this.m * this.ay;

    this.vx *= this.f;
    this.vy *= this.f;

    this.x += this.vx;
    this.y += this.vy;
  }
}

// draw
const draw = () => {
  canvas.width = canvas.width;
  

  points.forEach(p => {
    p.set_acceleration(mouse.x - p.x, mouse.y - p.y);

    context.fillStyle = p.c;
    context.beginPath();
    context.arc(p.x, p.y, p.r, 0, Math.PI * 2, false);
    context.closePath();
    context.fill();
  });
  
}

//make point
const mkpoint = () => {
  points.push(new point(mouse.x, mouse.y))
  // console.log(points[0])
}

document.getElementById('body').addEventListener("mousedown", mkpoint);

//explode
const explode = () => {
  points.forEach(p => {
    let vx = (Math.random()-0.5)*20
    let vy = Math.random() * Math.sqrt(100 - Math.pow(vx, 2))
    if(Math.random() > 0.5) {
      vy *= -1;
    }
    p.increase_velocity(vx, vy)
    p.set_color("#" + Math.round(Math.random()*0xffffff).toString(16));
  });
}

document.getElementById('body').addEventListener("mouseup", explode);

setInterval(() => {
  requestAnimationFrame(() => draw())
}, 10);

setInterval(() => {
  explode();
}, 1500);