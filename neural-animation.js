// Neural Network Animation — inspired by Nicky Case's Neurotic Neurons
// Self-contained, no dependencies. Drop into any page.
(function(){
const canvas = document.createElement('canvas');
canvas.id = 'neural-bg';
const style = canvas.style;
style.position = 'fixed';
style.top = '0';
style.left = '0';
style.width = '100%';
style.height = '100%';
style.zIndex = '0';
style.pointerEvents = 'none';
style.opacity = '0.6';
document.body.prepend(canvas);

const ctx = canvas.getContext('2d');
let W, H;

function resize(){
  W = canvas.width = window.innerWidth;
  H = canvas.height = window.innerHeight;
}
window.addEventListener('resize', resize);
resize();

// Neuron network
const NEURONS = 50;
const CONNECTION_DIST = 200;
const neurons = [];
const impulses = [];

class Neuron {
  constructor(){
    this.x = Math.random() * W;
    this.y = Math.random() * H;
    this.vx = (Math.random() - 0.5) * 0.3;
    this.vy = (Math.random() - 0.5) * 0.3;
    this.radius = 3 + Math.random() * 4;
    this.brightness = 0;
    this.targetBrightness = 0;
    this.phase = Math.random() * Math.PI * 2;
  }
  update(){
    this.x += this.vx;
    this.y += this.vy;
    if(this.x < 0 || this.x > W) this.vx *= -1;
    if(this.y < 0 || this.y > H) this.vy *= -1;
    this.brightness += (this.targetBrightness - this.brightness) * 0.05;
    this.targetBrightness = 0.1 + 0.05 * Math.sin(Date.now() * 0.001 + this.phase);
  }
}

class Impulse {
  constructor(from, to){
    this.from = from;
    this.to = to;
    this.progress = 0;
    this.speed = 0.02 + Math.random() * 0.01;
  }
  update(){
    this.progress += this.speed;
    return this.progress < 1;
  }
  getPosition(){
    const f = this.from, t = this.to;
    const p = this.progress;
    return {
      x: f.x + (t.x - f.x) * p,
      y: f.y + (t.y - f.y) * p,
    };
  }
}

// Create neurons
for(let i = 0; i < NEURONS; i++){
  neurons.push(new Neuron());
}

// Fire impulses periodically
function fireImpulse(){
  if(neurons.length < 2) return;
  const from = neurons[Math.floor(Math.random() * neurons.length)];
  // Find a connected neuron
  const targets = neurons.filter(n => {
    const dx = from.x - n.x, dy = from.y - n.y;
    return n !== from && Math.sqrt(dx*dx + dy*dy) < CONNECTION_DIST;
  });
  if(targets.length > 0){
    const to = targets[Math.floor(Math.random() * targets.length)];
    impulses.push(new Impulse(from, to));
    from.targetBrightness = 1;
    to.targetBrightness = 0.8;
  }
}

setInterval(fireImpulse, 800 + Math.random() * 400);

// Animation loop
function draw(){
  ctx.clearRect(0, 0, W, H);

  // Update
  neurons.forEach(n => n.update());

  // Draw connections
  for(let i = 0; i < neurons.length; i++){
    for(let j = i + 1; j < neurons.length; j++){
      const a = neurons[i], b = neurons[j];
      const dx = a.x - b.x, dy = a.y - b.y;
      const dist = Math.sqrt(dx*dx + dy*dy);
      if(dist < CONNECTION_DIST){
        const alpha = (1 - dist / CONNECTION_DIST) * 0.15;
        ctx.beginPath();
        ctx.moveTo(a.x, a.y);
        ctx.lineTo(b.x, b.y);
        ctx.strokeStyle = `rgba(100, 180, 255, ${alpha})`;
        ctx.lineWidth = 0.5;
        ctx.stroke();
      }
    }
  }

  // Draw impulses
  for(let i = impulses.length - 1; i >= 0; i--){
    const imp = impulses[i];
    if(!imp.update()){
      impulses.splice(i, 1);
      continue;
    }
    const pos = imp.getPosition();
    const grad = ctx.createRadialGradient(pos.x, pos.y, 0, pos.x, pos.y, 8);
    grad.addColorStop(0, 'rgba(255, 255, 255, 0.9)');
    grad.addColorStop(0.3, 'rgba(100, 200, 255, 0.6)');
    grad.addColorStop(1, 'rgba(100, 200, 255, 0)');
    ctx.beginPath();
    ctx.arc(pos.x, pos.y, 8, 0, Math.PI * 2);
    ctx.fillStyle = grad;
    ctx.fill();

    // Glow on connection line
    const f = imp.from, t = imp.to;
    const p = imp.progress;
    ctx.beginPath();
    ctx.moveTo(f.x, f.y);
    ctx.lineTo(t.x, t.y);
    ctx.strokeStyle = `rgba(150, 220, 255, ${0.4 * (1 - Math.abs(p - 0.5) * 2)})`;
    ctx.lineWidth = 2;
    ctx.stroke();
  }

  // Draw neurons
  neurons.forEach(n => {
    const r = n.radius * (0.5 + n.brightness * 0.5);
    const alpha = 0.3 + n.brightness * 0.7;
    
    // Glow
    const grad = ctx.createRadialGradient(n.x, n.y, 0, n.x, n.y, r * 4);
    grad.addColorStop(0, `rgba(150, 200, 255, ${alpha * 0.3})`);
    grad.addColorStop(1, 'rgba(150, 200, 255, 0)');
    ctx.beginPath();
    ctx.arc(n.x, n.y, r * 4, 0, Math.PI * 2);
    ctx.fillStyle = grad;
    ctx.fill();

    // Core
    ctx.beginPath();
    ctx.arc(n.x, n.y, r, 0, Math.PI * 2);
    ctx.fillStyle = `rgba(180, 220, 255, ${alpha})`;
    ctx.fill();
  });

  requestAnimationFrame(draw);
}
draw();
})();
