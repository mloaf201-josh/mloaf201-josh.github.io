document.addEventListener("DOMContentLoaded",function(){
// Neural Network Animation — hero-only, mouse-reactive
// Based on Nicky Case's Neurotic Neurons
(function(){
const hero = document.querySelector('.hero');
if(!hero) return;

const canvas = document.createElement('canvas');
canvas.id = 'neural-bg';
const s = canvas.style;
s.position = 'absolute';
s.top = '0';
s.left = '0';
s.width = '100%';
s.height = '100%';
s.zIndex = '0';
s.pointerEvents = 'auto';
s.opacity = '0.5';
hero.style.position = 'relative';
hero.prepend(canvas);

const ctx = canvas.getContext('2d');
let W, H, mx = -999, my = -999;

function resize(){
  W = canvas.width = hero.offsetWidth;
  H = canvas.height = hero.offsetHeight;
}
window.addEventListener('resize', resize);
resize();

// Mouse tracking
hero.addEventListener('mousemove', function(e){
  const rect = hero.getBoundingClientRect();
  mx = e.clientX - rect.left;
  my = e.clientY - rect.top;
});
hero.addEventListener('mouseleave', function(){
  mx = -999; my = -999;
});

// Neuron network
const NEURONS = 40;
const CONNECTION_DIST = 200;
const neurons = [];
const impulses = [];

class Neuron {
  constructor(){
    this.x = Math.random() * W;
    this.y = Math.random() * H;
    this.vx = (Math.random() - 0.5) * 0.4;
    this.vy = (Math.random() - 0.5) * 0.4;
    this.radius = 3 + Math.random() * 4;
    this.br = 0;
    this.tbr = 0;
    this.phase = Math.random() * Math.PI * 2;
    this.baseVx = this.vx;
    this.baseVy = this.vy;
  }
  update(){
    // Mouse interaction — gentle attraction
    if(mx > 0 && my > 0){
      const dx = mx - this.x;
      const dy = my - this.y;
      const dist = Math.sqrt(dx*dx + dy*dy);
      if(dist < 250){
        const force = (1 - dist / 250) * 0.3;
        this.vx += dx / dist * force * 0.1;
        this.vy += dy / dist * force * 0.1;
        this.tbr = 1 - dist / 250;
      }
    }
    
    this.x += this.vx;
    this.y += this.vy;
    if(this.x < 0 || this.x > W){ this.vx *= -1; this.x = Math.max(0, Math.min(W, this.x)); }
    if(this.y < 0 || this.y > H){ this.vy *= -1; this.y = Math.max(0, Math.min(H, this.y)); }
    
    // Damping — return to base speed
    this.vx += (this.baseVx - this.vx) * 0.01;
    this.vy += (this.baseVy - this.vy) * 0.01;
    
    this.br += (this.tbr - this.br) * 0.05;
    this.tbr = Math.max(0.1, this.tbr * 0.99);
  }
}

class Impulse {
  constructor(from, to){
    this.from = from; this.to = to;
    this.prog = 0;
    this.speed = 0.02 + Math.random() * 0.01;
  }
  update(){
    this.prog += this.speed;
    return this.prog < 1;
  }
  getPos(){
    return {
      x: this.from.x + (this.to.x - this.from.x) * this.prog,
      y: this.from.y + (this.to.y - this.from.y) * this.prog,
    };
  }
}

for(let i = 0; i < NEURONS; i++) neurons.push(new Neuron());

setInterval(function(){
  if(neurons.length < 2) return;
  const from = neurons[Math.floor(Math.random() * neurons.length)];
  const targets = neurons.filter(function(n){
    if(n === from) return false;
    const dx = from.x - n.x, dy = from.y - n.y;
    return Math.sqrt(dx*dx + dy*dy) < CONNECTION_DIST;
  });
  if(targets.length > 0){
    impulses.push(new Impulse(from, targets[Math.floor(Math.random() * targets.length)]));
    from.tbr = 1;
  }
}, 600 + Math.random() * 300);

function draw(){
  ctx.clearRect(0, 0, W, H);
  neurons.forEach(function(n){ n.update(); });

  // Connections
  for(let i = 0; i < neurons.length; i++){
    for(let j = i + 1; j < neurons.length; j++){
      const a = neurons[i], b = neurons[j];
      const dx = a.x - b.x, dy = a.y - b.y;
      const dist = Math.sqrt(dx*dx + dy*dy);
      if(dist < CONNECTION_DIST){
        const alpha = (1 - dist / CONNECTION_DIST) * 0.12 * (0.3 + a.br * 0.7 + b.br * 0.7);
        ctx.beginPath();
        ctx.moveTo(a.x, a.y);
        ctx.lineTo(b.x, b.y);
        ctx.strokeStyle = 'rgba(100, 180, 255, ' + alpha + ')';
        ctx.lineWidth = 0.5;
        ctx.stroke();
      }
    }
  }

  // Impulses
  for(let i = impulses.length - 1; i >= 0; i--){
    const imp = impulses[i];
    if(!imp.update()){ impulses.splice(i, 1); continue; }
    const pos = imp.getPos();
    const p = imp.prog;
    
    // Glow on line
    ctx.beginPath();
    ctx.moveTo(imp.from.x, imp.from.y);
    ctx.lineTo(imp.to.x, imp.to.y);
    ctx.strokeStyle = 'rgba(150, 220, 255, ' + (0.4 * (1 - Math.abs(p - 0.5) * 2)) + ')';
    ctx.lineWidth = 2.5;
    ctx.stroke();

    // Signal glow
    const grad = ctx.createRadialGradient(pos.x, pos.y, 0, pos.x, pos.y, 10);
    grad.addColorStop(0, 'rgba(255, 255, 255, 0.9)');
    grad.addColorStop(0.3, 'rgba(100, 200, 255, 0.6)');
    grad.addColorStop(1, 'rgba(100, 200, 255, 0)');
    ctx.beginPath();
    ctx.arc(pos.x, pos.y, 10, 0, Math.PI * 2);
    ctx.fillStyle = grad;
    ctx.fill();
  }

  // Neurons
  neurons.forEach(function(n){
    const r = n.radius * (0.5 + n.br * 0.8);
    const alpha = 0.3 + n.br * 0.7;
    
    // Glow
    const grad = ctx.createRadialGradient(n.x, n.y, 0, n.x, n.y, r * 5);
    grad.addColorStop(0, 'rgba(150, 200, 255, ' + (alpha * 0.3) + ')');
    grad.addColorStop(1, 'rgba(150, 200, 255, 0)');
    ctx.beginPath();
    ctx.arc(n.x, n.y, r * 5, 0, Math.PI * 2);
    ctx.fillStyle = grad;
    ctx.fill();

    // Core
    ctx.beginPath();
    ctx.arc(n.x, n.y, r, 0, Math.PI * 2);
    ctx.fillStyle = 'rgba(180, 220, 255, ' + alpha + ')';
    ctx.fill();
  });

  requestAnimationFrame(draw);
}
draw();
})();
});
