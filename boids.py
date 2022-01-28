import random
import yaml
from numpy import array
random.seed(42)
config = yaml.safe_load(open("config.yaml"))


class Boids:
	def __init__(self,
		count,
		x_range,
		y_range,
		xv_range,
		yv_range,
		flock_attraction,
		avoidance_radius,
		formation_flying_radius,
		speed_matching
		):
		#TODO: decouple the creation of boids from the updating
		self.count = count
		self.x_range = x_range
		self.y_range = y_range
		self.xv_range = xv_range
		self.yv_range = yv_range
		self.flock_attraction = flock_attraction
		self.avoidance_radius = avoidance_radius
		self.formation_flying_radius = formation_flying_radius
		self.speed_matching = speed_matching

	def initialize_boids(self):
		self.boids = [
			Boid(
				random.uniform(*self.x_range),
				random.uniform(*self.y_range),
				random.uniform(*self.xv_range),
				random.uniform(*self.yv_range),
				self
			)
			for boid in range(self.count)
		]

	def initialize_from_data(self, data):
		self.boids = [Boid(x, y, xv, yv, self) for x, y, xv, yv in zip(*data)]

	def update_boids(self):
		for me in self.boids:
			for other in self.boids:
				me.interact(other)
		for me in self.boids:
			for other in self.boids:
				me.interact_formation(other)				
		for me in self.boids:
			me.position += me.velocity


class Boid:
	def __init__(self,x,y,xv,yv,flock):
		self.position = array([x,y])
		self.velocity = array([xv,yv])
		self.flock = flock

	def interact(self, other):
		separation = other.position - self.position
		# Fly to middle
		self.velocity += separation*self.flock.flock_attraction / self.flock.count
		# Fly away from nearby boids
		if separation.dot(separation) < self.flock.avoidance_radius**2:
			self.velocity -= separation
	
	def interact_formation(self, other):
		separation = other.position - self.position
		if separation.dot(separation) < self.flock.formation_flying_radius**2:
			self.velocity += (other.velocity-self.velocity)*self.flock.speed_matching /self.flock.count