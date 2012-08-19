////////////////// Particle ////////////////////////////
function Particle() {
    this.x = 0.0;
    this.y = 0.0;
    this.vx = 0.0;
    this.vy = 0.0;
    this.ax = 0.0;
    this.ay = 0.0;
    this.targetX = null;
    this.targetY = null;
    this.targetForce = .003;
}


Particle.prototype.addForce = function (newAx, newAy) {
    this.ax += newAx;
    this.ay += newAy;
};


Particle.prototype.applyTargetForce = function() {
    // add force to target
    if (this.targetX != null)
        this.ax += (this.targetX - this.x) * this.targetForce;

    if (this.targetY != null)
        this.ay += (this.targetY - this.y) * this.targetForce;
};


Particle.prototype.move = function () {
    var dampening = 0.5;
    // update v and pos
    this.vx += this.ax;
    this.vy += this.ay;
    this.x += this.vx;
    this.y += this.vy;
    var d = Math.sqrt(this.vx*this.vx + this.vy*this.vy);
    // dampen
    this.vx *= dampening;
    this.vy *= dampening;
    // clear forces
    this.ax = 0;
    this.ay = 0;
    // return traveled distance
    return d;
};


////////////////// Spring ////////////////////////////
function Spring(particle1, particle2, len) {
    this.particle1 = particle1;
    this.particle2 = particle2;
    this.len = len;
    this.k = 0.01;
}


Spring.prototype.pushNpull = function () {
    var dx = this.particle1.x - this.particle2.x;
    var dy = this.particle1.y - this.particle2.y;
    var d = Math.sqrt(dx * dx + dy * dy);
    while (d < 10e-4) { // too close
        dx = -0.5 + Math.random();
        dy = -0.5 + Math.random();
        d = Math.sqrt(dx*dx + dy*dy);
    }
    var fx = this.k * (this.len - d) * dx/d;
    var fy = this.k * (this.len - d) * dy/d;
    this.particle1.addForce(fx, fy);
    this.particle2.addForce(-fx, -fy);
};


////////////////// Repulsion ////////////////////////////
function calculateRepulsion(particles) {
    for (var i = 0; i < particles.length-1; ++i) {
        var p1 = particles[i];
        for (var j = i+1; j < particles.length; ++j) {
            var p2 = particles[j];
            var dx = p1.x - p2.x;
            var dy = p1.y - p2.y;
            var d = Math.sqrt(dx*dx + dy*dy);
            while (d < 10e-4) { // too close
                dx = -0.5 + Math.random();
                dy = -0.5 + Math.random();
                d = Math.sqrt(dx*dx + dy*dy);
            }
            var force = 20 * Math.pow((50 / (d + 40)), 3);
            p1.addForce(force*dx/d, force*dy/d);
            p2.addForce(-force*dx/d, -force*dy/d);
        }
    }
}


////////////////// Global Update ////////////////////////////
function updateParticles(particles, springs) {
    // determine forces
    calculateRepulsion(particles);
    for (var i = 0; i < springs.length; ++i)
        springs[i].pushNpull();
    for ( i = 0; i < particles.length; ++i)
        particles[i].applyTargetForce();
    // move particles
    var totalDistance = 0.0;
    for (i = 0; i < particles.length; ++i)
        totalDistance += particles[i].move();
    return totalDistance;
}
